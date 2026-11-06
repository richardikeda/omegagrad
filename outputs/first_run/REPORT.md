# OMEGAGRAD: primeiro laboratorio reproduzivel

Configuracao e resultados numericos, sem afirmacao de descoberta de primos desconhecidos.

Execucao UTC: 2026-11-06T05:12:36.606801+00:00. Seeds: [0, 1, 2]. Backend: analytic.

## Protocolo

- Corte operacional: maior primo <= 2**S_bits. Nao calcula K(p)+T(p) nem valida um limite fisico cosmologico.
- L(z) = soma log((z-p/P_omega)^2+epsilon); W(x) = soma sin^2(pi*x/p).
- Derivada segunda: soma 2*(epsilon-d^2)/(d^2+epsilon)^2, com d=z-p/P_omega.
- Epsilon fixo = 1e-6. Controle escalado = 1e-6*(61/P_omega)^2; largura de suavizacao em inteiros = 0.061.
- Raizes por brackets + Brent + polimento Newton; malhas iniciam com 8 e 16 amostras por sqrt(epsilon), duplicando ate estabilizar (maximo 128). Estabilidade de malha nao e certificacao de todas as raizes, sobretudo degeneradas.
- Bacias do fluxo deterministico dz/dt=-L'(z), no dominio [0,1], delimitadas por maximos locais. Nao sao bacias da dinamica com momento/ruido.
- OmegaSieve parte de z=1, usa gradiente, momento e ruido relativo ao passo, com backtracking. Apos convergir, um transporte externo para a esquerda cruza a barreira; cada fase aparece no CSV.
- Rotulagem posterior: arredonda a coordenada inteira, exige erro <=0.25 e primalidade pela lista de referencia. Proximidade a um primo nunca basta para declarar convergencia.
- A funcao potencial ja recebe todos os primos do crivo. Cobertura e recuperacao de uma base conhecida, nao desempenho de um novo crivo de primalidade.

## Resultados

|epsilon|bits|P_omega|primos|minimos|barreiras|cobertura media|
|---|---:|---:|---:|---:|---:|---:|
|fixed|6|61|18|18|17|100.00%|
|scaled|6|61|18|18|17|100.00%|
|fixed|8|251|54|53|52|98.15%|
|scaled|8|251|54|54|53|100.00%|
|fixed|10|1021|172|110|109|43.02%|
|scaled|10|1021|172|172|171|100.00%|
|fixed|12|4093|564|74|73|2.84%|
|scaled|12|4093|564|564|563|100.00%|

## Validacao numerica

- fixed S=6: erro maximo AD vs analitico=5.68e-14; residuo maximo nas raizes=1.04e-10; estimativa |L'/L''|=5.3e-17; malha estavel=True; estados=lower_boundary;lower_boundary;lower_boundary.
- scaled S=6: erro maximo AD vs analitico=5.68e-14; residuo maximo nas raizes=1.04e-10; estimativa |L'/L''|=5.3e-17; malha estavel=True; estados=lower_boundary;lower_boundary;lower_boundary.
- fixed S=8: erro maximo AD vs analitico=2.27e-13; residuo maximo nas raizes=1.05e-10; estimativa |L'/L''|=5.57e-17; malha estavel=True; estados=lower_boundary;lower_boundary;lower_boundary.
- scaled S=8: erro maximo AD vs analitico=2.27e-13; residuo maximo nas raizes=1.5e-09; estimativa |L'/L''|=5.45e-17; malha estavel=True; estados=lower_boundary;lower_boundary;lower_boundary.
- fixed S=10: erro maximo AD vs analitico=1.82e-12; residuo maximo nas raizes=9.45e-11; estimativa |L'/L''|=5.55e-17; malha estavel=True; estados=lower_boundary;lower_boundary;lower_boundary.
- scaled S=10: erro maximo AD vs analitico=3.64e-12; residuo maximo nas raizes=2.95e-08; estimativa |L'/L''|=5.54e-17; malha estavel=True; estados=lower_boundary;lower_boundary;lower_boundary.
- fixed S=12: erro maximo AD vs analitico=7.28e-12; residuo maximo nas raizes=1.29e-10; estimativa |L'/L''|=5.79e-17; malha estavel=True; estados=lower_boundary;lower_boundary;lower_boundary.
- scaled S=12: erro maximo AD vs analitico=7.28e-11; residuo maximo nas raizes=4.97e-07; estimativa |L'/L''|=5.57e-17; malha estavel=True; estados=lower_boundary;lower_boundary;lower_boundary.

