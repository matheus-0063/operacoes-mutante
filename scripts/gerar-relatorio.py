"""Gera um relatório de quatro páginas com dados reais e capturas opcionais.

Dependência: python3 -m pip install reportlab
Identificação: docs/identificacao.json. Evidências: reports/resumo.json.
"""

import json
from pathlib import Path
from xml.sax.saxutils import escape

try:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.utils import ImageReader
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
        Image, Preformatted, KeepTogether,
    )
except ModuleNotFoundError as exc:
    raise SystemExit('Instale a dependência: python3 -m pip install reportlab') from exc

ROOT = Path(__file__).resolve().parent.parent
resumo = json.loads((ROOT / 'reports/resumo.json').read_text())
identificacao = json.loads((ROOT / 'docs/identificacao.json').read_text())
DESTINO = ROOT / 'output/pdf/relatorio-mutacao.pdf'
DESTINO.parent.mkdir(parents=True, exist_ok=True)
for campo in ('nome', 'matricula'):
    if not identificacao[campo].strip() or '[PREENCHER' in identificacao[campo]:
        raise SystemExit(f'Preencha o campo {campo} em docs/identificacao.json.')
azul = colors.HexColor('#17324D')
cinza = colors.HexColor('#526273')
claro = colors.HexColor('#F1F5F8')
styles = getSampleStyleSheet()
styles.add(ParagraphStyle('Texto', fontName='Helvetica', fontSize=10, leading=14, spaceAfter=7))
styles.add(ParagraphStyle('Secao', fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=azul, spaceBefore=10, spaceAfter=8))
styles.add(ParagraphStyle('Caso', fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=azul, spaceBefore=8, spaceAfter=6))
styles.add(ParagraphStyle('Nota', fontName='Helvetica', fontSize=8, leading=11, textColor=cinza, spaceAfter=5))
styles.add(ParagraphStyle('Codigo', fontName='Courier', fontSize=8.5, leading=11, backColor=claro, borderPadding=6, spaceAfter=9))
styles.add(ParagraphStyle('Capa', fontName='Helvetica-Bold', fontSize=25, leading=31, textColor=azul, alignment=TA_CENTER, spaceAfter=18))
styles.add(ParagraphStyle('Centro', fontName='Helvetica', fontSize=12, leading=19, alignment=TA_CENTER, spaceAfter=12))
styles.add(ParagraphStyle('Celula', fontName='Helvetica', fontSize=9, leading=12))

story = []
largura = A4[0] - 100
capturas = {
    '177': 'line_104.png',
    '193': 'line_109.png',
    '156': 'line_93.png',
}


def par(text, style='Texto'):
    return Paragraph(text, styles[style])


def add(text, style='Texto'):
    story.append(par(text, style))


def pct(valor):
    return f'{valor:.2f}%'.replace('.', ',')


def tabela(linhas, colunas):
    data = [[par(escape(str(c)), 'Celula') for c in row] for row in linhas]
    table = Table(data, colWidths=colunas, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), claro),
        ('TEXTCOLOR', (0, 0), (-1, 0), azul),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('LINEBELOW', (0, 0), (-1, 0), 0.7, azul),
        ('LINEBELOW', (0, 1), (-1, -1), 0.25, colors.HexColor('#D6DFE6')),
    ]))
    story.append(table)
    story.append(Spacer(1, 8))


def captura(mutante):
    caminho = ROOT / 'docs/capturas' / capturas[mutante]
    if not caminho.is_file():
        return
    w, h = ImageReader(str(caminho)).getSize()
    escala = min(largura / w, 132 / h)
    img = Image(str(caminho), width=w * escala, height=h * escala)
    story.append(KeepTogether([img, par(f'Figura: detalhe do mutante {mutante} no relatório inicial do Stryker.', 'Nota')]))
    story.append(Spacer(1, 8))


# Página 1: capa com identificação editável.
story.append(Spacer(1, 66))
add(escape(identificacao['disciplina']), 'Centro')
add('Análise de Eficácia de Testes<br/>com Teste de Mutação', 'Capa')
add('Biblioteca de operações matemáticas<br/>Jest e StrykerJS', 'Centro')
story.append(Spacer(1, 46))
for campo, rotulo in [('nome', 'Aluno'), ('matricula', 'Matrícula')]:
    valor = identificacao[campo]
    add(f'<b>{rotulo}:</b> {escape(valor)}', 'Centro')
story.append(Spacer(1, 30))
add(f'Repositório:<br/><link href="{escape(identificacao["repositorio"])}" color="#17324D">'
    f'{escape(identificacao["repositorio"])}</link>', 'Centro')
add(escape(identificacao['data']), 'Centro')
story.append(PageBreak())

