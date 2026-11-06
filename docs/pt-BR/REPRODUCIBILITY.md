# Reprodução e proveniência

**Richard Ikeda — Autor e pesquisador principal**

Instale Python 3.10 ou posterior e execute os comandos na raiz do repositório. O ambiente das campanhas está documentado nos JSONs. O requirements-lock.txt registra um ambiente de referência, sujeito a diferenças de compatibilidade entre versões de Python e plataformas. Resultados em ponto flutuante e tempos podem variar.

```bash
python -m pip install -e ".[test,report]"
python -m pytest -q
python -m omegagrad.experiments --output outputs/reproduction_phase1
python -m omegagrad.experiments --bits 6 --modes fixed --seeds 0 --backend autograd --output outputs/reproduction_autograd
python -m omegagrad.phase2
python -m omegagrad.phase3
python -m omegagrad.phase3_refine
python build_results_pdf.py --phase2
python build_results_pdf.py --phase3
python build_technical_papers.py
```

As Fases 2 e 3 sobrescrevem os diretórios de referência. Use uma cópia separada para reproduzir as campanhas. A geração dos artigos usa os arquivos Markdown e as figuras já publicadas. A integração contínua roda os testes e exemplos em Python 3.10 e 3.12. A geometria estendida tem custo superior ao da suíte de testes.

| Campanha | Commit de referência | Dados |
|---|---|---|
| Fase 1 | 2c828e8 | outputs/first_run e outputs/autograd_validation |
| Fase 2 | dc54a92 | outputs/phase2 |
| Fase 3 | 8579a08 | outputs/phase3 |

Os hashes registram os bytes presentes na execução. Na Fase 1, o JSON também registra hashes após normalização para LF pelo Git. Para reproduzir uma campanha histórica, use seu commit de referência. A edição de arquivo consolida a implementação e a documentação.

A Fase 3 preserva a geometria inicial e a refinada. Na execução refinada, avisos de integração são tratados como erros. A estabilidade sob refinamento sustenta o sinal dos R² observados, dentro do método de busca de raízes usado.

Value calcula derivadas escalares de primeira ordem. TensorValue combina gradientes reversos e segundas derivadas direcionais. Background integra a densidade do modelo e Residual subtrai campos compatíveis. A busca original avalia a malha em lote e refina raízes individualmente. A geometria estendida usa bisseção em lote. Avaliar o potencial completo custa O(número de primos) por coordenada, e o radar conserva etapas escalares em Python.

[Acervo histórico](ARCHIVE.md) · [Exemplos executáveis](REUSE_GUIDE.md)
