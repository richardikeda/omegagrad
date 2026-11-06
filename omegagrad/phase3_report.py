"""Auditable phase 3 tables and report."""
import json,math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image,PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from .experiments import write_csv

def build():
 out=Path('outputs/phase3');d=json.loads((out/'results.json').read_text());rows=d['radar']
 table=[]
 for r in rows:
  table.append(dict(bits=r['bits'],precision=r['filtered']['precision'],recall=r['filtered']['recall'],f1=r['filtered']['f1'],hybrid_precision=r['hybrid']['precision'],hybrid_recall=r['hybrid']['recall'],hybrid_f1=r['hybrid']['f1'],modular_calls=r['modular_calls'],all_integer_calls=r['integer_baseline_calls'],phase_locked_calls=r['phase_locked_baseline_calls'],reduction=1-r['modular_calls']/r['integer_baseline_calls'],reduction_vs_6k=1-r['modular_calls']/r['phase_locked_baseline_calls'],radar_seconds=r['radar_seconds'],verify_seconds=r['verify_seconds'],direct_mr_seconds=r['direct_mr_seconds']))
 write_csv(out/'summary.csv',table)
 fig,ax=plt.subplots(1,3,figsize=(14,4),layout='constrained');bits=[r['bits'] for r in rows]
 for metric in ['precision','recall','f1']:ax[0].plot(bits,[r['filtered'][metric] for r in rows],'-o',label=metric)
 ax[0].set_title('Geometric filter');ax[0].legend()
 ax[1].plot(bits,[r['hybrid']['precision'] for r in rows],'-o',label='precision');ax[1].plot(bits,[r['hybrid']['recall'] for r in rows],'-o',label='recall');ax[1].legend();ax[1].set_title('After base-2 Miller-Rabin')
 ax[2].semilogy(bits,[r['radar_seconds']+r['verify_seconds'] for r in rows],'-o',label='radar + MR');ax[2].semilogy(bits,[r['direct_mr_seconds'] for r in rows],'-o',label='direct MR');ax[2].legend();ax[2].set_title('Wall time (seconds)')
 for a in ax:a.set_xlabel('S_bits');a.grid(alpha=.2)
 fig.savefig(out/'comparison.png',dpi=180);plt.close(fig)
 lines=['# Fase 3 - v0.3.0','## Protocolo e interpretação',
 'O radar remove 2 e 3 da soma e procura mínimos em células de largura 0,98 centradas na malha 6k±1. Esta é uma restrição aritmética explícita, não descoberta emergente do potencial. Usar +cos²(pi*x) não seria equivalente: seus mínimos são semi-inteiros.',
 'E, H e distância fracionária são avaliados nos mínimos. O centro de energia é a média das energias dos mínimos de calibração. Limiar de energia e teto de curvatura vêm de quatro quantis; delta vem de 0,1, 0,25 ou 0,49. Seleciona-se o melhor F1 somente na base pequena. Não se usaram os primos-alvo na calibração. Em 6 bits não houve mínimos de calibração e o filtro retorna conjunto vazio.',
 'Há uma diferença estrutural entre treino e teste: um primo da base pequena é divisor de seu próprio termo da onda, enquanto um primo grande não é. Portanto, a calibração solicitada não representa a mesma distribuição de poços. O desempenho baixo nas escalas maiores pode refletir essa diferença; o experimento não isola sua causa.',
 'Miller-Rabin base 2 decompõe n-1=2^s*d e verifica a cadeia de quadrados. Não é apenas Fermat. Ambos estão implementados e testados separadamente. Uma única base não certifica primalidade; 2047 é um contraexemplo no teste unitário. As métricas finais usam verdade independente.',
 'O scanner usa gradientes analíticos e refinamento de raízes. As avaliações de campo já são vetorizadas por NumPy, mas a enumeração de células e calibração permanecem em laços Python. Não se atribui a escala alcançada exclusivamente ao novo TensorValue.',
 'TensorValue implementa broadcasting e retropropagação reversa. A segunda derivada é direcional por propagação de segunda ordem; em lotes de coordenadas independentes produz as Hessianas locais. Não oferece Hessiana densa de saídas acopladas. A validação compara 2048 coordenadas com fórmulas analíticas.',
 'Para geometria de 12/14/16 bits, barreiras são localizadas por bisseção vetorizada no interior central de cada gap. Intervalos sem bracket ou sem Hessiana negativa são excluídos e contados. As larguras são distâncias entre barreiras adjacentes divididas pelo gap local médio. Não são estimativas certificadas de todas as bacias possíveis.',
 'A regressão usa log(lambda residual), log(abs(H da barreira)) e deslocamento da barreira residual em relação à original, em unidades inteiras. Treino nos 70% superiores, embargo de uma linha e teste inferior. O campo ainda contém os primos-alvo; R² positivo significa associação retrospectiva, não previsão cega.',
 'O fundo foi refinado de 2049 para 4097 pontos globais com amostragem local nas bordas e integração subdividida na escala de epsilon. Na execução refinada, avisos de integração são tratados como erros. Os resultados iniciais e refinados são preservados para sensibilidade.',
 '## Resultados do radar e verificador']
 for r,t in zip(rows,table):
  lines.append(f"{r['bits']} bits: filtro P={t['precision']:.4f}, R={t['recall']:.4f}, F1={t['f1']:.4f}; híbrido P={t['hybrid_precision']:.4f}, R={t['hybrid_recall']:.4f}, F1={t['hybrid_f1']:.4f}. Chamadas modulares={t['modular_calls']}; redução contra todos os inteiros={t['reduction']:.2%}, contra 6k±1={t['reduction_vs_6k']:.2%}. Tempo radar={t['radar_seconds']:.3f}s; verificador={t['verify_seconds']:.4f}s; MR direto={t['direct_mr_seconds']:.4f}s. FP antes/depois do limiar na mesma malha: {r['phase_locked']['fp']}/{r['filtered']['fp']}.")
 r12=next(r for r in rows if r['bits']==12)
 lines+=['## Comparação com a Fase 2',f"Na Fase 2 havia 2211 FP em 12 bits; agora restam {r12['filtered']['fp']}. A diferença entre essas contagens não pode ser atribuída apenas à profundidade: também mudaram a base e a restrição de fase. A ablação na mesma malha, acima, isola a etapa de limiares. Primos descartados não podem ser recuperados pelo verificador posterior.",'## Geometria estendida']
 for r in d['geometry']:lines.append(f"{r['bits']} bits: R²={r['model']['r2']:.6f}, MAE={r['model']['mae']:.6f}, baseline MAE={r['baseline']['mae']:.6f}; barreiras={r['barriers']}, brackets ausentes={r['missing']}.")
 for r in d['ks']:lines.append(f"KS descritivo {r['a']}/{r['b']}: {r['ks']:.6f}.")
 lines+=['## Conclusão geral: o que funcionou, limites teóricos e descobertas empíricas',
 'O filtro geométrico pode elevar a precisão, mas perde recall e não mantém o mesmo desempenho ao ampliar o horizonte. Economizar chamadas modulares não implica economizar tempo: a construção e varredura do campo devem entrar no custo. A tabela permite comparar ambos na mesma máquina, sem alegar benchmark universal.',
 'A regressão estendida pode apresentar R² positivo, mas usa o potencial construído com o conjunto completo. Isso não resolve o limite do oráculo. A segunda derivada automática em lote foi validada no regime de coordenadas independentes; escala do potencial completo continua quadraticamente custosa ao avaliar um número de pontos proporcional ao número de primos.',
 'Não foi demonstrado um novo crivo competitivo, uma lei determinística de gaps ou invariância universal. Os resultados são experimentais, dependem dos critérios de seleção e incluem as falhas de calibração. Próximos testes precisam separar observáveis sem informação dos alvos, controles não primos e calibração transferível.',
 '## Reprodução', 'python -m omegagrad.phase3; python -m omegagrad.phase3_refine; python build_results_pdf.py --phase3. Tests: python -m pytest -q. summary.csv contém os benchmarks, radar.json os candidatos e limiares, arquivos features.csv os vetores geométricos e results.json a geometria, validação tensorial e sensibilidade. 18 bits foi executado para radar; a geometria estendida abrange 12,14,16 bits.']
 (out/'REPORT.md').write_text(chr(10).join(lines)+chr(10),encoding='utf-8')
 import html
 styles=getSampleStyleSheet();styles['BodyText'].leading=14;story=[]
 for s in lines:story.extend([Paragraph(html.escape(s.lstrip('# ')),styles['Heading2'] if s.startswith('#') else styles['BodyText']),Spacer(1,9)])
 story.extend([PageBreak(),Image(str(out/'comparison.png'),width=490,height=140)])
 SimpleDocTemplate('output/pdf/OMEGAGRAD_Phase3_Final_Report.pdf',pagesize=A4,leftMargin=42,rightMargin=42).build(story)
if __name__=='__main__':build()
