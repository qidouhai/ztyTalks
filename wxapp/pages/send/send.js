import api from "../../http/api"
import Dialog from '../../lib/vant/dialog/dialog';
import Toast from '../../lib/vant/toast/toast';
import Notify from '../../lib/vant/notify/notify';
const app = getApp()

Page({
  data: {
    message: "",
    label: "",
    date: "",
    fileList: [],
    mediaUrls: [],
    publish: "0",
    status: 1,
  },

  onLoad: function (option){

  },

  afterRead(event) {
    var that = this
    const { file } = event.detail;
    file.forEach(function(item,index,file){
      that.upload(item)
    })
  },
  oversize() {
    Notify({ type: 'warning', message: '文件太大，超出限制！' });
  },
  upload(file){
    var that = this
    const { fileList = [] } = that.data;
    const { mediaUrls = [] } = that.data;
    wx.uploadFile({
      url: app.globalData.serverApi + "/api/wx/upload", 
      filePath: file.url,
      name: 'file',
      formData: { 
        'nickName': app.globalData.userInfo.nickName,
        'openid': app.globalData.userInfo.openid,
        'fileUrl': file.url
      },
      success(res) {
        // 上传完成需要更新 fileList
        var data = JSON.parse(res.data) 
        fileList.push({ ...file, fileinfo: data.fileinfo,date:data.date,openid: data.openid,status: 'done',message: '上传完成'});
        mediaUrls.push(data.fileinfo);
        that.setData({ date:data.date });
        that.setData({ mediaUrls });
        that.setData({ fileList });
      },
    });
  },

  delete(event){
    // 删除完成需要更新 fileList
    const { fileList = [] } = this.data;
    const { mediaUrls = [] } = this.data;
    var deleteId = event.detail.index
    var deleteInfo = event.detail.file
    // console.log(deleteInfo)
    api.deleteFile(deleteInfo.openid,deleteInfo.date,deleteInfo.fileinfo.filename).then(res => {
      // console.log(res)
      if(res.status == 200) {
        console.log("删除成功")
        fileList.splice(deleteId, 1)
        mediaUrls.splice(deleteId, 1)
        this.setData({ fileList })
      }
    })
  },
  onChange(event) {
    this.setData({
      radio: event.detail,
    });
  },

  onClick(event) {
    const { name } = event.currentTarget.dataset;
    this.setData({
      publish: name,
    });
  },
  getLoction(){
    Dialog.confirm({
      title: '获取位置',
      message: '点击确定将获取您的位置',
      theme: "round-button"
    })
      .then(() => { 
        // on confirm
      })
      .catch(() => {
        // on cancel
      });
  },

  sendtalks(){
    // console.log(this.data.fileList)
    var mediaUrls = this.data.mediaUrls
    var mediaInfo = ""
    mediaUrls.forEach(function(item){
      mediaInfo += JSON.stringify(item) + ","
    })
    mediaInfo = "[" + mediaInfo + "]"
    var params = {
      session_key: app.globalData.session_key,
      username: app.globalData.userInfo.nickName,
      openid: app.globalData.userInfo.openid,
      status: this.data.status,
      publish: this.data.publish,
      description: this.data.message,
      mediaUrl: mediaInfo,
      label: this.data.label,
      date: this.data.date
    }
    Toast.loading({
      message: '发布中...',
      forbidClick: true,
      duration:0,
      mask:true,
      forbidClick: true
    });
    api.addTalks(params).then(res => {
      if (res.status == 200){
        // console.log(res)
        Toast.clear()
        this.setData({message: "",fileList: [],mediaUrls: [],label:"默认标签",publish: "0",domain: res.domain})
        Toast.success({
          message:'发布成功',
          duration:1000,
          forbidClick: true,
          onClose: () => {
            wx.switchTab({
              url: '../../pages/index/index',
              success: function(e){
                var page = getCurrentPages().pop();  
                if (page == undefined || page == null) return;  
                page.setData({talksPage: 1,talksList:[]})
                page.getTalks();
              }
              
            })
          },  
        });

      }else {
        Toast.clear()
        Toast.fail('发布失败');
      }

    })
  }
});