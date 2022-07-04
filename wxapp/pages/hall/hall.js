const app = getApp()
import api from "../../http/api"
import Toast from '../../lib/vant/toast/toast';
import Dialog from '../../lib/vant/dialog/dialog';
import Notify from '../../lib/vant/notify/notify';
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
    empty: false,
    actions: [{name: '删除'},{ name: '私密',subname: '存为私密',}]
  },


  onLoad: function (options) {
    this.setData({userInfo: app.globalData.userInfo})
    this.getTalks()
  },

  getTalks() {
    var that = this;
    api.getTalks("all",this.data.talksPage,1).then(res => {
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
    console.log(this.data.editInfo)
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
    }else if(event == "私密"){
      Dialog.confirm({
        context: this,
        title: '权限修改',
        message: '确定将这条说说设为私密吗？',
      })
      .then(() => {
        wx.getStorage({
          key:"session_key",
          success: function(res) {
            api.publish(that.data.editId,that.data.userInfo.openid,res.data,0).then(res => {
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


})