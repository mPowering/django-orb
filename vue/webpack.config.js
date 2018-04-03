'use strict'
require('yamlify/register')

// file system funcions
const path = require('path')
const fs = require('fs')

// processor functionalities
const webpack = require('webpack')
const yaml = require('js-yaml')

const notifier = require("webpack-notifier")
const browser_sync = require('browser-sync-webpack-plugin')
const friendly_errors = require('friendly-errors-webpack-plugin')


module.exports = (env) => {

    let CFG = env.init ? require(`${__dirname}/${env.init}`) : null
    let PROD = CFG.PROD = env.production ? true : false
    let DJANGO = CFG.DJANGO = env.django ? true : false

    let config = {
        entry: CFG.entries,
        output: {
            filename: `${CFG.publicPath}[name].js`,
            chunkFilename: `${CFG.publicPath}[name].js`,
            path: path.resolve(__dirname, CFG.build),
            publicPath: CFG.publicPath,
        },
        module: {
            rules: [
                require('./rules/rules.eslint'),
                require('./rules/rules.vue'),
                require('./rules/rules.babel'),

            ]
        },
        cache: !PROD,
        target: 'web',
        // devtool: 'inline-eval-cheap-source-map',
        // context: path.resolve(CFG.src),
        resolve: {
            extensions: [".js", ".json", '.yaml', '.yml', '.vue'],
            alias: {
                '@cmp': path.join(__dirname, `${CFG.src}/components`),
                'vue$': 'vue/dist/vue.common.js'
            }
        },
        plugins: [
            new webpack.DefinePlugin({
                'process.env': {
                    NODE_ENV: PROD ? '"production"' : '"development"'
                }
            }),
            new notifier({
                title: CFG.project,
                alwaysNotify: false,
                skipFirstNotification: false
            }),
            new friendly_errors(),
            // new webpack.optimize.CommonsChunkPlugin({
            //     name: 'vendor',
            //     minChunks: function (module, count) {
            //         // any required modules inside node_modules are extracted to vendor
            //         return (
            //         module.resource &&
            //         /\.js$/.test(module.resource) &&
            //         module.resource.indexOf(
            //             path.join(__dirname, '../node_modules')
            //         ) === 0
            //         )
            //     }
            // }),
            // new webpack.optimize.CommonsChunkPlugin({
            //     name: 'manifest',
            //     chunks: ['vendor']
            // }),
            new browser_sync({
                server: DJANGO ? false : CFG.build,
                proxy: DJANGO ? "localhost:8000" : false,
                port: 1515,
                ui: {
                    port: 8002,
                    weinre: 8003,
                },
                reloadDelay: 500,
                // reloadDebounce: 2000,
                ghostMode: {
                    clicks: true,
                    forms: true,
                    scroll: true,
                },
                logPrefix: CFG.project + " -- DEV",
                open: false,
                reloadOnRestart: true,
                injectChange: false,
                notify: false,
            }),
        ]
    }
    return config
}
