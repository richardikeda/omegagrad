import sys
if '--phase3' in sys.argv:
    from omegagrad.phase3_report import build
    build()
    raise SystemExit(0)
import sys
if '--phase2' in sys.argv:
    from omegagrad.phase2_report import build
    build()
    raise SystemExit(0)
import json,html
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image,PageBreak,Table,TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
root=Path('outputs/first_run'); data=json.loads((root/'results.json').read_text(encoding='utf-8'))
out=Path('output/pdf');out.mkdir(parents=True,exist_ok=True)
styles=getSampleStyleSheet();styles['BodyText'].fontSize=10;styles['BodyText'].leading=14
story=[]
def p(t,style='BodyText'):story.append(Paragraph(html.escape(t),styles[style]));story.append(Spacer(1,7))
def img(path,w=490,h=400):story.append(Image(str(path),width=w,height=h,kind='proportional'));story.append(Spacer(1,8))
def table(rows):
 t=Table(rows,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#155e75')),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('GRID',(0,0),(-1,-1),.3,colors.lightgrey)]));story.append(t);story.append(Spacer(1,12))
p('OMEGAGRAD','Title');p('Resultados experimentais e atlas de gráficos','Heading1');p('Laboratório de aritmética finita | 6 de novembro de 2026')
p('Este relatório reúne a implementação, o protocolo, os resultados das 24 simulações em quatro escalas e a validação inicial com autograd. As conclusões distinguem propriedades observadas, efeitos da regularização e hipóteses ainda não demonstradas.')
p('Síntese dos resultados','Heading2')
p('Com suavização proporcional ao inverso do quadrado do horizonte, todos os primos conhecidos foram recuperados nas três sementes de cada escala. Com epsilon fixo, os poços se fundem ou desaparecem: em 12 bits, restam 74 mínimos para 564 primos. A assimetria das barreiras não superou o preditor de referência no teste espacial realizado.')
p('A recuperação usa um campo que já contém os primos. Ela não constitui descoberta de primos desconhecidos. Os impulsos para atravessar barreiras são intervenções controladas e estão separados da descida nos registros.')
table([['Bits','Horizonte','Primos','Poços fixos','Poços escalados']]+[[s, next(r['summary']['p_omega'] for r in data['universes'] if r['summary']['s_bits']==s),next(r['summary']['prime_count'] for r in data['universes'] if r['summary']['s_bits']==s)]+[next(r['summary']['minimum_count'] for r in data['universes'] if r['summary']['s_bits']==s and r['summary']['epsilon_mode']==m) for m in ['fixed','scaled']] for s in [6,8,10,12]])
p('Validação: 23 testes passaram. A diferença máxima entre gradientes por autograd e fórmulas analíticas foi 7,28e-11. As 24 trajetórias terminaram no limite inferior; todas as partições de bacias somaram 1 e os catálogos de raízes estabilizaram sob refinamento da malha.')
story.append(PageBreak());p('Comparação visual das escalas','Heading1');img(root/'comparison.png',490,390)
p('Leitura: no alto, a perda de mínimos e de cobertura com epsilon fixo contrasta com a preservação no controle escalado. Embaixo à esquerda, as distribuições de larguras relativas se aproximam nas escalas maiores. Embaixo à direita, a dispersão de log(lambda) contra o próximo gap inferior não revela uma regra determinística simples.')
p('As medianas de largura relativa foram 1,012, 1,020 e 1,022 em 8, 10 e 12 bits. As distâncias KS entre escalas adjacentes foram aproximadamente 0,060 e 0,070. São medidas descritivas; dependência espacial e normalização impedem interpretá-las como prova de universalidade.')
story.append(PageBreak());p('Protocolo, métricas e interpretação detalhada','Heading1')
# Preserve the complete generated textual report, translating Markdown tables into PDF tables.
lines=(root/'REPORT.md').read_text(encoding='utf-8').splitlines();i=0
while i<len(lines):
 line=lines[i]
 if line.startswith('|'):
  rows=[]
  while i<len(lines) and lines[i].startswith('|'):
   cells=[x.strip() for x in lines[i].strip('|').split('|')]
   if not all(set(x)<=set('-: ') for x in cells):rows.append(cells)
   i+=1
  # Wrap dense comparative tables inside cells.
  if rows:
   rows=[[Paragraph(html.escape(c),styles['BodyText']) for c in row] for row in rows]
   t=Table(rows,colWidths=[490/len(rows[0])]*len(rows[0]),repeatRows=1)
   t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e2e8f0')),('GRID',(0,0),(-1,-1),.3,colors.lightgrey)]));story.append(t);story.append(Spacer(1,12))
  continue
 if line.startswith('## '):p(line[3:],'Heading2')
 elif line and not line.startswith('# '):p(line)
 i+=1
for r in data['universes']:
 s=r['summary'];mode=s['epsilon_mode'];bits=s['s_bits'];story.append(PageBreak());p(f'Atlas: {bits} bits | epsilon {mode}','Heading1')
 p(f"Horizonte {s['p_omega']}; {s['prime_count']} primos; epsilon={s['epsilon']:.8g}. Largura de suavização em unidades inteiras: {s['smoothing_width_integer']:.5g}.")
 img(root/f'{mode}_{bits}bits'/'landscape.png',490,410)
 p(f"Foram encontrados {s['minimum_count']} mínimos e {s['barrier_count']} barreiras. Cobertura validada média: {s['coverage_mean']:.2%}; intervalo entre sementes: {s['coverage_min']:.2%} a {s['coverage_max']:.2%}.")
 p('Painel superior: potencial e pontos estacionários (verde: mínimos; vermelho: máximos). Painel central: derivada; cruzamentos descendentes de zero indicam barreiras e ascendentes indicam atratores. Painel inferior: trajetória da semente 0; azul identifica descida e laranja identifica escape controlado. Os gráficos usam escalas verticais próprias.')
 p('A contagem de mínimos não é igual à cobertura: um mínimo pode estar deslocado demais para ser associado a um primo pelo critério de distância de 0,25 unidade inteira. As bacias medidas pertencem ao fluxo sem momento e sem ruído.')
story.append(PageBreak());p('Validação inicial com autograd','Heading1');img(Path('outputs/autograd_validation/fixed_6bits/landscape.png'),490,410);p('Neste ensaio, o próprio gradiente da navegação foi calculado por Value.backward(). Os 18 primos foram recuperados. Na bateria principal, o backend analítico vetorizado foi usado para reduzir o custo, sendo confrontado com autograd em cada configuração.')
p('Reprodução e fontes','Heading2');p('Executar: .venv/Scripts/python.exe -m pytest -q; depois .venv/Scripts/python.exe -m omegagrad.experiments. O README contém instalação e comando da validação integral por autograd.')
p('Fontes do estudo: docs/THEORY.md e docs/METHODOLOGY.md. Resultados auditáveis: outputs/first_run/results.json, summary.csv, scale_comparisons.csv e arquivos de cada universo. A pesquisa não apresenta revisão bibliográfica sistemática ou demonstração de originalidade.')
p('Os JSON incluem parâmetros, sementes, versões e hashes dos módulos. CSV individuais preservam raízes, gaps, bacias, previsões e trajetórias completas. Este PDF reúne o relatório e todos os gráficos; os registros por iteração permanecem nos CSV para auditoria.')
def footer(canvas,doc):
 canvas.setFont('Helvetica',8);canvas.setFillColor(colors.grey);canvas.drawString(42,25,'OMEGAGRAD | Laboratório experimental | 06/11/2026');canvas.drawRightString(553,25,str(doc.page))
path=out/'OMEGAGRAD_Resultados_Completos.pdf'
SimpleDocTemplate(str(path),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=40,bottomMargin=44).build(story,onFirstPage=footer,onLaterPages=footer)
from pypdf import PdfReader
reader=PdfReader(path);print(path.resolve());print('Pages:',len(reader.pages));print('Empty pages:',[i+1 for i,p in enumerate(reader.pages) if not p.extract_text().strip()])
