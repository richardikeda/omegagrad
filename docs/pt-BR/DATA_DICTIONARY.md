# Dicionário dos dados

| Arquivo | Conteúdo e interpretação |
|---|---|
| summary.csv | Horizonte, quantidade de primos, epsilon, mínimos, barreiras, cobertura, estabilidade e tempo por configuração |
| results.json | Metadados, hashes, diagnósticos, geometria, regressões e capturas de todas as configurações |
| scale_comparisons.csv | Medianas de larguras relativas e distâncias KS entre escalas adjacentes |
| gaps.csv | Primos inferior/superior, gap inteiro, barreiras, posição, lambda e próximo gap inferior |
| basins.csv | Mínimo real, primo mais próximo, deslocamento inteiro, limites, largura e curvatura |
| stationary_points.csv | Coordenada, tipo, resíduo absoluto, Hessiano, bracket e estimativa local de erro |
| predictions.csv | Alvos e previsões somente da região de teste |
| trajectory_seedN.csv | Iteração, z, L(z), gradiente e fase de movimento |
| landscape.png | Potencial, gradiente e trajetória da primeira semente |
| comparison.png | Comparação de topologia, cobertura, bacias e assimetria |

As coordenadas z e larguras width_z são normalizadas. Gaps, deslocamentos e width_integer usam unidades inteiras. Epsilon tem dimensão de distância normalizada ao quadrado. `nearest_prime` em basins.csv é associação descritiva, não declaração de recuperação pelo navegador.

`null` em JSON e células vazias em CSV representam valores ausentes ou não finitos, como lambda sem barreira única. Ausência não deve ser interpretada como zero. As estatísticas de cobertura agregam três sementes; sementes não são amostras independentes de universos aritméticos.

Dados de referência em `outputs/first_run`; ensaio com AD em `outputs/autograd_validation`. Os dados são gerados localmente pelo modelo; não são dados observacionais externos.

## Dados das Fases 2 e 3

| Arquivo | Conteúdo |
|---|---|
| Fase 2, results.json | Raízes originais e residuais, regressões pareadas, mínimos e candidatos da onda, alvos removidos e deslocamentos |
| Fase 2, neighbor_changes.csv | Associação a primos retidos, posição e Hessiana antes e depois da remoção |
| Fase 3, features.csv | Inteiro candidato n, coordenada estacionária x, energia, Hessiana e distância fracionária |
| Fase 3, radar.json | Limiares, candidatos, métricas antes e depois da filtragem e da verificação, chamadas modulares e tempos |
| Fase 3, geometry.json | Barreiras aceitas, intervalos ausentes, larguras relativas, variáveis da regressão e métricas |
| Fase 3, results.json | Radar, geometria inicial e refinada, distâncias KS, validação tensorial e metadados |
| Fase 3, summary.csv | Métricas do filtro e do híbrido, dois referenciais de chamadas modulares e tempos de execução |

As linhas de variáveis da Fase 3 seguem a ordem log(lambda), log(abs(H)), deslocamento em unidades inteiras e próximo gap inferior. Na Fase 2, a regressão usa apenas as duas primeiras variáveis. A regularização da onda tem configuração própria.

Precisão=TP/(TP+FP), recall=TP/(TP+FN) e F1=2PR/(P+R). A implementação usa zero quando o denominador é vazio. O R² usa a média dos alvos de teste no denominador da variância. Ganho em erro absoluto médio contra a média de treino é outro critério. Tempos medidos são descritivos.
