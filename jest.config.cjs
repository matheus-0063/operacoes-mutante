module.exports = {
  testEnvironment: 'node',
  testMatch: ['<rootDir>/test/**/*.test.js'],
  transform: {},
  collectCoverageFrom: ['src/**/*.js'],
  coverageReporters: ['text', 'html', 'json', 'json-summary', 'lcov'],
};