## Assimetria e proximo gap inferior

Para p[k]<p[k+1], lambda=(z*-p[k]/P)/(p[k+1]/P-z*). Alvo: p[k]-p[k-1]. Usa-se log(lambda) para a regressao.
Treino nos 70% superiores, um intervalo de embargo e teste na regiao inferior. Apenas gaps com exatamente uma barreira entram; a selecao pode introduzir vies.
A separacao protege o ajuste da regressao, mas o potencial global continua contendo os primos-alvo. Os resultados sao retrospectivos, sem evidencia de previsao cega.

|epsilon|bits|n treino/teste|rho Spearman|MAE media treino|MAE gap ajustado|MAE log(lambda)|R2 log(lambda)|
|---|---:|---:|---:|---:|---:|---:|---:|
|fixed|6|11/4|0.399|1.932|2.307|2.343|-4.715|
|scaled|6|11/4|0.399|1.932|2.307|2.343|-4.715|
|fixed|8|36/15|-0.076|2.033|2.225|3.565|-4.965|
|scaled|8|36/15|-0.081|2.033|2.225|3.499|-4.758|
|fixed|10|76/32|-0.050|3.056|3.317|4.673|-3.056|
|scaled|10|118/51|-0.053|2.983|3.207|4.331|-1.680|
|fixed|12|51/21|0.112|4.534|4.485|5.388|-4.527|
|scaled|12|393/168|-0.190|3.458|3.518|5.324|-1.811|

## Comparacao de escala

Larguras brutas encolhem por normalizacao e pela quantidade de atratores: media=1/numero_de_bacias quando particionam [0,1]. Isso sozinho nao prova invariancia.
Comparacao descritiva das larguras divididas pela media dos gaps adjacentes; exclui primos nas duas bordas. KS e distancia entre CDFs, sem p-valor inferencial.

|epsilon|bits A/B|mediana A|mediana B|distancia KS|
|---|---:|---:|---:|---:|
|fixed|6/8|1.011|1.022|0.226|
|fixed|8/10|1.022|1.019|0.317|
|fixed|10/12|1.019|6.965|0.576|
|scaled|6/8|1.011|1.012|0.188|
|scaled|8/10|1.012|1.020|0.060|
|scaled|10/12|1.020|1.022|0.070|

## Interpretacao e limites

- Primos normalizados nao sao necessariamente pontos estacionarios: no primo, os demais termos contribuem um gradiente nao nulo. Medimos o deslocamento real em basins.csv.
- Com epsilon fixo, a largura sqrt(epsilon)*P cresce em unidades inteiras. A fusao/perda de pocos e um efeito da regularizacao que precisa ser separado da aritmetica.
- Mesmo com epsilon escalado, os primos adicionais mudam o campo global. Sem estabilidade quantitativa entre escalas e controles adicionais, nao se conclui invariancia.
- Maximos em uma dimensao sao barreiras, nao selas no sentido multivariado. Nao ha garantia de uma barreira por gap para epsilon positivo arbitrario.
- W(x)=0 codifica multiplos comuns da base, incluindo zero, e nao identifica automaticamente primos. Seu valor/gradiente foi validado nos testes.
- Nao sao demonstrados novos teoremas, estruturas fractais ou ganhos de complexidade. O custo de cada avaliacao do campo e linear no numero de primos previamente conhecidos.
- Proximo teste para previsao: construir observaveis que nao usem os primos ocultados; repetir em regioes/escala independentes e contra controles nao primos.

## Artefatos

- summary.csv: comparativo; results.json: configuracao, hashes, geometrias, diagnosticos e capturas.
- scale_comparisons.csv e comparison.png: comparacoes de escala.
- Por universo: gaps.csv, basins.csv, stationary_points.csv, predictions.csv, trajectory_seed*.csv, results.json e landscape.png.
