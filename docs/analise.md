# Análise das execuções

## Método e rastreabilidade

O código de produção e o arquivo `test/operacoes.test.js` foram preservados. O ajuste de CommonJS no `package.json` acompanha o formato que esses arquivos já usavam; não muda o comportamento das funções. A configuração inicial limita o Jest ao arquivo original, enquanto a final inclui também `test/operacoes.aprimoradas.test.js`.

Foram executadas ambas as fases com StrykerJS 9.6.1, Jest 29.7.0 e Node 24.8.0. Os conjuntos têm as mesmas 213 mutações, sem exclusão de operadores ou trechos. `scripts/resumir-resultados.cjs` exige que as fontes e as identidades dos mutantes sejam iguais e interrompe a consolidação se encontrar resultados não analisados. O SHA-256 da fonte é registrado em `reports/resumo.json`.

## Cobertura e eficácia

Os 50 testes originais aprovados cobriam 73 de 74 linhas (98,64%), 82 de 96 instruções (85,41%), 53 de 53 funções instrumentadas (100%) e 20 de 34 ramificações (58,82%). O total de 53 funções da cobertura inclui as funções de callback além das 50 operações exportadas.

A execução inicial identificou 154 mutantes mortos, 3 com timeout, 44 sobreviventes e 12 sem cobertura. O score é `(154 + 3) / 213 × 100 = 73,71%`. A discrepância entre as métricas indica entradas e asserções insuficientes: executar a função não basta para diferenciar a implementação correta de uma alteração defeituosa.

## Três mutantes sobreviventes da execução inicial

| ID / linha | Alteração | Por que sobreviveu | Caso adicionado | Evidência final |
| --- | --- | --- | --- | --- |
| 177 / 104 | `a > b` → `a >= b` | O teste usava `(10, 5)`; ambas as comparações retornam `true`. | `isMaiorQue(5, 5)` deve retornar `false`; o mutante retorna `true`. | `Killed`, teste 81 no JSON final. |
| 193 / 109 | Remoção de `.sort((a, b) => a - b)` | O array inicial já estava ordenado. | `medianaArray([3, 1, 2])` deve retornar 2; o mutante retorna 1. | `Killed`, teste 97 no JSON final. |
| 156 / 93 | `celsius * 9 / 5` → `celsius / 9 / 5` | Com 0 °C, tanto a multiplicação quanto a divisão produzem zero. | `celsiusParaFahrenheit(100)` deve retornar 212; o mutante retorna aproximadamente 34,22. | `Killed`, teste 91 no JSON final. |

Os IDs dos testes são os registrados nesta execução pelo Stryker, não números escritos nos títulos dos casos. Os três exemplos podem ser conferidos nos dois relatórios JSON e HTML. As capturas fornecidas pelo aluno foram incluídas no PDF; os arquivos correspondentes estão relacionados em `docs/capturas/README.md`.

## Outros casos acrescentados

A suíte complementar inclui mensagens de erro específicas, raízes e fatoriais nas fronteiras, arrays vazios, resultados booleanos falsos, números não primos, comparações iguais e invertidas, ambos os limites de `clamp`, conversões com entradas não nulas e medianas de arrays pares, desordenados, negativos e com valores de dois dígitos. As medianas também preservam o array de entrada.

As mensagens originais de máximo, mínimo e mediana contêm os caracteres `не`. Os testes verificam as mensagens existentes; não houve correção do texto de produção durante a comparação.

Os dois mutantes de fronteira de `clamp` (142 e 146) parecem equivalentes para zeros sem distinção de sinal, mas não são equivalentes para todos os valores `Number`: `clamp(+0, -0, 1)` e `clamp(-0, -1, +0)` devem preservar o zero recebido. `Object.is`, usado por `toBe`, distingue `+0` de `-0`; isso também afeta `1 / x`. Esses casos mataram as trocas `<` → `<=` e `>` → `>=`.

## Resultados finais

Com 55 casos adicionais, os 105 testes passam e a cobertura chega a 100% nas quatro métricas. A execução final contabiliza 205 mutantes mortos, 3 com timeout, 5 sobreviventes e 0 sem cobertura. O score bruto é `(205 + 3) / 213 × 100 = 97,65%`, uma evolução de 23,94 pontos percentuais. Timeout é uma detecção do Stryker, mas não uma falha de asserção; por isso foi discriminado nas contagens.

## Justificativa dos cinco equivalentes restantes

Os domínios considerados são inteiros não negativos para fatorial e arrays comuns de números, com `reduce` padrão, para produto. Não são usados objetos com coerção de tipos que muda a cada chamada, nem métodos de array substituídos para distinguir mutações de fluxo sem diferença no uso normal da biblioteca.

| IDs | Mutação | Justificativa |
| --- | --- | --- |
| 28 | Condição completa do retorno antecipado do fatorial substituída por `false`. | Para 0 e 1, o acumulador começa em 1 e o laço `i = 2; i <= n` não executa. O retorno continua sendo 1. Para `n >= 2`, o caminho já era o mesmo. |
| 29 | `n === 0 || n === 1` substituído por `n === 0 && n === 1`. | A condição é sempre falsa; aplica-se a mesma prova de 28. |
| 30 | Somente `n === 0` substituído por `false`. | Para 0, o laço não executa e retorna 1; para 1, o outro termo ainda dá o retorno antecipado. Os demais casos não mudam. |
| 32 | Somente `n === 1` substituído por `false`. | Para 1, o laço não executa e retorna 1; para 0, o outro termo ainda dá o retorno antecipado. Os demais casos não mudam. |
| 135 | Condição de retorno antecipado de `produtoArray([])` substituída por `false`. | `[].reduce((acc, val) => acc * val, 1)` já retorna 1. Arrays não vazios já executavam essa mesma redução. |

O consolidador constrói cada uma dessas versões usando as posições reais do relatório e compara os resultados com o original. São verificadas 171 entradas (0 a 170) para cada mutante de fatorial e seis arrays para o produto. As amostras apoiam a análise, mas a prova de equivalência se baseia no fluxo descrito acima.

O score complementar sem os cinco equivalentes é `208 / (213 - 5) × 100 = 100%`. Esse cálculo é uma **análise manual ajustada**; o relatório oficial continua mostrando **97,65%**. A meta bruta superior a 98% do enunciado não foi atingida. No domínio considerado, mantendo o código e o conjunto de mutantes, novos testes de comportamento não eliminam esses cinco casos. O tratamento desses equivalentes precisa ser validado com o professor.

## Conclusão

A cobertura identifica o que foi executado; o teste de mutação ajuda a avaliar o que foi efetivamente verificado. A melhoria veio de casos que expõem diferenças observáveis em erros, limites, cálculos e ordenação. Os sobreviventes também exigem análise crítica: alguns representam lacunas, enquanto outros mantêm a mesma semântica no domínio relevante. Relatar os valores brutos, os timeouts e as equivalências mantém a comparação verificável.
