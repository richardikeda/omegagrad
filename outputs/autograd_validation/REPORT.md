# OMEGAGRAD: primeiro laboratorio reproduzivel

Configuracao e resultados numericos, sem afirmacao de descoberta de primos desconhecidos.

Execucao UTC: 2026-11-06T05:11:47.323060+00:00. Seeds: [0]. Backend: autograd.

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

## Validacao numerica

- fixed S=6: erro maximo AD vs analitico=5.68e-14; residuo maximo nas raizes=1.04e-10; estimativa |L'/L''|=5.3e-17; malha estavel=True; estados=lower_boundary.

## Assimetria e proximo gap inferior

Para p[k]<p[k+1], lambda=(z*-p[k]/P)/(p[k+1]/P-z*). Alvo: p[k]-p[k-1]. Usa-se log(lambda) para a regressao.
Treino nos 70% superiores, um intervalo de embargo e teste na regiao inferior. Apenas gaps com exatamente uma barreira entram; a selecao pode introduzir vies.
A separacao protege o ajuste da regressao, mas o potencial global continua contendo os primos-alvo. Os resultados sao retrospectivos, sem evidencia de previsao cega.

|epsilon|bits|n treino/teste|rho Spearman|MAE media treino|MAE gap ajustado|MAE log(lambda)|R2 log(lambda)|
|---|---:|---:|---:|---:|---:|---:|---:|
|fixed|6|11/4|0.399|1.932|2.307|2.343|-4.715|

## Comparacao de escala

Larguras brutas encolhem por normalizacao e pela quantidade de atratores: media=1/numero_de_bacias quando particionam [0,1]. Isso sozinho nao prova invariancia.
Comparacao descritiva das larguras divididas pela media dos gaps adjacentes; exclui primos nas duas bordas. KS e distancia entre CDFs, sem p-valor inferencial.

|epsilon|bits A/B|mediana A|mediana B|distancia KS|
|---|---:|---:|---:|---:|

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