# Página 2: resultados iniciais e primeiro mutante.
add('1. Análise inicial e método', 'Secao')
add('O experimento utiliza as 50 operações do projeto base. A suíte original foi preservada; '
    '55 novos casos foram adicionados em um arquivo complementar. O código de produção permaneceu igual '
    'nas duas execuções e foram avaliados os mesmos 213 mutantes, sem exclusões de operadores.')
ini = resumo['inicial']
fim = resumo['final']
tabela([
    ['Indicador', 'Inicial', 'Final'],
    ['Testes aprovados', ini['testes'], fim['testes']],
    ['Cobertura de linhas', pct(ini['cobertura']['lines']['pct']), pct(fim['cobertura']['lines']['pct'])],
    ['Cobertura de instruções', pct(ini['cobertura']['statements']['pct']), pct(fim['cobertura']['statements']['pct'])],
    ['Cobertura de ramificações', pct(ini['cobertura']['branches']['pct']), pct(fim['cobertura']['branches']['pct'])],
    ['Cobertura de funções', pct(ini['cobertura']['functions']['pct']), pct(fim['cobertura']['functions']['pct'])],
    ['Pontuação de mutação bruta', pct(ini['mutacao']['score']), pct(fim['mutacao']['score'])],
], [largura * .52, largura * .24, largura * .24])
add('A cobertura inicial de linhas era alta, mas a suíte deixou 44 mutantes sobreviventes e 12 sem cobertura. '
    'Executar uma linha não comprova a eficácia da asserção: as entradas originais omitiam fronteiras, '
    'resultados falsos, arrays vazios e valores que revelam erros de cálculo.')
add(f'Ambiente: Node {resumo["ambiente"]["node"]}, Jest {resumo["ambiente"]["jest"]} e '
    f'StrykerJS {resumo["ambiente"]["stryker"]}. Comandos: npm run coverage:inicial, '
    'npm run mutate:inicial, npm run coverage e npm run mutate. O módulo foi configurado como CommonJS, '
    'conforme require/module.exports já utilizados pelo código.', 'Nota')
add('2. Mutantes críticos e soluções', 'Secao')
add('Caso 1 - Mutante 177: comparação na igualdade', 'Caso')
add('Na linha 104, <b>a &gt; b</b> foi substituído por <b>a &gt;= b</b>. O teste inicial usava '
    '(10, 5), que resulta em true nas duas versões. Faltava verificar a fronteira a === b.')
story.append(Preformatted('expect(op.isMaiorQue(5, 5)).toBe(false);', styles['Codigo']))
add('O novo caso produz false no original e true no mutante. O relatório final registra '
    '<b>Killed</b> para o mesmo mutante que inicialmente tinha estado <b>Survived</b>.')
captura('177')
story.append(PageBreak())

# Página 3: outros dois exemplos e estratégia dos novos testes.
add('Caso 2 - Mutante 193: mediana sem ordenação', 'Secao')
add('Na linha 109, foi removida a chamada <b>.sort((a, b) =&gt; a - b)</b>. O teste original '
    'fornecia [1, 2, 3, 4, 5], que já estava ordenado. A posição central continuava correta '
    'mesmo quando o algoritmo ignorava a ordenação.')
story.append(Preformatted('expect(op.medianaArray([3, 1, 2])).toBe(2);\nexpect(op.medianaArray([9, 1, 5, 3])).toBe(4);', styles['Codigo']))
add('A entrada desordenada [3, 1, 2] tem mediana 2, mas o mutante retorna 1. O segundo '
    'caso cobre a média dos dois elementos centrais de um array par. Outros casos verificam '
    'ordenação numérica, valores negativos e preservação do array original. Estado final: <b>Killed</b>.')
captura('193')
add('Caso 3 - Mutante 156: fator de conversão oculto pelo zero', 'Secao')
add('Na linha 93, <b>celsius * 9 / 5</b> passou a <b>celsius / 9 / 5</b>. '
    'O teste original usava 0 °C: o termo multiplicativo permanece zero e ambas as versões retornam 32 °F.')
story.append(Preformatted('expect(op.celsiusParaFahrenheit(100))\n  .toBeCloseTo(212, 10);', styles['Codigo']))
add('Com 100 °C, o resultado correto é 212 °F e o mutante retorna aproximadamente 34,22 °F. A entrada torna '
    'o fator de conversão observável. Foram acrescentados 25 °C, -40 °C e casos não nulos '
    'na conversão inversa. Estado final: <b>Killed</b>.')
captura('156')
add('Estratégia dos novos casos de teste', 'Caso')
add('Além dos três exemplos, a suíte complementar verifica mensagens específicas de erro, '
    'arrays vazios, resultados booleanos falsos, números compostos e valores nas fronteiras '
    'das comparações. Para a mediana, foram usados arrays pares e ímpares, valores negativos '
    'e números de dois dígitos, com asserção de que a entrada permanece inalterada.')
