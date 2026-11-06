# Reutilização dos componentes numéricos

**Richard Ikeda — Autor e pesquisador principal**

Instale o pacote e rode os módulos a partir da raiz. Cada exemplo verifica seu resultado por comparação com uma solução analítica.

| Comando | Aplicação |
|---|---|
| python -m examples.scalar_optimization | Descida de gradiente em energia quadrática |
| python -m examples.tensor_derivatives | Gradiente e curvatura de energias independentes em lote |
| python -m examples.background_subtraction | Subtração de fundo por spline em um sinal espacial |
| python -m examples.stationary_landscape | Extremos e bacias de uma energia de dois poços |

## Derivadas

Value oferece operações aritméticas, potências reais, seno, cosseno, log e exp. Cada chamada de backward zera os gradientes do grafo alcançável e soma as contribuições dos nós compartilhados. Reconstrua o grafo a cada novo passo de otimização e mantenha os valores fixos entre a avaliação e a retropropagação.

TensorValue aceita broadcasting nas operações implementadas. Com direção v, propaga a tangente e d²f(x+t·v)/dt². A chamada sum().backward() diferencia a soma das saídas. Para coordenadas escalares independentes e direções unitárias, a segunda derivada fornece a curvatura local. Em saídas acopladas, ela é uma contração direcional. Divida matrizes grandes em blocos e valide domínios, formas e derivadas.

## Subtração de fundo

Residual aceita objetos que implementem field(z, derivative=0|1|2). O exemplo adapta uma CubicSpline de deriva quadrática e recupera uma senoide com suas duas primeiras derivadas. Background implementa o integral específico da densidade prima. Em outras aplicações, use um modelo de fundo motivado pelo problema e compare resoluções. Ajustar o fundo aos próprios dados pode apagar parte do sinal ou incorporar informação dos alvos.

## Extremos e bacias

O exemplo usa roots de omegagrad.phase2. A malha é avaliada em lote e cada mudança de sinal é refinada por Brent escalar. Para um ToyUniverse, stationary_points em omegagrad.omegasieve também amostra vizinhanças dos primos e aplica uma correção de Newton com salvaguarda. A função geometry retorna as bacias e compara resoluções. A bisseção em lote da Fase 3 é uma rotina separada.

Refine a malha, compare catálogos e registre raízes degeneradas ou intervalos ausentes. Em uma dimensão, máximos delimitam as bacias do fluxo de gradiente. Momento e ruído alteram a dinâmica.

[Citação](../../CITATION.cff) · [Código dos exemplos](../../examples/README.md)
