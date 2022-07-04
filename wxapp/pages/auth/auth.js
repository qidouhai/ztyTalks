// pages/auth/auth.js
import api from "../../http/api"
const app = getApp()
Page({

  getUserProfile(e) {
    // 推荐使用wx.getUserProfile获取用户信息，开发者每次通过该接口获取用户个人信息均需用户确认
    // 开发者妥善保管用户快速填写的头像昵称，避免重复弹窗
    wx.getUserProfile({
      desc: '用于完善用户资料', // 声明获取用户个人信息后的用途，后续会展示在弹窗中，请谨慎填写
      success: (res) => {
        this.auth(res.userInfo)
      },
      fail: () => {
        wx.exitMiniProgram()
      }
    })
  },

  auth(userInfo) {
    var that = this
    wx.login({
      success (res) {
        if (res.code) {
          api.getToken(res.code).then(res => {
            console.log(res.session_key)
            var openid = res.openid
            var session_key = res.session_key
            api.updateUserinfo(openid,userInfo.nickName,userInfo.avatarUrl)
            api.getUser(openid).then(res => {
              if(res.code == 200){
                console.log("用户存在")
                api.updatekey(openid,session_key)
                that.setUser(openid,session_key)
              }else if(res.code == 500){
                console.log("添加用户")
                api.addUser(openid,userInfo.nickName,userInfo.avatarUrl,session_key).then(res => {
                  that.setUser(openid,session_key)
                })
              }else {
                console.log("未知错误")
              }
            })
          })
        } else {
          console.log('登录失败！' + res.errMsg)
            wx.showModal({
              title: "登录失败！",
              content: res.errMsg
            });
        }
      }
    })
  },

  setUser(openid,session_key){
    wx.setStorage({
      key:"openid",
      data:openid
    })
    wx.setStorage({
      key:"session_key",
      data:session_key
    })
    app.globalData.session_key = session_key
    wx.reLaunch({
      url: '/pages/index/index',
    })
  }

})
