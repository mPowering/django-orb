const eslint_rules = {
    test: /\.(js|vue)$/,
    loader: 'eslint-loader',
    enforce: 'pre',
    options: {
        formatter: require('eslint-friendly-formatter')
    }
}

module.exports = eslint_rules
