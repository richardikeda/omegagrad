# Arquitetura e reprodução

## Componentes e responsabilidades

- `engine.py`: Value escalar com operações reais, sin, cos, log, exp e potências; backprop iterativo evita limite de recursão. Cada backward zera o grafo alcançável. Não mutar valores entre forward e backward.
- `universe.py`: crivo de Eratóstenes, normalização, L e W; avaliações NumPy em blocos e Hessiano analítico. Suporta S_bits de 2 a 20, sujeito aos limites de memória e malha.
- `omegasieve.py`: catálogo numérico de pontos estacionários, bacias e navegador. O Hessiano é analítico; o motor não constrói grafos de derivadas superiores.
- `experiments.py`: configuração, diagnósticos, regressões, gráficos e exportação.
- `build_results_pdf.py`: relatório de referência em PDF usando dados já calculados.

## Ambiente e auditoria

`requirements-lock.txt` registra versões de dependências do ambiente de publicação. O JSON mantém as versões efetivas de Python, NumPy, SciPy e Matplotlib da execução, parâmetros, sementes e hashes SHA-256 dos módulos. Resultados float64 podem apresentar diferenças pequenas entre plataformas; tempo de execução não é benchmark controlado.

Cada avaliação do campo custa O(n) no número de primos. O crivo e a construção da base fazem parte do custo, e não podem ser omitidos em comparações com algoritmos de primalidade.

Os testes confrontam AD com diferenças finitas e fórmulas analíticas, verificam grafos compartilhados e longos, domínios inválidos, onda, horizontes, partição das bacias, refinamento e repetibilidade das trajetórias.

## Histórico técnico inicial

A primeira navegação usava um passo excessivamente conservador em regiões planas. Foi substituída por adaptação à curvatura com limitação e backtracking. A malha inicial de 12 bits perdeu um par de raízes próximo; o refinamento automático e um teste de regressão foram adicionados. A bateria publicada foi executada após essas correções.

A integração contínua executa os testes; os resultados de referência são artefatos experimentais versionados. Alterações científicas devem gerar uma nova pasta de resultados e registrar diferenças de protocolo.
