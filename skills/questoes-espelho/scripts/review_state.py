"""Prepare blind review packets and check revision evidence; no pedagogical grading."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

FORBIDDEN = {"correct", "answer", "correct_answer", "expected_answer", "gabarito",
             "solution", "resolution", "resolucao", "resolução", "private", "spec", "rationale"}
DEFAULT_CHECKS = ["content", "cognitive", "mirror"]


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def resolve_path(value, base):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Caminho ausente ou inválido")
    path = Path(value)
    return (base / path).resolve() if not path.is_absolute() else path.resolve()


def check_student(value, location="student"):
    if isinstance(value, dict):
        for key, child in value.items():
            if key.strip().casefold() in FORBIDDEN:
                raise ValueError(f"Campo privado na versão estudantil: {location}.{key}")
            check_student(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            check_student(child, f"{location}[{index}]")


def prepare_item(path):
    path = Path(path).resolve()
    item = read_json(path)
    if not isinstance(item, dict):
        raise ValueError("Item precisa ser um objeto JSON")
    if not isinstance(item.get("id"), str) or not item["id"].strip():
        raise ValueError("Item sem ID textual estável")
    if not item.get("student") or not isinstance(item["student"], dict):
        raise ValueError("Item sem objeto student completo")
    check_student(item["student"])
    assets = item.get("assets", [])
    if not isinstance(assets, list):
        raise ValueError("assets precisa ser uma lista")
    resolved_assets = []
    seen = set()
    for asset in assets:
        if not isinstance(asset, dict) or not isinstance(asset.get("id"), str) or not asset["id"]:
            raise ValueError("Ativo sem ID")
        if asset["id"] in seen:
            raise ValueError(f"ID de ativo duplicado: {asset['id']}")
        seen.add(asset["id"])
        target = resolve_path(asset.get("path"), path.parent)
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        if asset.get("sha256") and asset["sha256"].lower() != digest:
            raise ValueError(f"Hash declarado desatualizado do ativo {asset['id']}")
        resolved_assets.append({"id": asset["id"], "path": str(target), "sha256": digest})
    payload = {key: item.get(key) for key in ("id", "student", "private", "spec")}
    # Include actual asset bytes' digests: editing an image in place invalidates review.
    payload["assets"] = [{"id": a["id"], "sha256": a["sha256"]} for a in resolved_assets]
    digest = hashlib.sha256(canonical(payload).encode("utf-8")).hexdigest()
    return item, digest, resolved_assets


def packet(path):
    item, digest, assets = prepare_item(path)
    return {"id": item["id"], "item_sha256": digest, "student": item["student"],
            "assets": assets}


def evidence_nonempty(path):
    """Reject blank text reports; binary evidence remains an existence check."""
    if not path.is_file():
        return False
    content = path.read_bytes()
    if not content:
        return False
    try:
        return bool(content.decode("utf-8-sig").strip())
    except UnicodeDecodeError:
        return True


def check_state(path):
    path = Path(path).resolve()
    state = read_json(path)
    if not isinstance(state, dict):
        raise ValueError("Estado precisa ser um objeto")
    expected = state.get("expected_item_ids")
    if (not isinstance(expected, list) or not expected
            or any(not isinstance(item_id, str) or not item_id.strip() for item_id in expected)
            or len(set(expected)) != len(expected)):
        raise ValueError("expected_item_ids deve listar os IDs solicitados, únicos e não vazios; sem essa lista não é possível comprovar a cobertura do lote")
    expected_set = set(expected)
    checks = state.get("required_checks", DEFAULT_CHECKS)
    if (not isinstance(checks, list) or not checks
            or any(not isinstance(c, str) or not c.strip() for c in checks)
            or len(set(checks)) != len(checks)):
        raise ValueError("required_checks precisa conter nomes únicos e não vazios")
    entries = state.get("items")
    if not isinstance(entries, list):
        raise ValueError("items precisa ser uma lista")
    results, seen = [], set()
    for entry in entries:
        problems = []
        item_id = entry.get("id") if isinstance(entry, dict) else None
        if not isinstance(item_id, str) or not item_id.strip() or item_id in seen:
            raise ValueError(f"ID ausente ou duplicado no estado: {item_id!r}")
        seen.add(item_id)
        if item_id not in expected_set:
            problems.append("ID extra: item não consta da encomenda em expected_item_ids")
        digest = None
        try:
            item_path = resolve_path(entry.get("path"), path.parent)
            item, digest, _ = prepare_item(item_path)
            if item["id"] != item_id:
                problems.append("ID do snapshot diverge do estado")
            reviews = entry.get("reviews", [])
            if not isinstance(reviews, list) or any(not isinstance(r, dict) for r in reviews):
                raise ValueError("reviews precisa ser lista de objetos")
            for name in checks:
                candidates = [r for r in reviews if r.get("check") == name]
                if not candidates:
                    problems.append(f"Revisão ausente: {name}")
                    continue
                # The latest record controls: an old success cannot hide a newer failure.
                review = candidates[-1]
                if review.get("item_sha256") != digest:
                    problems.append(f"Revisão de outra versão: {name}")
                if review.get("result") != "pass":
                    problems.append(f"Revisão não aprovada automaticamente: {name}")
                evidence = resolve_path(review.get("evidence"), path.parent)
                if not evidence_nonempty(evidence):
                    problems.append(f"Evidência ausente ou vazia: {name}")
            if entry.get("pending"):
                problems.append(f"Pendência registrada: {entry['pending']}")
        except (OSError, ValueError, TypeError) as exc:
            problems.append(str(exc))
        results.append({"id": item_id, "item_sha256": digest, "mechanically_complete": not problems,
                        "problems": problems})
    missing = [item_id for item_id in expected if item_id not in seen]
    extras = [result["id"] for result in results if result["id"] not in expected_set]
    for item_id in missing:
        results.append({"id": item_id, "item_sha256": None, "mechanically_complete": False,
                        "problems": ["Item solicitado ausente do estado"]})
    by_id = {result["id"]: result for result in results}
    results = [by_id[item_id] for item_id in expected] + [by_id[item_id] for item_id in extras]
    complete = sum(r["mechanically_complete"] for r in results if r["id"] in expected_set)
    return {"scope": "revision fingerprints and evidence files; not pedagogical validation",
            "requested": len(expected), "recorded": len(entries), "mechanically_complete": complete,
            "pending": len(expected) - complete, "missing_item_ids": missing, "unexpected_item_ids": extras,
            "coverage_complete": not missing and not extras,
            "all_mechanical_checks_passed": complete == len(expected) and not extras,
            "items": results}


def main():
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("packet", "check"):
        command_parser = sub.add_parser(command)
        command_parser.add_argument("input", type=Path)
        command_parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = packet(args.input) if args.command == "packet" else check_state(args.input)
        serialized = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            if args.output.resolve() == args.input.resolve():
                raise ValueError("A saída não pode sobrescrever a entrada")
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(serialized, encoding="utf-8")
        else:
            print(serialized, end="")
        return 2 if args.command == "check" and not result["all_mechanical_checks_passed"] else 0
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
