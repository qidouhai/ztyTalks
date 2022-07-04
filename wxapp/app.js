
App({
  globalData: {
    userInfo: {},
    session_key: "",
    systemInfo:{},
    serverApi: "https://talks.ztyang.com",
    qiniuDomain: "https://disk.ztyang.com"
  },

  onLaunch: function () {
    var that = this
    wx.getStorage({
      key: 'openid',
      success: function(res) {
        if(res.data == undefined){
          wx.reLaunch({
            url: '/pages/auth/auth',
          })
        }else{
          // console.log("本地Storage已有openid:" + res.data)
        }
      },
      fail: function(){
        wx.reLaunch({
          url: '/pages/auth/auth',
        })
      }
      
    })
    wx.getStorage({
      key: 'session_key',
      success: function(res) {
        if(res.data == undefined){
          wx.reLaunch({
            url: '/pages/auth/auth',
          })
        }else{
          that.globalData.session_key = res.data
        }
      }
    })
    wx.getSystemInfo({
      success (res) {
        that.globalData.systemInfo = res
      }
    })
  },

})
