#!/usr/bin/env python3
"""Plan ordered, indivisible batches of normalized question items using stdlib.

This helper never opens spreadsheets, extracts mirrors, generates questions, or
changes input data. Missing mirror metadata is reported for later verification.
Run with --help for the JSON contract and examples.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0"
EFFORT_WEIGHTS = {"simple": 1, "standard": 1, "complex": 2}
DEFAULT_REQUIRED_MIRROR_FIELDS = ("exam", "edition", "question")


class PlanningError(ValueError):
    """An invalid normalized input, with a stable machine-readable code."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def positive_integer(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise PlanningError("invalid_capacity", f"{name} must be a positive integer.")
    return value


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def json_fingerprint(payload: dict[str, Any]) -> str:
    try:
        canonical = json.dumps(
            payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeError) as exc:
        raise PlanningError("invalid_json_value", "Input must contain valid JSON values.") from exc
    return "sha256:" + hashlib.sha256(canonical).hexdigest()


def field_is_missing(mirror: dict[str, Any], field: str) -> bool:
    # Dotted relative field paths permit future profile-specific metadata.
    value: Any = mirror
    for part in field.split("."):
        if not isinstance(value, dict) or part not in value:
            return True
        value = value[part]
    return value is None or (isinstance(value, str) and not value.strip()) or value == [] or value == {}


