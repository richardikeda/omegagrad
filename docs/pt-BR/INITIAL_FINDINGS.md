# Conclusões iniciais

## 1. A regularização controla a topologia observada

Com epsilon fixo, os números de mínimos foram 18, 53, 110 e 74, para bases de 18, 54, 172 e 564 primos. Em 12 bits, sqrt(epsilon)*P_omega=4,093 unidades inteiras. A suavização deixa de ser pequena em relação a muitos gaps.

A cobertura validada foi 100%, 98,15%, 43,02% e 2,84%. Em 12 bits, todos os 74 mínimos foram visitados, mas apenas 16 receberam rótulo primo pelo critério de distância. Isso evidencia a necessidade de separar visita a mínimos de recuperação dos pontos originais.

## 2. O controle escalado preservou os poços nas escalas testadas

Com epsilon escalado, foram encontrados 18, 54, 172 e 564 mínimos, com uma barreira entre cada par consecutivo. Todas as três sementes recuperaram a base completa. O escape controlado participa desse resultado; descida pura não enumera espontaneamente todos os poços.

## 3. Há estabilidade descritiva nas larguras relativas

Medianas de 1,012, 1,020 e 1,022 para 8, 10 e 12 bits. Distâncias KS: 0,060 entre 8 e 10; 0,070 entre 10 e 12. A similaridade é compatível com estabilidade aproximada, mas também pode refletir a normalização local e a estrutura genérica de potenciais de pontos. Não foi demonstrada invariância ou estrutura fractal.

## 4. Assimetria não melhorou a previsão neste protocolo

Em 12 bits com epsilon escalado: MAE 5,324 para log(lambda), contra 3,458 da média do treino; R²=-1,811. Esse modelo simples não generalizou melhor para a região inferior. Isso não prova impossibilidade de outras relações, mas não sustenta uma regra determinística de previsão.

## Próximos experimentos

1. Controles de pontos igualmente espaçados e aleatórios com densidade comparável.
2. Varredura sistemática de epsilon e análise de bifurcações.
3. Testes em escalas maiores, com custo e convergência registrados.
4. Observáveis calculados sem acesso aos primos-alvo ocultados.
5. Sensibilidade a localização, bordas, momento, ruído e tolerâncias.

Esses itens são propostas, não experimentos já realizados. O estudo atual não demonstra novos teoremas nem vantagem de complexidade sobre o crivo usado como referência.


## Fase 2: novos testes

A subtração do fundo contínuo melhorou o MAE do modelo conjunto de assimetria e curvatura contra a média de treino, mas não atingiu R² positivo. O modelo usa intervalos pareados antes/depois e continua retrospectivo. Portanto, não se demonstrou que a borda era a única causa da dificuldade de previsão.

A onda foi construída somente com primos até a raiz do horizonte. A precisão caiu de 36,11% para 19,51% entre 6 e 12 bits, enquanto o recall ficou entre 92,86% e 100%. Isso refuta, para o detector implementado, a identificação automática entre mínimos arredondados e primos desconhecidos.

O teste de remoção registra deslocamentos e Hessianas e avalia uma regra de anomalia de gaps: ponto médio de intervalos maiores que duas vezes a mediana dos gaps retidos. Não houve recuperações exatas nas quatro escalas. Esse resultado é específico dessa regra; não demonstra impossibilidade de detectores mais informativos. Não foram ajustados parâmetros usando os rótulos ocultos.

Detalhes, contagens e limitações numéricas estão no [relatório da Fase 2](../../outputs/phase2/REPORT.md).


## Fase 3

O filtro geométrico aumenta a precisão em 12 bits, com perda de recall. A comparação com a Fase 2 também muda a malha e a base; a redução total de falsos positivos não pode ser atribuída somente à profundidade. A calibração na base pequena tem distribuição diferente do intervalo oculto. A regressão com deslocamento das barreiras continua retrospectiva, mesmo quando R² supera zero. Resultados completos, custos e sensibilidade estão no [relatório da Fase 3](../../outputs/phase3/REPORT.md).

## Síntese da versão 1.0.0

A preservação de um mínimo por primo foi observada entre 6 e 12 bits com largura de suavização constante em unidades inteiras. A geometria residual estendida produziu distâncias KS de 0,037545 entre 12 e 14 bits e 0,028529 entre 14 e 16 bits. São comparações descritivas de distribuições dependentes espacialmente.

A regressão de duas variáveis na Fase 2 reduziu o MAE frente à média do treino, mantendo R² negativo. Na Fase 3, o modelo com deslocamento obteve R² de 0,0398, 0,1216 e 0,1841 em 12, 14 e 16 bits. Em 16 bits, o MAE foi 4,6450 contra 5,4999. A associação é retrospectiva porque o potencial contém os alvos.

Em 12 bits, 2.211 falsos positivos na Fase 2 passaram a 57 após restrição de fase e filtragem na Fase 3. A mudança de 97,42% reúne etapas distintas, enquanto o recall caiu de 98,17% para 59,71%. O híbrido chegou a 99,86% de precisão e 67,49% de recall em 16 bits. Em 18 bits, obteve 99,89% e 69,03%. Pseudoprimos sobrevivem à verificação de uma base. O custo híbrido foi 66,8 vezes o direto em 16 bits e 58,8 vezes em 18 bits.

Os desvios máximos medidos foram 7,28e-11 no gradiente escalar, 2,05e-12 no gradiente tensorial e 1,40e-9 na segunda derivada tensorial. O limite de 1e-10 descreve os gradientes medidos. As tabelas completas estão no [artigo consolidado](ARTIGO_TECNICO.md).
