const Fly = require("../lib/wx.js")
const fly = Fly()
var app = getApp();
fly.config.baseURL = app.globalData.serverApi

// 请求拦截
fly.interceptors.request.use(config => {
  return config
})


// 响应拦截
fly.interceptors.response.use(res => {
  return res.data 
})

export default fly