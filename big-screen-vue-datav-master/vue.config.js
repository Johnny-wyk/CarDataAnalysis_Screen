const path = require('path')
const resolve = dir => {
  return path.join(__dirname, dir)
}
module.exports = {
  publicPath: './',
  transpileDependencies: [],
  chainWebpack: config => {
    config.resolve.alias
      .set('_c', resolve('src/components')) // key,value自行定义，比如.set('@@', resolve('src/components'))
  },
  devServer: {
    proxy: {
      '/myApp': {  // 根据后端 API 的路径进行配置
        target: 'http://127.0.0.1:8000',  // Django 服务地址
        changeOrigin: true,
        pathRewrite: { '^/myApp': '/myApp' },
      },
    },
  },
}