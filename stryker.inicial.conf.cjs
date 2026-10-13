const config = require('./stryker.conf.json');
const jestConfig = require('./jest.config.cjs');

module.exports = {
  ...config,
  jest: {
    projectType: 'custom',
    config: {
      ...jestConfig,
      testMatch: ['<rootDir>/test/operacoes.test.js'],
    },
  },
  htmlReporter: { fileName: 'reports/mutation/inicial/mutation.html' },
  jsonReporter: { fileName: 'reports/mutation/inicial/mutation.json' },
};
