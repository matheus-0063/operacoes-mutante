# Capturas para o relatório escrito

As três capturas reais fornecidas pelo aluno foram incluídas no relatório final. A correspondência com os mutantes foi conferida nos relatórios inicial e final do Stryker.

1. Abra `reports/mutation/inicial/mutation.html` no seu navegador local.
2. Entre em `src/operacoes.js` e habilite o filtro **Survived**.
3. Se precisar substituir uma imagem, selecione o mutante e capture seu detalhe, incluindo a alteração e o estado **Survived**:

| Mutante | Linha | Alteração | Arquivo neste diretório |
| --- | --- | --- | --- |
| 177 | 104 | `a > b` para `a >= b` | `line_104.png` |
| 193 | 109 | remoção de `.sort((a, b) => a - b)` | `line_109.png` |
| 156 | 93 | `celsius * 9 / 5` para `celsius / 9 / 5` | `line_93.png` |

No macOS, use `Cmd + Shift + 4`, capture a região e renomeie o PNG. Prefira uma captura horizontal, com texto legível, sem a área de trabalho inteira.

Execute `npm run relatorio` para gerar novamente o PDF com essas imagens. O gerador insere cada captura no caso correspondente e não inclui avisos de revisão nem espaços reservados.
