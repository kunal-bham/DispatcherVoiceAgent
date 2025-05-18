const path = require('path')
const webpack = require('webpack')

module.exports = {
  mode: 'production',
  entry: {
    'vanta.halo.min': './src/vanta.halo.js'
  },
  output: {
    filename: '[name].js',
    path: path.resolve(__dirname, 'dist'),
    library: '_vantaEffect',
    libraryTarget: 'umd',
    globalObject: 'typeof self !== \'undefined\' ? self : this',
  },
  module: {
    rules: [
      { test: /\.(glsl|frag|vert)$/, use: ['raw-loader', 'glslify-loader'], exclude: /node_modules/ },
    ],
  },
  optimization: {
    minimize: true
  },
  plugins: [
    new webpack.optimize.ModuleConcatenationPlugin(),
  ],
  devServer: {
    static: {
      directory: path.join(__dirname, ''),
    },
    compress: true,
  }
}