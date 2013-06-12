basePath = '../';

files = [
  JASMINE,
  JASMINE_ADAPTER,
  '../../../js/angularjs/lib/angular.js',
  '../../../js/angularjs/lib/angular-*.js',
  'test/lib/angular-mocks.js',
  'app/js/**/*.js',
  'test/unit/**/*.js'
];

autoWatch = true;

browsers = ['Chrome'];

junitReporter = {
  outputFile: 'test_out/unit.xml',
  suite: 'unit'
};
