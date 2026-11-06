# OMEGAGRAD

**A Differentiable Top-Down Framework for Cosmological Finite Arithmetic**

Laboratório aberto de computação científica para investigar a geometria de conjuntos finitos de primos por meio de potenciais diferenciáveis. O algoritmo **OmegaSieve** percorre o campo do horizonte superior até a base, registrando atratores, barreiras e trajetórias.

O objetivo é testar hipóteses sobre assimetria e estabilidade de escala com dados reproduzíveis. O campo é construído a partir de primos conhecidos: este projeto **não apresenta um algoritmo para descobrir primos desconhecidos**, nem demonstra uma teoria física cosmológica.

![Comparação experimental](outputs/first_run/comparison.png)

## Resultados iniciais

| Bits | Horizonte | Primos | Mínimos: epsilon fixo | Mínimos: epsilon escalado |
|---:|---:|---:|---:|---:|
| 6 | 61 | 18 | 18 | 18 |
| 8 | 251 | 54 | 53 | 54 |
| 10 | 1021 | 172 | 110 | 172 |
| 12 | 4093 | 564 | 74 | 564 |

- O controle de suavização recuperou todos os primos conhecidos nas três sementes de cada escala, com escape externo controlado entre poços.
- A largura relativa mediana das bacias foi 1,012, 1,020 e 1,022 em 8, 10 e 12 bits. A semelhança é descritiva; não prova invariância.
- Em 12 bits, o modelo linear de log(lambda) apresentou MAE 5,32; a média do treino apresentou MAE 3,46. Não houve ganho preditivo neste protocolo.
- 23 testes passaram na validação inicial. O erro máximo AD versus analítico foi 7,28e-11.

## Instalação e execução

Python 3.10 ou superior. A execução de referência usou Python 3.12.13.

```bash
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# PowerShell: .venv/Scripts/Activate.ps1
python -m pip install -e ".[test,report]"
python -m pytest -q
python -m omegagrad.experiments
python build_results_pdf.py
```

Para reproduzir as versões utilizadas: `python -m pip install -r requirements-lock.txt`, seguido de `python -m pip install -e ".[test,report]"`.

Para executar a navegação diretamente com autograd:

```bash
python -m omegagrad.experiments --bits 6 --modes fixed --seeds 0 --backend autograd --output outputs/autograd_validation
```

A execução padrão grava em `outputs/first_run`, substituindo os resultados anteriores. Use `--output outputs/my_run` para preservar o conjunto de referência. A geração do PDF usa os diretórios de referência.

## Documentação

- [Fundamentação e escolhas de modelagem](docs/THEORY.md)
- [Métodos, métricas e controles](docs/METHODOLOGY.md)
- [Conclusões iniciais e limites](docs/INITIAL_FINDINGS.md)
- [Arquitetura e reprodução](docs/REPRODUCIBILITY.md)
- [Dicionário dos dados](docs/DATA_DICTIONARY.md)
- [Relatório completo](outputs/first_run/REPORT.md)
- [PDF com resultados e gráficos](output/pdf/OMEGAGRAD_Resultados_Completos.pdf)
- [Como contribuir](CONTRIBUTING.md)

## Organização

`omegagrad/`: implementação; `tests/`: verificações numéricas; `docs/`: estudo; `outputs/`: dados e figuras de referência; `output/pdf/`: relatório; `build_results_pdf.py`: gerador do relatório.

## Licença

Código, documentação e resultados publicados sob [MIT](LICENSE). Trabalho experimental de Richard Ikeda. Contribuições devem preservar a distinção entre medição, hipótese e demonstração.
