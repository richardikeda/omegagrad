"""Phase 2 report, generated exclusively from persisted experimental data."""
import json
from pathlib import Path
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Image,PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

def build():
 root=Path('outputs/phase2');data=json.loads((root/'results.json').read_text(encoding='utf-8'));lines=['# Fase 2: Background Detrending & Blind Wave Sieve','', '## Protocolo e limites','',
 'O fundo usa somente horizonte, epsilon e densidade P/log(uP). Integração adaptativa seguida de spline cúbica em 2049 pontos globais e refinamento local nas bordas; comparação com 1025 pontos globais registra sensibilidade do gradiente. A derivada da spline é uma aproximação da derivada do integral. A densidade assintótica é uma escolha de modelo, especialmente aproximada perto de 2.',
 'O detrending ainda usa todos os primos em L. A regressão combina log(lambda) e log(abs(H)) da barreira, com intervalos pareados antes/depois, treino espacial superior de 70%, um intervalo de embargo e teste inferior. Portanto, não é uma previsão cega. Ganho em MAE e R² positivo são critérios distintos.',
 'A onda recebe somente o horizonte e a base até sua raiz quadrada. O horizonte é informado e sua primalidade não é descoberta. O scanner percorre brackets do gradiente em ordem decrescente e refina mínimos com Brent; trata-se de enumeração de pontos estacionários, não de uma trajetória de descida com momento. Candidatos são inteiros arredondados, sem filtro de divisibilidade e sem consulta à verdade. Toda a lista de primos do intervalo é usada apenas pelo avaliador.',
 'A resolução da onda foi comparada entre passos 0,05 e 0,025. Isso não prova completude: extremos muito próximos podem escapar. Epsilon finito limita a altura das barreiras; não há garantia de que um primo seja mínimo nem de que arredondar um mínimo evite compostos.',
 'O holdout remove aproximadamente 10% dos primos internos com semente 42 e preserva o horizonte. Registra raízes antes/depois, deslocamentos dos mínimos associados e Hessianas. Um diagnóstico simples propõe o ponto médio de gaps retidos maiores que duas vezes a mediana. Este controle usa apenas a base retida; a lista removida é usada para pontuação exata. Não é um estimador otimizado de coordenadas via Hessianas. Os catálogos permitem analisar mudanças de limites das bacias.',
 'Os gráficos e catálogos de raízes usam malha global e amostras locais na escala de epsilon. A fase 2 não fornece certificação de completude dos catálogos residuais. Não foi isolado o efeito individual de lambda versus Hessiana nesta regressão conjunta.', '', '## Resultados por escala','']
 for r in data['universes']:
  b=r['blind'];a=r['detrending_after'];before=r['detrending_before'];h=r['holdout']['metrics']
  lines += [f"### {r['bits']} bits",f"Base pequena: {r['base']}. Horizonte: {r['horizon']}.",f"Onda cega: precisão {b['precision']:.4f}; recall {b['recall']:.4f}; F1 {b['f1']:.4f}. TP={b['tp']}, FP={b['fp']}, FN={b['fn']}. Candidatos estáveis sob refinamento: {r['blind_grid_stable']}.",f"Regressão antes: MAE {before['model']['mae']:.4f}, R² {before['model']['r2']:.4f}. Depois: MAE {a['model']['mae']:.4f}, R² {a['model']['r2']:.4f}. Baseline: MAE {a['baseline']['mae']:.4f}. Treino/teste: {a['train']}/{a['test']}.",f"Sensibilidade máxima do gradiente de fundo (1025/2049 pontos): {r['background_gradient_refinement_max']:.6g}.",f"Holdout: {len(r['holdout']['hidden'])} removidos; acertos exatos={h['tp']}, falsos positivos={h['fp']}, não recuperados={h['fn']}; F1={h['f1']:.4f}.",'']
 lines += ['## Conclusões iniciais','', 'A remoção do fundo melhora o erro médio em relação à média de treino nas quatro escalas avaliadas, mas não atinge R² positivo. Esse resultado não demonstra que a deriva de borda era a única causa da baixa previsão.', 'A onda é cega em relação aos primos interiores, mas os mínimos arredondados não formam um crivo preciso. A alta recuperação vem acompanhada de muitos falsos positivos. Testes modulares poderiam eliminar compostos, mas mudariam o método para um crivo clássico; não foram usados para melhorar as métricas.', 'O holdout mede perturbações e avalia uma regra explícita de recuperação. Comparar com o campo completo serve como diagnóstico retrospectivo, não como informação disponível a um detector cego. Não se conclui identificação única de primos ocultos a partir da geometria.', '', '## Reprodução','', 'Executar python -m omegagrad.phase2 e python build_results_pdf.py --phase2. Resultados completos em outputs/phase2/results.json e arquivos por escala. Os CSV registram deslocamentos e Hessianas dos pontos associados. Testes: python -m pytest -q.']
 text='\n\n'.join(lines);(root/'REPORT.md').write_text(text,encoding='utf-8')
 styles=getSampleStyleSheet();styles['BodyText'].leading=14;story=[]
 import html
 for line in lines:
  if not line:continue
  style='Heading1' if line.startswith('# ') else 'Heading2' if line.startswith('##') else 'BodyText'
  story.append(Paragraph(html.escape(line.lstrip('# ')),styles[style]));story.append(Spacer(1,8))
 for r in data['universes']:
  story.extend([PageBreak(),Paragraph(f"Atlas: {r['bits']} bits",styles['Heading1']),Image(str(root/f"{r['bits']}bits.png"),width=490,height=327),Spacer(1,16),Paragraph('Em cima: potencial original e fundo; potencial residual. Embaixo: gradiente residual e onda cega nos últimos 80 inteiros do horizonte. A comparação não garante que cada mínimo corresponda a um primo.',styles['BodyText'])])
 path=Path('output/pdf/OMEGAGRAD_Phase2_Blind_Discovery.pdf');SimpleDocTemplate(str(path),pagesize=A4,leftMargin=42,rightMargin=42).build(story)
 print(path)
if __name__=='__main__':build()
