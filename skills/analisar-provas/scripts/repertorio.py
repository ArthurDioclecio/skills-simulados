"""Read-only repertoire lookup/validation; explicit inventory output. No external packages."""
import argparse,hashlib,json,sys,unicodedata
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def norm(s):return ''.join(c for c in unicodedata.normalize('NFKD',s.casefold()) if not unicodedata.combining(c))
def validate(d,verify_files=False):
 errors=[];warnings=[]
 if d.get('schema_version')!=1:errors.append('schema_version deve ser1')
 if d.get('status') not in ['partial','complete']:errors.append('status inválido')
 if not d.get('exam') or not d.get('exam_id'):errors.append('Identidade da prova ausente')
 sources=d.get('sources',[]);items=d.get('items',[]);claims=d.get('claims',[])
 source_map={s.get('id'):s for s in sources};item_map={q.get('id'):q for q in items}
 if None in source_map or len(source_map)!=len(sources):errors.append('IDs de fontes ausentes/duplicados')
 if None in item_map or len(item_map)!=len(items):errors.append('IDs de itens ausentes/duplicados')
 hashes={};occurrences=[];complete=bool(d.get('inventory_complete')) and bool(items)
 for s in sources:
  h=s.get('sha256','');path=s.get('path','')
  if len(h)!=64 or any(c not in '0123456789abcdefABCDEF' for c in h):errors.append(f'Hash inválido: {s.get("id")}')
  if h in hashes:warnings.append(f'Fontes de mesmo hash: {hashes[h]} e {s.get("id")}')
  hashes[h]=s.get('id')
  if not path:errors.append(f'Caminho de fonte ausente: {s.get("id")}')
  if verify_files:
   p=Path(path)
   if not p.is_file():warnings.append(f'Fonte local indisponível: {path}')
   elif hashlib.sha256(p.read_bytes()).hexdigest()!=h.lower():errors.append(f'Fonte alterada: {path}')
 def evidence(e):
  if 'item_id' in e:
   if e['item_id'] not in item_map:errors.append(f'Evidência aponta item ausente: {e["item_id"]}')
  elif 'source_id' in e:
   sid=e['source_id'];ps=e.get('pages',[])
   if sid not in source_map:errors.append(f'Fonte de evidência ausente: {sid}')
   elif not ps or any(not isinstance(p,int) or p<1 or (source_map[sid].get('pages') and p>source_map[sid]['pages']) for p in ps):errors.append(f'Páginas de evidência inválidas: {sid}')
  else:errors.append('Evidência sem item nem fonte/páginas')
 distributions={};annulled=0;unclassified=0
 for q in items:
  qid=q.get('id');oc=q.get('occurrences',[])
  if not oc:errors.append(f'Item sem ocorrência: {qid}');complete=False
  if not q.get('read_complete') or (q.get('visual_required') and not q.get('visual_checked')):complete=False
  for o in oc:
   key=o.get('key');sid=o.get('source_id');occurrences.append(key)
   if not key or not o.get('number'):errors.append(f'Identidade de ocorrência inválida: {qid}')
   evidence({'source_id':sid,'pages':o.get('pages',[])})
  if q.get('annulled'):annulled+=1;continue
  lvl=q.get('difficulty')
  if lvl not in ['fácil','média','difícil','indeterminada']:errors.append(f'Nível inválido: {qid}')
  if not q.get('difficulty_reason'):warnings.append(f'Dificuldade sem fundamento: {qid}')
  if lvl=='indeterminada':unclassified+=1
  key=str(q.get('stage','?'))+' | '+str(q.get('subject','?'))
  distributions.setdefault(key,Counter())[lvl]+=1
 duplicates=[k for k,n in Counter(occurrences).items() if n>1]
 if duplicates:errors.append(f'Ocorrências atribuídas mais de uma vez: {duplicates}')
 expected=d.get('expected_occurrences',[])
 if len(expected)!=len(set(expected)):errors.append('Inventário esperado contém duplicações')
 missing=sorted(set(expected)-set(occurrences));extra=sorted(set(occurrences)-set(expected),key=str)
 if missing or extra or not expected:complete=False
 if missing:warnings.append(f'{len(missing)} ocorrências esperadas sem ficha')
 if extra:warnings.append(f'{len(extra)} ocorrências fora do inventário esperado')
 claim_ids=[]
 for c in claims:
  claim_ids.append(c.get('id'));ev=c.get('evidence',[])
  if not c.get('text') or not c.get('scope'):errors.append('Padrão sem texto/escopo')
  if c.get('strength') not in ['observed','recurring','hypothesis']:errors.append('Grau de evidência inválido')
  if not ev:errors.append(f'Padrão sem evidência: {c.get("id")}')
  for e in ev:evidence(e)
  if c.get('strength')=='recurring' and len({e.get('item_id') for e in ev if 'item_id' in e})<2 and not any('source_id' in e for e in ev):errors.append(f'Recorrência sem suporte múltiplo: {c.get("id")}')
  f=c.get('frequency')
  if f:
   n=f.get('numerator');den=f.get('denominator');basis=f.get('basis')
   if not isinstance(n,int) or not isinstance(den,int) or den<=0 or n<0 or n>den:errors.append(f'Frequência impossível: {c.get("id")}')
   if not basis:errors.append('Frequência sem universo')
   limit={'unique_items':len(items),'physical_occurrences':len(occurrences)}.get(basis)
   if limit is not None and not f.get('population') and den!=limit:errors.append('Denominador não corresponde ao universo; declarar population para subconjunto')
 if len(claim_ids)!=len(set(claim_ids)) or None in claim_ids:errors.append('IDs de padrões inválidos')
 if d.get('status')=='complete' and not complete:errors.append('Análise completa declarada sem cobertura integral comprovada')
 return {'ok':not errors,'coverage_status':'complete' if complete and not errors else 'partial','unique_items':len(items),'physical_occurrences':len(occurrences),'annulled_items':annulled,'unclassified_valid_items':unclassified,'missing_occurrences':missing,'extra_occurrences':extra,'difficulty_by_stage_subject':{k:dict(v) for k,v in distributions.items()},'errors':errors,'warnings':warnings,'note':'Validação estrutural; não certifica leitura, solução, qualidade editorial ou representatividade.'}
