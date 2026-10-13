# Análise de eficácia de testes com StrykerJS

Laboratório de Testes de Software com 50 operações matemáticas, Jest e StrykerJS. A biblioteca e os 50 testes iniciais foram preservados. A suíte complementar adiciona 55 casos orientados pelos mutantes da execução inicial.

## Resultados medidos em 13/10/2026

| Indicador | Inicial | Final |
| --- | ---: | ---: |
| Testes aprovados | 50 | 105 |
| Cobertura de linhas | 98,64% | 100% |
| Cobertura de instruções | 85,41% | 100% |
| Cobertura de ramificações | 58,82% | 100% |
| Cobertura de funções | 100% | 100% |
| Pontuação de mutação **bruta** | 73,71% | **97,65%** |
| Mutantes mortos / timeout | 154 / 3 | 205 / 3 |
| Mutantes sobreviventes / sem cobertura | 44 / 12 | 5 / 0 |

**A meta bruta superior a 98% ainda não foi atingida.** Os cinco sobreviventes finais são equivalentes no domínio usual das funções: quatro tornam redundante o retorno antecipado de `fatorial(0)` e `fatorial(1)`, e um remove o retorno antecipado do produto de um array vazio, cujo `reduce` já retorna 1. A justificativa está em [docs/analise.md](docs/analise.md).

O cálculo complementar descontando esses equivalentes é 100%. Ele **não substitui** o resultado de 97,65% mostrado pelo Stryker. Nenhuma mutação foi excluída; o mesmo código e os mesmos 213 mutantes foram utilizados antes e depois. A aceitação desse tratamento deve ser confirmada com o professor.

## Instalação e reprodução

Requisitos: Node.js 20 ou superior e npm. Validado com Node 24.8.0, Jest 29.7.0 e StrykerJS 9.6.1. O `package-lock.json` faz parte do projeto.

```bash
npm ci
npm run analisar
```

O comando `analisar` executa cobertura e mutação da suíte inicial, cobertura e mutação da suíte completa e a consolidação dos resultados. As etapas também podem ser executadas individualmente:

```bash
npm run test:inicial
npm run coverage:inicial
npm run mutate:inicial
npm test
npm run coverage
npm run mutate
npm run resultados
```

| Evidência | Caminho |
| --- | --- |
| Mutação inicial, HTML e JSON | `reports/mutation/inicial/` |
| Mutação final, HTML e JSON | `reports/mutation/final/` |
| Resumo, contagens e análise de equivalentes | `reports/resumo.json` |
| Cobertura inicial e final, após executar | `coverage/inicial/` e `coverage/final/` |
| Testes iniciais preservados | `test/operacoes.test.js` |
| Casos adicionados | `test/operacoes.aprimoradas.test.js` |

Abra `mutation.html` no seu navegador para navegar pelos detalhes. A configuração usa `coverageAnalysis: perTest` e aplica mutações somente a `src/operacoes.js`. O valor `thresholds.high: 98` sinaliza a meta; `break: 0` permite gerar as evidências mesmo quando a meta não é atingida. `npm run resultados` informa explicitamente o cumprimento ou não da meta.

O pacote foi configurado como CommonJS porque fonte e testes já utilizavam `module.exports` e `require`. A configuração do Jest foi concentrada em `jest.config.cjs`; não há alteração na lógica das operações. Stryker 9.6.1 foi fixado para ser compatível com o Node instalado.

## Relatório escrito

A versão final está em `output/pdf/relatorio-mutacao.pdf`, com quatro páginas, identificação preenchida e as três capturas reais fornecidas pelo aluno. Conforme solicitado, o documento não contém avisos de revisão nem espaços reservados para imagens.

1. Confira os dados preenchidos em `docs/identificacao.json`.
2. Confira em [docs/capturas/README.md](docs/capturas/README.md) a correspondência das capturas dos mutantes 177, 193 e 156.
3. Instale a dependência de geração do PDF e gere a versão preenchida:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-relatorio.txt
.venv/bin/python scripts/gerar-relatorio.py
```

Se `reportlab` já estiver instalado no seu `python3`, basta `npm run relatorio`. O código-fonte editável do relatório é `scripts/gerar-relatorio.py`; os dados vêm de `reports/resumo.json` e `docs/identificacao.json`. O gerador inclui as capturas quando os arquivos estão disponíveis e omite imagens ausentes, sem criar espaços reservados.

Consulte [docs/entrega.md](docs/entrega.md) para concluir o trabalho e fazer o commit/push no seu fork.

Referências: [configuração oficial do StrykerJS](https://stryker-mutator.io/docs/stryker-js/configuration/), [integração com Jest](https://stryker-mutator.io/docs/stryker-js/jest-runner/) e [operadores de mutação](https://stryker-mutator.io/docs/mutation-testing-elements/supported-mutators/).
