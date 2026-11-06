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
