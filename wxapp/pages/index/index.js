// pages/index/index.js
import Toast from '../../lib/vant/toast/toast';
import Dialog from '../../lib/vant/dialog/dialog';
import Notify from '../../lib/vant/notify/notify';
import api from "../../http/api"
const app = getApp()
Page({

  data: {
    serverApi: app.globalData.serverApi,
    talksPage: 1,
    userInfo: {},
    talksList: [],
    systemInfo:app.globalData.systemInfo,
    allPage: 0,
    show: false,
    qiniuDomain: app.globalData.qiniuDomain,
    editId:"",
    editInfo: {},
    empty: false,
    actions: [{name: '删除'},{ name: '公开',subname: '展示在大厅，所有人可见',}],
  },

  getTalks() {
    var that = this;
    api.getTalks(this.data.userInfo.openid,this.data.talksPage,0).then(res => {
      if (res.code == 200) {
        that.setData({
          talksList: that.data.talksList.concat(res.list),
          allPage: res.allpage,
        })
        if (that.data.talksList.length == 0){
          that.setData({empty: true})
        }else {
          that.setData({empty: false})
        }
      }
    })
  },
  mediaPlay(Event){
    var url = Event.target.dataset.currenturl
    var index = Event.target.dataset.index
    var mediaList = Event.target.dataset.medialist
    var date = Event.target.dataset.date
    var that = this
    var sources = []
   
    mediaList.forEach(function(item,index,mediaList){
      sources[index] = {
        url:  that.data.qiniuDomain + "/talks/" + that.data.userInfo.openid + "/" + date + "/" + item.filename,
        type: item.filetype
      }
    })
    console.log(sources)
    wx.previewMedia({
      sources: sources, 
      current: index, 
      url: url 
    })

  },

  action(e){
    var show = this.data.show;
    this.setData({ show: !show });
    this.setData({
      editId: e.target.dataset.talkid,
      editInfo: e.target.dataset.talkinfo
    })
  },
  onClose() {
    this.setData({ show: false });
  },

  onSelect(e) {
    var that = this
    var event = e.detail.name
    if(event == "删除"){
      Dialog.confirm({
        context: this,
        title: '删除',
        message: '确定删除这条说说吗？',
      })
      .then(() => {
       wx.getStorage({
          key:"session_key",
          success: function(res) {
            api.deleteTalk(that.data.editId,that.data.userInfo.openid,res.data).then(res=> {
              if(res.code == 200){
                Notify({ type: 'success', message: '删除成功！' });
                that.setData({talksPage: 1,talksList:[]})
                that.getTalks()
              }else{
                Notify({ type: 'warning', message: '删除失败！' });
              }
            })
          }
        })
      })
    }else if(event == "公开"){
      Dialog.confirm({
        context: this,
        title: '权限修改',
        message: '确定公开这条说说吗？',
      })
      .then(() => {
        wx.getStorage({
          key:"session_key",
          success: function(res) {
            api.publish(that.data.editId,that.data.userInfo.openid,res.data,1).then(res => {
              if(res.code == 200){
                Notify({ type: 'success', message: '权限修改成功！' });
                that.setData({talksPage: 1,talksList:[]})
                that.getTalks()
              }else{
                Notify({ type: 'warning', message: '权限修改失败！' });
              }
            })
          }
        })
      })
    }
  },

  onLoad: function (options) {
    var that = this
    wx.getStorage({
      key: 'openid',
      success: function(res) {
        // console.log(res)
        api.getUser(res.data).then(res => {
          that.setData({
            userInfo: res.obj
          })
          app.globalData.userInfo = res.obj
          that.getTalks()
        wx.setStorage({
          key:"openid",
          data:res.obj.openid
        })
        wx.setStorage({
          key:"nickName",
          data:res.obj.nickName
        })
        wx.setStorage({
          key:"avatarUrl",
          data:res.obj.avatarUrl
        })
        })

      }
    })
  },

  onRefresh(){
    var that = this
    wx.showNavigationBarLoading()
    Toast.loading({
      message: '正在刷新...',
      forbidClick: true,
      duration:0,
      mask:true,
      forbidClick: true
    });
    setTimeout(function () {
      that.setData({talksPage: 1,talksList:[]})
      that.getTalks()
      wx.hideNavigationBarLoading();
      Toast.clear()
      wx.stopPullDownRefresh();
      wx.stopPullDownRefresh();
    }, 500)
  },
  onPullDownRefresh:function(){
    this.onRefresh();
  },
  sendTalk(){
    wx.reLaunch({
      url: '/pages/send/send',
    })
  },

  copy(e) {
    var text = e.target.dataset.copytext
    console.log("复制成功:",text)
    wx.setClipboardData({
      data: text,
      success: function(res){
        wx.getClipboardData({
          success: function (res) {
            Notify({ type: 'success', message: '文本复制成功！' });
          },
          fail: function(res){
            Notify({ type: 'warning', message: '文本复制失败！' });
          }
        })
      }
    })
  }
  
})