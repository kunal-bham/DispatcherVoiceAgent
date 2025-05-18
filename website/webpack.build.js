const webpack = require("webpack")
const webpackConfig = require("./webpack.config.js")

function timeStr(){
  return '[' + new Date().toLocaleTimeString() + ']';
}

const compiler = webpack(webpackConfig)

function compilerCallback (err, stats) {
  console.log(timeStr() + " Building vanta.halo.min")
  if (stats.compilation.errors && stats.compilation.errors.length) {
    console.log('COMPILATION ERROR')
    console.log(stats.compilation.errors)
  }
}

if (process.argv[2] == 'watch') {
  const watching = compiler.watch({
    aggregateTimeout: 300,
    poll: undefined
  }, compilerCallback);
  console.log(timeStr() + " Watching for changes... ");
  (function wait() {
    setTimeout(wait, 1000);
  })();
} else {
  compiler.run(compilerCallback);
}