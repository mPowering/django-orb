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
