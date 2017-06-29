// karma.conf.js
let webpackConfig = require('./webpack.config.js')
delete webpackConfig.entry



module.exports = function (config) {
    config.set({
        browsers: ['PhantomJS'],
        singleRun: false,
        autoWatch: true,
        autoWatchBatchDelay: 300,
        frameworks: ['jasmine', 'chai', 'phantomjs-shim', 'es6-shim'],
        reporters: ['spec', 'coverage'],
        files: ['./test.js'],
        preprocessors: {
        './test.js': ['webpack', 'sourcemap']
        },
        // use the webpack config
        webpack: {
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
