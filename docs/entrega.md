# Guia de entrega

A implementação, as duas execuções, os relatórios HTML/JSON, o resumo e a versão final do PDF estão prontos. O PDF inclui a identificação e as três capturas reais fornecidas pelo aluno, sem avisos de revisão ou espaços reservados.

## 1. Revisar a análise e combinar o critério da meta

Leia `docs/analise.md` e a versão final em `output/pdf/relatorio-mutacao.pdf`.

O enunciado exige score **superior a 98%**. O score bruto obtido é **97,65%**, com cinco mutantes equivalentes documentados. O score ajustado complementar é 100%; ele não substitui o score bruto. Confirme com o professor se a justificativa dos equivalentes atende à meta. Caso ele exija literalmente mais de 98% no HTML, pergunte se autoriza desativar pontualmente os equivalentes comprovados ou refatorar os retornos redundantes. Essas mudanças não foram feitas, para preservar o código base e o conjunto comparado.

## 2. Conferir a capa

A capa já foi preenchida com Matheus Fernandes de Oliveira, matrícula 773220. Os dados estão em `docs/identificacao.json`. Confira também o nome da disciplina, a data e o link do repositório. O remote atual aponta para `https://github.com/matheus-0063/operacoes-mutante`; confirme que é o seu fork correto.

## 3. Conferir as capturas incluídas

As capturas incluídas, relacionadas em `docs/capturas/README.md`, são:

- `docs/capturas/line_104.png`: mutante 177, comparação `>` → `>=`.
- `docs/capturas/line_109.png`: mutante 193, remoção da ordenação da mediana.
- `docs/capturas/line_93.png`: mutante 156, fator de conversão Celsius/Fahrenheit.

As alterações capturadas correspondem a mutantes com estado **Survived** no relatório inicial e **Killed** no relatório final.

## 4. Gerar e conferir o PDF preenchido

Se `python3` já tiver ReportLab instalado:

```bash
npm run relatorio
```

Caso contrário, na raiz do projeto:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-relatorio.txt
.venv/bin/python scripts/gerar-relatorio.py
```

O resultado fica em `output/pdf/relatorio-mutacao.pdf`. O gerador inclui as capturas disponíveis e omite as ausentes, sem espaços reservados. Ao acrescentar imagens, confira a legibilidade e confirme que o documento continua com 2 a 4 páginas. O texto é editável em `scripts/gerar-relatorio.py`.

## 5. Publicar a implementação no seu fork

Confira as alterações e aponte para seu fork antes de publicar:

```bash
git remote -v
git status --short
git diff
npm test
```

Para publicar futuras alterações após a revisão, faça o commit e o push:

```bash
git add .gitignore README.md package.json package-lock.json jest.config.cjs stryker.conf.json stryker.inicial.conf.cjs test/operacoes.aprimoradas.test.js scripts docs reports output/pdf/relatorio-mutacao.pdf requirements-relatorio.txt
git commit -m "Aprimora testes e documenta análise de mutação"
git push origin main
```

O PDF está incluído no repositório e também deve ser anexado à entrega pelo portal da disciplina. Após o push, confira se os novos testes, a configuração e as evidências estão presentes. Se sua branch não for `main`, ajuste o último comando para sua branch.

## 6. Entregar

- Link do seu fork com a suíte aprimorada publicada.
- PDF final de 2 a 4 páginas, com identificação preenchida e as três capturas reais.
- Justificativa dos mutantes equivalentes conforme a orientação recebida do professor.

Revise o texto para garantir que você entende e consegue explicar as entradas escolhidas, as fraquezas dos testes originais e a diferença entre cobertura e eficácia.
