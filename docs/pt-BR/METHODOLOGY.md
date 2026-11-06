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
