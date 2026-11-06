# Fase 2: Background Detrending & Blind Wave Sieve



## Protocolo e limites



O fundo usa somente horizonte, epsilon e densidade P/log(uP). Integração adaptativa seguida de spline cúbica em 2049 pontos globais e refinamento local nas bordas; comparação com 1025 pontos globais registra sensibilidade do gradiente. A derivada da spline é uma aproximação da derivada do integral. A densidade assintótica é uma escolha de modelo, especialmente aproximada perto de 2.

O detrending ainda usa todos os primos em L. A regressão combina log(lambda) e log(abs(H)) da barreira, com intervalos pareados antes/depois, treino espacial superior de 70%, um intervalo de embargo e teste inferior. Portanto, não é uma previsão cega. Ganho em MAE e R² positivo são critérios distintos.

A onda recebe somente o horizonte e a base até sua raiz quadrada. O horizonte é informado e sua primalidade não é descoberta. O scanner percorre brackets do gradiente em ordem decrescente e refina mínimos com Brent; trata-se de enumeração de pontos estacionários, não de uma trajetória de descida com momento. Candidatos são inteiros arredondados, sem filtro de divisibilidade e sem consulta à verdade. Toda a lista de primos do intervalo é usada apenas pelo avaliador.

A resolução da onda foi comparada entre passos 0,05 e 0,025. Isso não prova completude: extremos muito próximos podem escapar. Epsilon finito limita a altura das barreiras; não há garantia de que um primo seja mínimo nem de que arredondar um mínimo evite compostos.

O holdout remove aproximadamente 10% dos primos internos com semente 42 e preserva o horizonte. Registra raízes antes/depois, deslocamentos dos mínimos associados e Hessianas. Um diagnóstico simples propõe o ponto médio de gaps retidos maiores que duas vezes a mediana. Este controle usa apenas a base retida; a lista removida é usada para pontuação exata. Não é um estimador otimizado de coordenadas via Hessianas. Os catálogos permitem analisar mudanças de limites das bacias.

Os gráficos e catálogos de raízes usam malha global e amostras locais na escala de epsilon. A fase 2 não fornece certificação de completude dos catálogos residuais. Não foi isolado o efeito individual de lambda versus Hessiana nesta regressão conjunta.



## Resultados por escala



### 6 bits

Base pequena: [2, 3, 5, 7]. Horizonte: 61.

Onda cega: precisão 0.3611; recall 0.9286; F1 0.5200. TP=13, FP=23, FN=1. Candidatos estáveis sob refinamento: True.

Regressão antes: MAE 2.5747, R² -5.7099. Depois: MAE 1.6778, R² -1.7412. Baseline: MAE 1.9318. Treino/teste: 11/4.

Sensibilidade máxima do gradiente de fundo (1025/2049 pontos): 0.000742922.

Holdout: 2 removidos; acertos exatos=0, falsos positivos=0, não recuperados=2; F1=0.0000.



### 8 bits

Base pequena: [2, 3, 5, 7, 11, 13]. Horizonte: 251.

Onda cega: precisão 0.3038; recall 1.0000; F1 0.4660. TP=48, FP=110, FN=0. Candidatos estáveis sob refinamento: True.

Regressão antes: MAE 3.5802, R² -5.0175. Depois: MAE 1.9832, R² -0.9590. Baseline: MAE 2.0333. Treino/teste: 36/15.

Sensibilidade máxima do gradiente de fundo (1025/2049 pontos): 0.00389996.

Holdout: 5 removidos; acertos exatos=0, falsos positivos=8, não recuperados=5; F1=0.0000.



### 10 bits

Base pequena: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]. Horizonte: 1021.

Onda cega: precisão 0.2355; recall 0.9814; F1 0.3798. TP=158, FP=513, FN=3. Candidatos estáveis sob refinamento: True.

Regressão antes: MAE 4.3860, R² -1.7359. Depois: MAE 2.7106, R² -0.1737. Baseline: MAE 2.9831. Treino/teste: 118/51.

Sensibilidade máxima do gradiente de fundo (1025/2049 pontos): 0.0237357.

Holdout: 17 removidos; acertos exatos=0, falsos positivos=14, não recuperados=17; F1=0.0000.



### 12 bits

Base pequena: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61]. Horizonte: 4093.

Onda cega: precisão 0.1951; recall 0.9817; F1 0.3255. TP=536, FP=2211, FN=10. Candidatos estáveis sob refinamento: True.

Regressão antes: MAE 5.3309, R² -1.8164. Depois: MAE 3.0214, R² -0.0435. Baseline: MAE 3.4578. Treino/teste: 393/168.

Sensibilidade máxima do gradiente de fundo (1025/2049 pontos): 0.0232745.

Holdout: 56 removidos; acertos exatos=0, falsos positivos=79, não recuperados=56; F1=0.0000.



## Conclusões iniciais



A remoção do fundo melhora o erro médio em relação à média de treino nas quatro escalas avaliadas, mas não atinge R² positivo. Esse resultado não demonstra que a deriva de borda era a única causa da baixa previsão.

A onda é cega em relação aos primos interiores, mas os mínimos arredondados não formam um crivo preciso. A alta recuperação vem acompanhada de muitos falsos positivos. Testes modulares poderiam eliminar compostos, mas mudariam o método para um crivo clássico; não foram usados para melhorar as métricas.

O holdout mede perturbações e avalia uma regra explícita de recuperação. Comparar com o campo completo serve como diagnóstico retrospectivo, não como informação disponível a um detector cego. Não se conclui identificação única de primos ocultos a partir da geometria.



## Reprodução



Executar python -m omegagrad.phase2 e python build_results_pdf.py --phase2. Resultados completos em outputs/phase2/results.json e arquivos por escala. Os CSV registram deslocamentos e Hessianas dos pontos associados. Testes: python -m pytest -q.