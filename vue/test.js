// require all test files using special Webpack feature
// https://webpack.github.io/docs/context.html#require-context
import Vue from 'vue'

Vue.config.productionTip = false

var testsContext = require.context('./components/', true, /\.spec$/)
testsContext.keys().forEach(testsContext)