add('Os valores esperados foram definidos a partir do comportamento matemático e do contrato '
    'das operações. Em conversões com ponto flutuante, toBeCloseTo usa precisão de dez casas; '
    'nos demais exemplos, toBe exige o resultado específico. Isso permite identificar '
    'alterações que a execução de uma única entrada nominal não revelava.')
story.append(PageBreak())

# Página 4: resultado bruto, equivalências, reflexão e referências.
add('3. Resultados finais e limitação da meta', 'Secao')
add(f'A pontuação bruta passou de <b>{pct(ini["mutacao"]["score"])}</b> para '
    f'<b>{pct(fim["mutacao"]["score"])}</b>, ganho de '
    f'<b>{resumo["ganhoPontosPercentuais"]:.2f} pontos percentuais</b>. '
    'Na fase final, 205 mutantes foram mortos por asserções, 3 foram detectados por timeout, '
    '5 sobreviveram e nenhum ficou sem cobertura. Os 105 testes passaram e a cobertura atingiu 100% nas quatro métricas.')
add('O Stryker inclui Killed e Timeout no numerador: <b>(205 + 3) / 213 = 97,65%</b>. '
    'Os timeouts são apresentados separadamente; não são mortes por asserção.')
add('<b>A meta bruta superior a 98% não foi alcançada.</b> Os cinco sobreviventes abaixo são '
    'equivalentes nos domínios usuais das funções. Nenhum foi desativado para aumentar artificialmente o resultado.')
tabela([
    ['IDs / função', 'Justificativa da equivalência'],
    ['28, 29, 30 e 32 / fatorial', 'As mutações removem total ou parcialmente o retorno antecipado para 0 e 1. O acumulador já inicia em 1 e o laço começa em 2; sem o retorno antecipado, a saída continua sendo 1. Para os demais inteiros não negativos, o cálculo permanece igual.'],
    ['135 / produtoArray', 'Sem o retorno antecipado de [], reduce com acumulador inicial 1 retorna o mesmo 1. Para arrays não vazios com reduce padrão, ambos os caminhos executam a mesma redução.'],
], [largura * .29, largura * .71])
add('As justificativas foram apoiadas por 171 entradas de fatorial por mutante (0 a 170) e 6 arrays '
    'para produtoArray. Essas amostras confirmam os exemplos; a equivalência decorre da análise '
    'do fluxo e dos elementos neutros, dentro dos domínios declarados.')
add('O cálculo complementar, descontando somente esses cinco equivalentes, é '
    '<b>208 / (213 - 5) = 100%</b>. Esse valor ajustado não substitui o score bruto do Stryker. '
    'Mantendo o código e o conjunto de mutantes, o teto bruto no domínio considerado é 97,65%. '
    'A interpretação da eficácia considera, portanto, tanto a pontuação bruta quanto '
    'as justificativas de equivalência apresentadas.')
add('4. Conclusão', 'Secao')
add('A cobertura mede execução; a mutação avalia a capacidade de detectar alterações de comportamento. '
    'A evolução observada veio de entradas que expõem falhas reais: igualdade, valores não nulos, '
    'arrays desordenados, casos de erro e retornos booleanos falsos. A análise dos equivalentes '
    'também demonstra que um sobrevivente exige interpretação: ele pode revelar uma lacuna nos testes '
    'ou uma transformação sem diferença observável no domínio da função.')
add('Referências e evidências', 'Caso')
add('StrykerJS, configuração: <link href="https://stryker-mutator.io/docs/stryker-js/configuration/">'
    'stryker-mutator.io/docs/stryker-js/configuration/</link><br/>'
    'Operadores de mutação: <link href="https://stryker-mutator.io/docs/mutation-testing-elements/supported-mutators/">'
    'stryker-mutator.io/docs/mutation-testing-elements/supported-mutators/</link><br/>'
    'Evidências locais: reports/resumo.json e reports/mutation/{inicial,final}/mutation.json. '
    'Execuções realizadas em 13/10/2026.', 'Nota')


def rodape(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor('#D6DFE6'))
    canvas.line(50, 42, A4[0] - 50, 42)
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(cinza)
    canvas.drawString(50, 29, 'Análise de eficácia de testes | Testes de Software')
    canvas.drawRightString(A4[0] - 50, 29, str(doc.page))
    canvas.restoreState()


doc = SimpleDocTemplate(str(DESTINO), pagesize=A4, rightMargin=50, leftMargin=50,
                        topMargin=42, bottomMargin=56,
                        title='Análise de Eficácia de Testes com Teste de Mutação',
                        author=identificacao['nome'])
doc.build(story, onFirstPage=rodape, onLaterPages=rodape)
print(f'PDF gerado: {DESTINO}')
