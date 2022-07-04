import fly from './index'

export default {
  getTalks(openid,page,publish) {
    return fly.post("/api/talkslist",null,{params:{openid,page,publish}
    })
  },
 
  getToken(code) {
    return fly.get("/api/wx/login",{code})
  },

  getUser(openid) {
    return fly.post("/api/wx/getUserInfoByOpenid",null,{params:{openid}})
  },
  getInfo(openid) {
    return fly.post("/api/wx/getInfo",null,{params:{openid}})
  },
  updateUserinfo(openid,nickname,avatarurl) {
    return fly.post("/api/wx/updateUserInfo",null,{params:{openid,nickname,avatarurl}})
  },
  addUser(openid,nickName,avatarUrl,session_key) {
    return fly.post("/api/wx/addUser",null,{params:{openid,nickName,avatarUrl,session_key}})
  },
  deleteFile(openid,date,filename) {
    return fly.post("/api/wx/delete",null,{params:{openid,date,filename}})
  },
  addTalks(params) {
    return fly.post("/api/wx/addtalks",null,{params})
  },
  updatekey(openid,session_key) {
    return fly.post("/api/wx/updatekey",null,{params:{openid,session_key}})
  },
  deleteTalk(talkid,openid,session_key) {
    return fly.post("/api/wx/deleteTalk",null,{params:{talkid,openid,session_key}})
  },
  publish(talkid,openid,session_key,publish) {
    return fly.post("/api/wx/editpublish",null,{params:{talkid,openid,session_key,publish}})
  }
}