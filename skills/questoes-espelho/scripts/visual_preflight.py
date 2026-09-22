"""Flag bounding-box collisions/clipping in code-native visuals. Alerts are not judgments."""
import argparse,json
from pathlib import Path
def check(d):
 width,height=d['width'],d['height'];els=d.get('elements',[]);alerts=[];ids=set()
 for e in els:
  if e['id'] in ids:raise ValueError('ID de elemento duplicado')
  ids.add(e['id']);x,y,w,h=e['bbox']
  if w<0 or h<0:raise ValueError('Caixa com dimensão negativa')
  if x<0 or y<0 or x+w>width or y+h>height:alerts.append({'type':'clipping','id':e['id']})
 for i,a in enumerate(els):
  for b in els[i+1:]:
   if a.get('kind')!='text' and b.get('kind')!='text':continue
   if a.get('kind') in ['background','container'] or b.get('kind') in ['background','container']:continue
   if b['id'] in a.get('allow_overlap_with',[]) or a['id'] in b.get('allow_overlap_with',[]):continue
   ax,ay,aw,ah=a['bbox'];bx,by,bw,bh=b['bbox']
   if min(ax+aw,bx+bw)>max(ax,bx) and min(ay+ah,by+bh)>max(ay,by):alerts.append({'type':'potential_overlap','elements':[a['id'],b['id']]})
 return {'alerts':alerts,'result':'requires_visual_review','note':'Caixas aproximam traçados; falsos positivos/negativos possíveis. Não verifica pertinência, conteúdo, contraste ou raster/OCR. Inspecionar ativo e saída final mesmo sem alertas.'}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');a=p.parse_args()
 print(json.dumps(check(json.loads(Path(a.input).read_text(encoding='utf-8-sig'))),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
