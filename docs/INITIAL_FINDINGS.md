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