def main():
 ap=argparse.ArgumentParser(description=__doc__);sub=ap.add_subparsers(dest='cmd',required=True)
 p=sub.add_parser('lookup');p.add_argument('exam');p.add_argument('--edition',type=int)
 p=sub.add_parser('inventory');p.add_argument('files',nargs='+');p.add_argument('--output',required=True)
 p=sub.add_parser('validate');p.add_argument('analysis');p.add_argument('--verify-files',action='store_true')
 a=ap.parse_args()
 if a.cmd=='lookup':
  found=[]
  for p in read(ROOT/'references/repertorio/index.json')['profiles']:
   if any(norm(a.exam)==norm(n) for n in [p['exam_id'],p['name']]+p.get('aliases',[])):
    if a.edition is None or a.edition in p.get('exam_editions',[]):found.append(p)
  out={'matches':found,'action':'Ler perfil e verificar etapa/edição.' if found else 'Nenhum perfil compatível; analisar as fontes enviadas sem herdar outra banca.'}
 elif a.cmd=='inventory':
  records=[];seen={}
  for name in a.files:
   p=Path(name).resolve()
   if not p.is_file():ap.error(f'Arquivo não encontrado: {p}')
   h=hashlib.sha256(p.read_bytes()).hexdigest();ident=f's{len(records)+1}'
   records.append({'id':ident,'path':str(p),'sha256':h,'bytes':p.stat().st_size,'duplicate_of':seen.get(h)});seen.setdefault(h,ident)
  out={'files':records,'note':'Inventário de arquivos; identidade de prova e cobertura de itens ainda exigem análise.'}
  target=Path(a.output);target.parent.mkdir(parents=True,exist_ok=True);target.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf8')
 else:out=validate(read(a.analysis),a.verify_files)
 print(json.dumps(out,ensure_ascii=False,indent=2))
 return 1 if out.get('ok') is False else 0
if __name__=='__main__':sys.exit(main())