def plan_batches(payload: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic plan without mutating payload.

    All item IDs and shared-stimulus IDs are opaque, nonempty strings. Connected
    stimulus groups form indivisible units. If a component spans other items,
    its whole interval is indivisible, preserving the original item order.
    """
    if not isinstance(payload, dict):
        raise PlanningError("invalid_input", "The JSON root must be an object.")
    if "items" not in payload or not isinstance(payload["items"], list):
        raise PlanningError("invalid_items", "items must be an array (an empty array is allowed).")
    items = payload["items"]
    max_items = positive_integer(payload.get("max_items", 5), "max_items")
    max_effort = payload.get("max_effort_units")
    if max_effort is not None:
        max_effort = positive_integer(max_effort, "max_effort_units")

    required = payload.get("required_mirror_fields", list(DEFAULT_REQUIRED_MIRROR_FIELDS))
    if not isinstance(required, list) or any(
        not nonempty_string(field)
        or field.startswith("mirror.")
        or any(not part.strip() for part in field.split("."))
        for field in required
    ):
        raise PlanningError(
            "invalid_required_fields",
            "required_mirror_fields must be an array of nonempty paths relative to mirror, e.g. ['exam', 'edition', 'question'].",
        )
    if len(set(required)) != len(required):
        raise PlanningError("duplicate_required_fields", "required_mirror_fields contains duplicates.")

    ids: list[str] = []
    seen: set[str] = set()
    efforts: list[int] = []
    validations: list[dict[str, Any]] = []
    stimuli_by_item: list[list[str]] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise PlanningError("invalid_item", f"items[{index}] must be an object.")
        item_id = item.get("id")
        if not nonempty_string(item_id):
            raise PlanningError("missing_item_id", f"items[{index}].id must be an existing, nonempty string; IDs are never invented.")
        if item_id in seen:
            raise PlanningError("duplicate_item_id", f"Duplicate item ID: {item_id!r}.")
        seen.add(item_id)
        ids.append(item_id)

        complexity = item.get("complexity", "standard")
        if not isinstance(complexity, str) or complexity not in EFFORT_WEIGHTS:
            raise PlanningError("invalid_complexity", f"Item {item_id!r}: complexity must be simple, standard, or complex.")
        efforts.append(EFFORT_WEIGHTS[complexity])

        stimuli = item.get("shared_stimulus_ids", [])
        if not isinstance(stimuli, list) or any(not nonempty_string(stimulus) for stimulus in stimuli):
            raise PlanningError("invalid_stimulus_ids", f"Item {item_id!r}: shared_stimulus_ids must be an array of nonempty strings.")
        stimuli_by_item.append(stimuli)

        mirror = item.get("mirror")
        if mirror is None:
            mirror = {}
        if not isinstance(mirror, dict):
            raise PlanningError("invalid_mirror", f"Item {item_id!r}: mirror must be an object or null.")
        missing = ["mirror." + field for field in required if field_is_missing(mirror, field)]
        validations.append({
            "item_id": item_id,
            "missing_fields": missing,
            "blocked_for_authoring": bool(missing),
            "status": "needs_verified_metadata" if missing else "metadata_present_not_verified",
            "effort_units": efforts[-1],
            "complexity_assumed": "complexity" not in item,
        })

    fingerprint = json_fingerprint(payload)
    parent = list(range(len(items)))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(first: int, second: int) -> None:
        a, b = find(first), find(second)
        if a != b:
            parent[b] = a

    first_by_stimulus: dict[str, int] = {}
    for index, stimuli in enumerate(stimuli_by_item):
        for stimulus in stimuli:
            if stimulus in first_by_stimulus:
                union(index, first_by_stimulus[stimulus])
            else:
                first_by_stimulus[stimulus] = index

    components: dict[int, list[int]] = {}
    for index in range(len(items)):
        components.setdefault(find(index), []).append(index)
    intervals = sorted((positions[0], positions[-1]) for positions in components.values())
    units: list[tuple[int, int]] = []
    for start, end in intervals:
        if units and start <= units[-1][1]:
            units[-1] = (units[-1][0], max(units[-1][1], end))
        else:
            units.append((start, end))

    def exceeds(count: int, effort: int) -> bool:
        return count > max_items or (max_effort is not None and effort > max_effort)

    warnings: list[dict[str, Any]] = []
    if not items:
        warnings.append({"code": "empty_input", "message": "No items to plan."})
    batches: list[dict[str, Any]] = []
    current_indices: list[int] = []
    current_units: list[list[str]] = []
    current_effort = 0

    def flush() -> None:
        nonlocal current_indices, current_units, current_effort
        if not current_indices:
            return
        batch_id = f"B{len(batches) + 1:03d}"
        item_ids = [ids[index] for index in current_indices]
        oversize = exceeds(len(item_ids), current_effort)
        batch_warnings: list[str] = []
        if oversize:
            batch_warnings.append("indivisible_unit_exceeds_capacity")
            warnings.append({
                "code": "indivisible_unit_exceeds_capacity",
                "batch_id": batch_id,
                "item_ids": item_ids,
                "message": "The indivisible ordered unit is retained whole despite exceeding a configured capacity.",
            })
        batches.append({
            "batch_id": batch_id,
            "item_ids": item_ids,
            "item_count": len(item_ids),
            "effort_units": current_effort,
            "oversize": oversize,
            "indivisible_units": current_units,
            "blocked_item_ids": [ids[index] for index in current_indices if validations[index]["blocked_for_authoring"]],
            "warnings": batch_warnings,
        })
        current_indices = []
        current_units = []
        current_effort = 0

    for start, end in units:
        indices = list(range(start, end + 1))
        unit_effort = sum(efforts[index] for index in indices)
        if current_indices and exceeds(len(current_indices) + len(indices), current_effort + unit_effort):
            flush()
        current_indices.extend(indices)
        current_units.append([ids[index] for index in indices])
        current_effort += unit_effort
        if exceeds(len(indices), unit_effort):
            flush()
    flush()

    planned_ids = [item_id for batch in batches for item_id in batch["item_ids"]]
    planned_set = set(planned_ids)
    # Internal invariant checks remain active under python -O.
    if planned_ids != ids or len(planned_set) != len(ids):
        raise RuntimeError("Planner invariant failed: coverage or original order changed.")
    return {
        "schema_version": SCHEMA_VERSION,
        "source_fingerprint": fingerprint,
        "max_items": max_items,
        "max_effort_units": max_effort,
        "effort_weights": dict(EFFORT_WEIGHTS),
        "required_mirror_fields": list(required),
        "batches": batches,
        "item_validation": validations,
        "missing_fields": [validation for validation in validations if validation["missing_fields"]],
        "coverage": {
            "input_items": len(ids),
            "planned_items": len(planned_ids),
            "unique_planned_items": len(planned_set),
            "complete": planned_ids == ids,
            "missing_item_ids": [],
            "duplicate_item_ids": [],
            "original_order_preserved": planned_ids == ids,
        },
        "warnings": warnings,
    }


def reject_constant(value: str) -> None:
    raise PlanningError("invalid_json_value", f"Non-finite JSON number {value!r} is not allowed.")


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise PlanningError("duplicate_json_key", f"Duplicate JSON object key: {key!r}.")
        result[key] = value
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Plan ordered question batches from normalized JSON; never reads XLSX or creates mirror metadata.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Input contract:
  {"items": [{"id": "q001", "mirror": {"exam": "SSA", "stage": 3,
    "edition": 2026, "day": 2, "question": 1},
    "shared_stimulus_ids": [], "complexity": "standard"}],
   "max_items": 5, "max_effort_units": null,
   "required_mirror_fields": ["exam", "edition", "question"]}

max_items limits question count (default 5). Optional max_effort_units limits
effort: simple/standard = 1, complex = 2. Missing complexity defaults to standard
and is explicitly reported. All IDs must already exist and remain unchanged.
Connected shared stimuli, including intervening items, cannot be split. Oversize
units remain whole with a warning. For SSA profiles, include stage and day in
required_mirror_fields. Missing fields do not prevent planning; they flag items
for verified extraction before authorship. Presence is not factual validation.
Source fingerprint is SHA-256 of the complete input with sorted JSON keys.

Examples:
  python plan_batches.py input.json > plan.json
  python plan_batches.py input.json --output plan.json
  cat input.json | python plan_batches.py -

Exit codes: 0 = plan produced (possibly warnings); 2 = input or I/O error.
Errors are JSON on stderr. No network or non-stdlib dependencies are used.
""",
    )
    parser.add_argument("input", nargs="?", default="-", help="UTF-8 JSON file or - for stdin (default)")
    parser.add_argument("--output", "-o", help="UTF-8 JSON output file; defaults to stdout")
    args = parser.parse_args(argv)
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    try:
        if args.output and args.input != "-" and Path(args.input).resolve() == Path(args.output).resolve():
            raise PlanningError("input_output_conflict", "Output must not overwrite the input file.")
        raw = sys.stdin.read().lstrip("\ufeff") if args.input == "-" else Path(args.input).read_text(encoding="utf-8-sig")
        payload = json.loads(raw, parse_constant=reject_constant, object_pairs_hook=reject_duplicate_keys)
        result = plan_batches(payload)
        encoded = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
        if args.output:
            Path(args.output).write_text(encoded, encoding="utf-8")
        else:
            sys.stdout.write(encoded)
        return 0
    except json.JSONDecodeError as exc:
        error = {"code": "invalid_json", "message": f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}."}
    except PlanningError as exc:
        error = {"code": exc.code, "message": str(exc)}
    except (OSError, UnicodeError) as exc:
        error = {"code": "io_error", "message": str(exc)}
    sys.stderr.write(json.dumps({"error": error}, ensure_ascii=False) + "\n")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
