// pages/user/user.js
import api from "../../http/api"
const app = getApp()
Page({
  data: {
    avatarUrl:"",
    nickName:"",
    info:{}
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this
    wx.getStorage({
      key: 'avatarUrl',
      success: function(res) {
        that.setData({
          avatarUrl: res.data
        })
      }
    })
    wx.getStorage({
      key: 'nickName',
      success: function(res) {
        that.setData({
          nickName: res.data
        })
      }
    })
  },
  cleanStorge(){
    wx.clearStorageSync()
    wx.showToast({
      title: "清理成功", // 提示的内容
      icon: "success", // 图标，默认success
      image: "", // 自定义图标的本地路径，image 的优先级高于 icon
      duration: 3000, // 提示的延迟时间，默认1500
      mask: false, // 是否显示透明蒙层，防止触摸穿透
      success: function () {
          // console.log("接口调用成功的回调函数");
          wx.reLaunch({
            url: '/pages/auth/auth',
          })
      },
      fail: function () {
          // console.log("接口调用失败的回调函数");
      },
      complete: function () {
          // console.log("接口调用结束的回调函数（调用成功、失败都会执行）");
      }
  })
  },
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    var that= this
    api.getInfo(app.globalData.userInfo.openid).then(res => {
      if(res.code == 200)
      console.log(res.obj)
      that.setData({
        info: res.obj
      })
    })
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})