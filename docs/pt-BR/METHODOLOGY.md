# Protocolo experimental

## Desenho

Quatro escalas: 6, 8, 10 e 12 bits. Duas políticas: epsilon=1e-6 fixo e epsilon=1e-6*(61/P_omega)^2 escalado. Três sementes: 0, 1 e 2. Total: 24 trajetórias, além do ensaio de 6 bits com autograd na navegação.

O controle escalado mantém sqrt(epsilon)*P_omega=0,061 em unidades inteiras. Assim, separa parte do efeito da regularização do aumento do horizonte.

## Raízes e bacias

Amostragem com espaçamento ligado a sqrt(epsilon), brackets por mudança de sinal, Brent e polimento Newton. A malha inicia em 8 amostras por largura de suavização e dobra até estabilidade, limitada a 128. Em 12 bits com epsilon fixo, o refinamento foi necessário para resolver um par próximo.

Cada raiz registra resíduo do gradiente, Hessiano, largura do bracket e estimativa |L'/L''|. Esta última é uma estimativa local, não um limite certificado. Raízes tangenciais ou degeneradas podem escapar do método de mudança de sinal.

As bacias são intervalos delimitados pelos máximos para o fluxo dz/dt=-L'(z) em [0,1]. A extensão ao ponto zero é usada apenas como fronteira. As larguras devem somar 1. Não se trata de bacias da dinâmica com ruído e momento.

## Navegação

Partida z=1, momento 0,5 e ruído relativo 0,02, com semente explícita. O passo é adaptado à curvatura e limitado; backtracking verifica o potencial. O ruído desaparece com o deslocamento proposto para permitir convergência. Isso não é um amostrador térmico de Langevin.

Ao encontrar um mínimo, um transporte externo para a esquerda cruza a barreira. O navegador não consulta o catálogo de raízes para esse transporte. Porém, o campo já contém a lista de primos. As fases `descent` e `escape` ficam registradas.

Uma captura requer gradiente pequeno e Hessiano positivo. Depois, a coordenada inteira é arredondada: só recebe rótulo primo se a distância for no máximo 0,25 e o inteiro pertencer à base de referência. Por isso, quantidade de mínimos e cobertura são métricas distintas.

## Assimetria e teste de gaps

Para p[k]<p[k+1], lambda=(z*-p[k]/P)/(p[k+1]/P-z*). O alvo é o próximo gap inferior p[k]-p[k-1]. Apenas intervalos com uma barreira entram. Essa seleção pode produzir viés.

Ajusta-se regressão linear com log(lambda), com o gap atual e com ambos. Treino nos 70% superiores, um intervalo de embargo e teste na região inferior. Comparam-se MAE e R² com a média do treino e o gap atual. Duzentos embaralhamentos dos alvos de treino são diagnósticos, não testes de significância sob independência espacial.

A separação protege o ajuste dos coeficientes, mas não elimina informação do alvo contida no potencial global. O teste é retrospectivo.

## Comparação de escala

A largura de cada bacia é dividida pela média dos gaps vizinhos ao primo associado. Excluem-se associações aos primos das duas extremidades. Comparam-se medianas e distância entre CDFs pelo KS, sem interpretação inferencial de p-valores. A média das larguras brutas é 1/número de bacias quando elas particionam o domínio; seu encolhimento sozinho é uma identidade geométrica.

## Fases 2 e 3

Na Fase 2, a quadratura do fundo e a spline são refinadas globalmente e nas bordas. A regressão conjunta usa log(lambda) e log(abs(H)) e compara intervalos que têm uma barreira única antes e depois da subtração. A onda recebe o horizonte e a base até sua raiz quadrada. A varredura descendente detecta mudanças de sinal e refina mínimos por Brent. Os passos 0,05 e 0,025 são comparados. Os mínimos são arredondados e pontuados contra uma referência separada. O holdout remove aproximadamente 10% dos primos internos com semente 42. A regra testada propõe o ponto médio de intervalos retidos maiores que duas vezes a mediana.

Na Fase 3, a soma logarítmica exclui 2 e 3. A busca usa células de largura 0,98 centradas em 6k±1. Energia e curvatura têm tetos escolhidos entre quatro quantis, e a distância fracionária admite 0,1, 0,25 ou 0,49. O F1 de treino usa somente rótulos da base pequena. A autoanulação dos termos dos primos da base induz uma diferença entre calibração e teste. O experimento não isolou seu efeito causal.

Os sobreviventes passam por Miller–Rabin forte base 2. Chamadas são comparadas tanto com todos os inteiros quanto com 6k±1. O tempo total inclui radar e verificação. Os registros de tempo são de execuções individuais.

Em 12, 14 e 16 bits, a bisseção em lote busca barreiras em intervalos centrais dos gaps e rejeita curvatura inválida. A regressão acrescenta o deslocamento da barreira em unidades inteiras. O fundo refinado tem 4097 nós globais, refinamento nas bordas e integração subdividida. Os resultados iniciais com 2049 nós permitem avaliar sensibilidade. A geometria usa a base completa, incluindo os alvos. KS compara distribuições empíricas e tem interpretação descritiva.
