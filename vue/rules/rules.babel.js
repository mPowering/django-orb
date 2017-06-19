// { test: /\.js/, exclude: /node_modules/, loader: 'babel-loader' }

const js_rules = {
    test: /\.js$/,
    exclude: /(node_modules|bower_components)/,
    use: [
        {
            loader: 'babel-loader',
            // options: {
            //     presets: ['env', 'stage-2']
            // }
        }    
    ]
}

module.exports = js_rules
