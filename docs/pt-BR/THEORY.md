# Fundamentação e escolhas de modelagem

## O que o laboratório representa

Um universo finito é um conjunto de primos limitado por um orçamento operacional `S_bits`. Define-se `P_omega = max {p primo: p <= 2**S_bits}` e `p_hat = p/P_omega`. O maior primo passa a ocupar z=1. Isso permite comparar diferentes conjuntos em um domínio comum.

A palavra cosmológico designa a motivação de um horizonte finito. A implementação não calcula complexidade de Kolmogorov, custo de prova de primalidade ou capacidade física do universo. Um limite de representação em bits não é uma medição termodinâmica.

## Por que um potencial logarítmico

O polinômio U(z)=produto(z-p_hat) contém os pontos conhecidos como raízes, mas produtos extensos apresentam dificuldades de escala numérica. O funcional suavizado é:

```text
L(z) = soma log((z-p_hat_i)^2 + epsilon)
L'(z) = soma 2*d_i/(d_i^2+epsilon)
L''(z) = soma 2*(epsilon-d_i^2)/(d_i^2+epsilon)^2
d_i = z-p_hat_i
```

Epsilon é uma distância normalizada ao quadrado. A largura característica é sqrt(epsilon), não epsilon. O campo depende de todos os primos inseridos. Um mínimo não precisa coincidir com um primo: os outros termos exercem força resultante. Suavização suficientemente grande pode eliminar pares de mínimo e máximo.

Em uma dimensão, as chamadas selas do projeto são máximos locais com L''<0, separando bacias. A geometria é calculada numericamente, sem promessa de localização simbólica exata.

## Onda de divisibilidade

`W(x)=soma sin²(pi*x/p)` é diferenciável. Seus zeros matemáticos são os múltiplos comuns da base, incluindo zero. Portanto, mínimos de W não são, por definição, indicadores de primalidade. A implementação valida valor e gradiente; a bateria principal investiga L.

## Papel da diferenciação automática

O motor escalar registra um grafo de operações e aplica a regra da cadeia em ordem topológica reversa. Isso permite validar derivadas e experimentar outros funcionais. A bateria usa fórmulas analíticas vetorizadas conferidas contra o motor, evitando o custo de reconstruir um grafo escalar a cada avaliação.

## Fundo contínuo e radar

A densidade aproximada P_omega/log(u·P_omega) é integrada de 2/P_omega a 1 contra o núcleo logarítmico. O residual é a diferença entre o potencial completo e esse fundo. O fundo usa horizonte e epsilon, enquanto o potencial completo contém os primos-alvo.

O radar usa U(x)=-soma log(sin²(pi·x/p)+epsilon). Na Fase 3, exclui 2 e 3 da soma e examina células centradas em 6k±1. Trata-se de uma restrição aritmética explícita. A regularização limita a contribuição de termos próximos de zero. Tanto os mínimos deslocados quanto o arredondamento podem gerar candidatos compostos.

## O que permanece em aberto

Sem observáveis independentes dos primos desconhecidos, nenhuma correlação neste campo demonstra previsão cega. Sem controles não primos e mais escalas, semelhança entre distribuições não demonstra uma propriedade exclusiva dos primos.
