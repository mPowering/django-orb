// "jasmine-core": "^2.8.0",
// "jsdom": "^11.4.0",
// "jsdom-global": "^3.0.2",
// "karma": "^1.7.1",
// "karma-chrome-launcher": "^2.2.0",
// "karma-coverage": "^1.1.1",
// "karma-es6-shim": "^1.0.0",
// "karma-firefox-launcher": "^1.0.1",
// "karma-jasmine": "^1.1.0",
// "karma-jsdom-launcher": "^6.1.2",
// "karma-phantomjs-launcher": "^1.0.4",
// "karma-phantomjs-shim": "^1.5.0",
// "karma-sourcemap-loader": "^0.3.7",
// "karma-spec-reporter": "^0.0.31",
// "karma-webpack": "^2.0.6",
// "nightwatch": "^0.9.16",
// "phantomjs-prebuilt": "^2.1.16",
// "selenium-download": "^2.0.10",
// "vue-test-utils": "^1.0.0-beta.6",

// karma.conf.js
let webpackConfig = require('./webpack.config.js')
delete webpackConfig.entry



module.exports = function (config) {
    config.set({
        browsers: ['jsdom'],
        singleRun: false,
        autoWatch: true,
        autoWatchBatchDelay: 300,
        frameworks: ['jasmine', 'phantomjs-shim', 'es6-shim'],
        reporters: ['spec', 'coverage'],
        files: [
            './test.js'
        ],
        preprocessors: {
        './test.js': ['webpack', 'sourcemap']
        },
        client: {
            captureConsole: false
        },
        // use the webpack config
        webpack: {
            resolve: {
                extensions: [".js", ".json", '.yaml', '.yml', '.vue'],
                alias: {
                    '@cmp': path.join(__dirname, `./components`),
                    'vue$': 'vue/dist/vue.common.js'
                }
            },
            module: {
                rules: [
                    require('./rules/rules.vue'),
                    require('./rules/rules.babel'),
                ]
            },
            watch: true
        },
        // avoid walls of useless text
        webpackMiddleware: {
        noInfo: true
        }
    })
}
