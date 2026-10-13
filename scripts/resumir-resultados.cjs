const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const vm = require('node:vm');

const root = path.resolve(__dirname, '..');
const ler = (arquivo) => JSON.parse(fs.readFileSync(path.join(root, arquivo), 'utf8'));
const fonte = fs.readFileSync(path.join(root, 'src/operacoes.js'), 'utf8');
const fases = {};
const relatorios = {};

for (const fase of ['inicial', 'final']) {
  const relatorio = ler(`reports/mutation/${fase}/mutation.json`);
  const arquivo = relatorio.files['src/operacoes.js'];
  if (arquivo.source !== fonte) throw new Error(`Fonte do relatório ${fase} difere da fonte atual. Reexecute a análise.`);
  const contagem = { Killed: 0, Timeout: 0, Survived: 0, NoCoverage: 0 };
  for (const mutante of arquivo.mutants) {
    if (!(mutante.status in contagem)) throw new Error(`Status inesperado: ${mutante.status}. Revise o relatório.`);
    contagem[mutante.status]++;
  }
  const total = arquivo.mutants.length;
  const detectados = contagem.Killed + contagem.Timeout;
  fases[fase] = {
    testes: Object.values(relatorio.testFiles).reduce((soma, arquivo) => soma + arquivo.tests.length, 0),
    cobertura: ler(`coverage/${fase}/coverage-summary.json`).total,
    mutacao: { total, ...contagem, detectados, score: 100 * detectados / total },
  };
  relatorios[fase] = arquivo;
}

// Requer o mesmo conjunto de mutações nas duas fases para a comparação ser válida.
const identidade = (m) => JSON.stringify([m.id, m.mutatorName, m.location, m.replacement]);
if (JSON.stringify(relatorios.inicial.mutants.map(identidade).sort()) !== JSON.stringify(relatorios.final.mutants.map(identidade).sort())) {
  throw new Error('Os conjuntos de mutantes inicial e final diferem. Reexecute ambas as fases com a mesma configuração.');
}

const justificativas = {
  '28': 'Sem o retorno antecipado de fatorial(0) ou fatorial(1), resultado começa em 1 e o laço não executa; a saída continua 1.',
  '29': 'A conjunção n === 0 && n === 1 nunca é verdadeira; para 0 e 1 o laço não executa e a saída continua 1.',
  '30': 'Desativar somente n === 0 faz fatorial(0) chegar ao acumulador 1 sem executar o laço.',
  '32': 'Desativar somente n === 1 faz fatorial(1) chegar ao acumulador 1 sem executar o laço.',
  '135': 'O reduce de um array vazio, com valor inicial 1, já retorna 1; o retorno antecipado é redundante para arrays comuns.',
};
const sobreviventes = relatorios.final.mutants.filter((m) => m.status === 'Survived');
const executar = (codigo) => {
  const contexto = { module: { exports: {} } };
  vm.runInNewContext(codigo, contexto, { timeout: 1000 });
  return contexto.module.exports;
};
const original = executar(fonte);
function alterar(mutante) {
  const linhas = fonte.split('\n');
  const offset = ({ line, column }) => linhas.slice(0, line - 1).reduce((soma, linha) => soma + linha.length + 1, 0) + column - 1;
  return fonte.slice(0, offset(mutante.location.start)) + mutante.replacement + fonte.slice(offset(mutante.location.end));
}
const equivalentes = sobreviventes.map((m) => {
  if (!justificativas[m.id]) throw new Error(`Mutante ${m.id} ainda precisa de análise; não deve ser classificado como equivalente automaticamente.`);
  const trecho = alterar(m);
  const alterado = executar(trecho);
  const funcao = m.id === '135' ? 'produtoArray' : 'fatorial';
  const entradas = funcao === 'fatorial'
    ? Array.from({ length: 171 }, (_, i) => i)
    : [[], [2], [-3, 2], [0, 5], [-1, -2], [1, 2, 3]];
  for (const entrada of entradas) {
    if (!Object.is(original[funcao](entrada), alterado[funcao](entrada))) {
      throw new Error(`A amostra refuta a equivalência do mutante ${m.id}.`);
    }
  }
  return { id: m.id, linha: m.location.start.line, tipo: m.mutatorName, replacement: m.replacement,
    justificativa: justificativas[m.id], amostrasVerificadas: entradas.length,
    dominio: funcao === 'fatorial' ? 'números inteiros não negativos' : 'arrays comuns de números com reduce padrão' };
});

const idsCriticos = ['177', '193', '156'];
const criticos = idsCriticos.map((id) => {
  const inicial = relatorios.inicial.mutants.find((m) => m.id === id);
  const final = relatorios.final.mutants.find((m) => m.id === id);
  if (inicial?.status !== 'Survived' || final?.status !== 'Killed') throw new Error(`Revise o exemplo crítico ${id}.`);
  return { id, linha: inicial.location.start.line, tipo: inicial.mutatorName, replacement: inicial.replacement,
    statusInicial: inicial.status, statusFinal: final.status, killedBy: final.killedBy };
});
const resumo = {
  data: '2026-10-13',
  ambiente: { node: process.version, jest: require('jest/package.json').version,
    stryker: require('@stryker-mutator/core/package.json').version },
  fonteSha256: crypto.createHash('sha256').update(fonte).digest('hex'),
  ...fases,
  ganhoPontosPercentuais: fases.final.mutacao.score - fases.inicial.mutacao.score,
  metaBrutaSuperada: fases.final.mutacao.score > 98,
  scoreAjustadoPorEquivalentes: 100 * fases.final.mutacao.detectados / (fases.final.mutacao.total - equivalentes.length),
  aviso: 'O score ajustado é uma análise complementar; não substitui o score bruto emitido pelo Stryker. Amostras apoiam a justificativa, mas não provam equivalência por si só.',
  equivalentes,
  criticos,
};
fs.writeFileSync(path.join(root, 'reports/resumo.json'), JSON.stringify(resumo, null, 2) + '\n');
for (const fase of ['inicial', 'final']) {
  const valores = fases[fase];
  console.log(`${fase}: ${valores.testes} testes; linhas ${valores.cobertura.lines.pct}%; score ${valores.mutacao.score.toFixed(2)}%`);
}
console.log(`Meta bruta > 98%: ${resumo.metaBrutaSuperada ? 'atingida' : 'não atingida'}; ${equivalentes.length} equivalentes documentados.`);
console.log(`Score ajustado complementar: ${resumo.scoreAjustadoPorEquivalentes.toFixed(2)}%. Evidências: reports/resumo.json`);
