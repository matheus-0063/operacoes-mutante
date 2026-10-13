const op = require('../src/operacoes');

describe('Casos complementares orientados pelos mutantes iniciais', () => {
  describe('Erros, mensagens e limites das operações básicas', () => {
    test('divisão por zero preserva a mensagem de erro', () => {
      expect(() => op.divisao(5, 0)).toThrow(new Error('Divisão por zero não é permitida.'));
    });

    test('raiz quadrada aceita zero e rejeita negativos com mensagem específica', () => {
      expect(op.raizQuadrada(0)).toBe(0);
      expect(() => op.raizQuadrada(-1)).toThrow(
        new Error('Não é possível calcular a raiz quadrada de um número negativo.'),
      );
    });

    test.each([[0, 1], [1, 1], [2, 2], [5, 120]])('fatorial(%s) = %s', (n, esperado) => {
      expect(op.fatorial(n)).toBe(esperado);
    });

    test('fatorial rejeita negativos com mensagem específica', () => {
      expect(() => op.fatorial(-1)).toThrow(
        new Error('Fatorial não é definido para números negativos.'),
      );
    });

    test('arrays vazios respeitam os elementos neutros e o contrato da média', () => {
      expect(op.somaArray([])).toBe(0);
      expect(op.mediaArray([])).toBe(0);
      expect(op.produtoArray([])).toBe(1);
    });

    test.each([
      ['maximoArray', 'Array vazio не possui valor máximo.'],
      ['minimoArray', 'Array vazio не possui valor mínimo.'],
      ['medianaArray', 'Array vazio не possui mediana.'],
    ])('%s rejeita array vazio com a mensagem original', (funcao, mensagem) => {
      // As mensagens do projeto base contêm "не"; o contrato original foi preservado.
      expect(() => op[funcao]([])).toThrow(new Error(mensagem));
    });

    test('inverso rejeita zero com mensagem específica', () => {
      expect(() => op.inverso(0)).toThrow(new Error('Não é possível inverter o número zero.'));
      expect(op.inverso(-4)).toBe(-0.25);
    });
  });

  describe('Resultados booleanos e valores de fronteira', () => {
    test.each([
      [0, true, false], [2, true, false], [3, false, true],
      [-2, true, false], [-3, false, true],
    ])('paridade de %s: par=%s, ímpar=%s', (n, par, impar) => {
      expect(op.isPar(n)).toBe(par);
      expect(op.isImpar(n)).toBe(impar);
    });

    test.each([
      [-1, false], [0, false], [1, false], [2, true], [3, true],
      [4, false], [9, false], [25, false], [29, true],
    ])('isPrimo(%s) = %s', (n, esperado) => {
      expect(op.isPrimo(n)).toBe(esperado);
    });

    test.each([
      [10, 2, true], [10, 3, false], [0, 3, true], [-10, 2, true], [10, 0, false],
    ])('isDivisivel(%s, %s) = %s', (a, b, esperado) => {
      expect(op.isDivisivel(a, b)).toBe(esperado);
    });

    test.each([
      [5, 5, false, false, true], [3, 5, false, true, false], [5, 3, true, false, false],
    ])('comparações de %s e %s', (a, b, maior, menor, igual) => {
      expect(op.isMaiorQue(a, b)).toBe(maior);
      expect(op.isMenorQue(a, b)).toBe(menor);
      expect(op.isEqual(a, b)).toBe(igual);
    });

    test('igualdade é estrita, sem coerção de tipos', () => {
      expect(op.isEqual(7, '7')).toBe(false);
    });

    test.each([
      [-5, 0], [0, 0], [5, 5], [10, 10], [15, 10],
    ])('clamp(%s, 0, 10) = %s', (valor, esperado) => {
      expect(op.clamp(valor, 0, 10)).toBe(esperado);
    });

    test('clamp preserva o sinal do zero recebido nas fronteiras', () => {
      // +0 e -0 são iguais em comparações, mas distinguíveis por Object.is e 1 / x.
      expect(op.clamp(+0, -0, 1)).toBe(+0);
      expect(op.clamp(-0, -1, +0)).toBe(-0);
    });
  });

  describe('Entradas que não anulam os fatores de conversão', () => {
    test.each([[100, 212], [-40, -40], [25, 77]])(
      '%s Celsius = %s Fahrenheit', (celsius, fahrenheit) => {
        expect(op.celsiusParaFahrenheit(celsius)).toBeCloseTo(fahrenheit, 10);
      },
    );

    test.each([[212, 100], [-40, -40], [77, 25]])(
      '%s Fahrenheit = %s Celsius', (fahrenheit, celsius) => {
        expect(op.fahrenheitParaCelsius(fahrenheit)).toBeCloseTo(celsius, 10);
      },
    );
  });

  describe('Mediana com ordenação numérica e tamanhos variados', () => {
    test.each([
      [[3, 1, 2], 2],
      [[10, 2, 1], 2],
      [[9, 1, 5, 3], 4],
      [[10, 2], 6],
      [[-1, -10, -3], -3],
      [[5], 5],
      [[4, 1, 4, 2], 3],
    ])('mediana de %j = %s', (valores, esperado) => {
      expect(op.medianaArray(valores)).toBe(esperado);
    });

    test('mediana não modifica o array recebido', () => {
      const valores = [9, 1, 5, 3];
      expect(op.medianaArray(valores)).toBe(4);
      expect(valores).toEqual([9, 1, 5, 3]);
    });
  });
});
