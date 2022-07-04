import hashlib,shutil,json,uuid,time,os,requests,filetype
from urllib.parse import quote
from flask import Blueprint, jsonify, request, session,make_response
from exts import db, basedir, appId, appSecret,Domain
from models.model import talksSheet, WxUser, Admin
from controller import Qiniu
import datetime,time

api = Blueprint('api', __name__)


def auth(session_key,openid):
	try:
		wxuser = WxUser.query.filter(WxUser.openid == openid).first()
		a = hashlib.md5()
		a.update(session_key.encode(encoding="utf-8"))
		key = a.hexdigest()  # sha1哈希加密
		print("加密",key,wxuser.session_key)
		if key == wxuser.session_key:
			return True 
		else:
			return False
	except:
		return False



# 用户登录接口
@api.route('/signIn', methods=['POST'])
def signIn():
	# 从request对象中读取表单内容：
	username = request.form.get('username')
	password = request.form['password']
	userResult = Admin.query.filter(Admin.userName == username).first()  # 简单查询  使用关键字实参的形式来设置字段名
	if userResult is not None:
		a = hashlib.md5()
		a.update(password.encode(encoding="utf-8"))
		md5Password = a.hexdigest()  # sha1哈希加密
		if md5Password == userResult.password:
			session['username'] = userResult.userName
			return jsonify({'status': 200, 'errmsg': '登录成功！'})
		return jsonify({'status': 500, 'errmsg': '用户密码错误，请输入正确的密码！'})
	return jsonify({'status': 500, 'errmsg': '登录失败，用户不存在！'})


# 上传图片视频
@api.route('/wx/upload', methods=['post'])
def up_file():
	nickName = request.values.get('nickName')
	openid = request.values.get('openid')
	fileUrl = request.values.get('fileUrl')
	date =  time.strftime('%Y-%m-%d', time.localtime(int(time.time()))) 
	fileExt = fileUrl.split(".")[-1]
	fileName = str(uuid.uuid1())
	filePath = f"{basedir}/uploadfile/{openid}/{date}"
	isExists = os.path.exists(filePath)
	if not isExists:
		os.makedirs(filePath)
	img = request.files.get('file')
	f = open(f'{filePath}/{fileName}.{fileExt}',"wb")
	f.write(img.read())
	f.close()
	filePath = f"{basedir}/uploadfile/{openid}/{date}/{fileName}.{fileExt}"
	kind = filetype.guess(filePath)
	file_type = kind.mime.split("/")[0]
	return jsonify({'status': 200, 'url': f"https://talks.ztyang.com/api/uploadfile?openid={openid}&date={date}&filename={fileName}.{fileExt}",
	'nickName': nickName,"date":date,"fileinfo":{'filename':f"{fileName}.{fileExt}",'filetype': file_type},'openid': openid})



# 删除图片视频
@api.route('/wx/delete', methods=['post'])
def delete_file():
	filename = request.args.get('filename')
	openid = request.args.get('openid')
	date =  request.args.get('date')
	filePath = f"{basedir}/uploadfile/{openid}/{date}/{filename}"
	# print(filePath)
	isExists = os.path.exists(filePath)
	if isExists:
		os.remove(filePath)
		return jsonify({'status': 200, 'msg': '删除成功','filename': filename})
	else:
		return jsonify({'status': 500, 'errmsg': '文件不存在，删除失败','filename': filename})

# 构造媒体响应
@api.route("/uploadfile",methods=['GET'])
def get_frame():
	try:
		openid = request.values.get('openid')
		date = request.values.get('date')
		filename = request.values.get('filename')
		filePath = f"{basedir}/uploadfile/{openid}/{date}/{filename}"
		kind = filetype.guess(filePath)
		# print(kind.mime)
		with open(filePath, 'rb') as f:
			file = f.read()
			response = make_response(file)
			utf_filename = quote(filename.encode("utf-8"))
			response.headers["Content-Disposition"] = "inline;filename*=utf-8''{}".format(utf_filename)
			response.headers["Content-Type"] = kind.mime
			return response
	except: 
		return jsonify({'status': 500, 'errmsg': '文件不存在','filename': filename})
 
 

# 添加说说
@api.route('/wx/addtalks', methods=['POST'])
def talksAdd():
	# try:
	session_key = request.values.get('session_key')
	openid = None if request.values.get('openid') == "undefined" else request.values.get('openid')
	print("会话验证失败",auth(session_key,openid))
	if not auth(session_key,openid):
		return jsonify({'status': 500, 'errmsg': '发布失败！'})
	description = request.values.get('description')
	publish = int(request.values.get('publish'))
	date = request.values.get('date')
	status = int(request.values.get('status'))
	username = None if request.values.get('username') == "undefined" else request.values.get('username')
	label = "默认标签" if request.values.get('label') == "" else request.values.get('label')
	mediaUrl = eval(request.values.get('mediaUrl'))
	location = request.values.get('location')
	qiniu = Qiniu(openid,date)
	for item in mediaUrl:
		qiniu.upload(item['filename'])
	filePath = f"{basedir}/uploadfile/{openid}/{date}"
	if os.path.exists(filePath):
		shutil.rmtree(filePath)
	if description == "" and mediaUrl == "":
		return jsonify({'status': 500, 'errmsg': '发布失败！'})
	param = talksSheet(status=status,openid=openid,publish=publish, description=description, username=username, label=label,
								mediaUrl=str(mediaUrl),
								location=location,
								thumbUp=0,
							publishDate=int(time.time())
		)
	db.session.add(param)
	db.session.commit()
	if param.id > 0:
		return jsonify({'status': 200, 'msg': '发布成功！','domain':Domain})
	return jsonify({'status': 500, 'errmsg': '发布失败！'})
	# except:
	# 	return jsonify({'status': 500, 'errmsg': '发布失败！'})


# 查询说说数据返回json
@api.route("/talkslist", methods=['GET', 'POST'])
def talksList():
	try:
		per_page = 10
		publish = int(request.args.get("publish"))
		publish = [0,1] if publish == 0 else [1]
		page = int(request.args.get("page"))
		openid = request.args.get("openid")
		if openid != "all":
			dataw = talksSheet.query.filter(talksSheet.openid == openid,talksSheet.publish.in_(publish)).order_by(
			talksSheet.id.desc()).paginate(page, per_page=per_page, error_out=False)
			allpage = int(len(talksSheet.query.filter(talksSheet.openid == openid,talksSheet.publish.in_(publish)).all()) / 10) + 1
		else:
			dataw = talksSheet.query.filter(talksSheet.publish.in_(publish)).order_by(
			talksSheet.id.desc()).paginate(page, per_page=per_page, error_out=False)
			allpage = int(len(talksSheet.query.filter(talksSheet.publish.in_(publish)).all()) / 10) + 1
		jsonData = []
		for pet in dataw.items:
			publishDate = ''
			if pet.publishDate is not None:
				publishDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(pet.publishDate)))
				date = publishDate.split(" ")[0]
			talk_list = pet.description.split("\n")
			talkHtml = '<div class="talks">' + "".join([f'<p class="p">{item}</p>' for item in talk_list]) + '</div>'
			o = {'openid': pet.openid, 'id': pet.id, "location": pet.location, "description": pet.description,
				"username": pet.username, "label": pet.label,'publish':pet.publish,'talkHtml':talkHtml,
				"mediaUrl": eval(pet.mediaUrl),"thumbUp": pet.thumbUp,"publishDate": publishDate,'date': date}
			jsonData.append(o)
		
		p = {'code': 200,'page': dataw.page, 'allpage': allpage,"list": jsonData}
		return jsonify(p)
	except:
		return jsonify({'code': 500,'errmsg': '查询失败'})

# 根据id删除说说
@api.route('/wx/deleteTalk', methods=['POST'])
def deleteTalk():
	talkId = request.values.get('talkid')
	openid = request.values.get('openid')
	session_key = request.values.get('session_key')
	resulttalks = talksSheet.query.filter(talksSheet.id == talkId,talksSheet.openid == openid).first()
	mediaUrl = eval(resulttalks.mediaUrl)
	date = time.strftime('%Y-%m-%d', time.localtime(int(resulttalks.publishDate)))
	if auth(session_key,openid):
		db.session.delete(resulttalks)
		db.session.commit()
		if len(mediaUrl) != 0:
			qiniu = Qiniu(openid,date)
			for item in mediaUrl:
				qiniu.delete(item['filename'])
		return jsonify({'code': 200, 'msg': '删除成功！'})
	return jsonify({'code': 500, 'errmsg': '删除失败！'})

# 修改说说权限
@api.route("/wx/editpublish", methods=['POST'])
def editpublish():
	openid = request.args.get("openid")
	session_key = request.args.get("session_key")
	talkId = request.args.get("talkid")
	publish = int(request.args.get("publish"))
	if auth(session_key,openid):
		dataw = talksSheet.query.filter(talksSheet.id == talkId,talksSheet.openid == openid).first()
		dataw.publish = publish
		db.session.commit()
		return jsonify({'code': 200, 'msg': '修改成功！'})
	return jsonify({'code': 500, 'errmsg': '修改失败！'})

# 请求微信接口获取openid、session_key
@api.route("/wx/login", methods=['GET', 'POST'])
def wxLogin():
	code = request.args.get("code")
	wxUrl = "https://api.weixin.qq.com/sns/jscode2session?appid={appId}&secret={appSecret}&js_code={code}&grant_type=authorization_code".format(
		appId=appId, appSecret=appSecret, code=code)
	req = requests.get(wxUrl) 
	jsonText = req.text  
	resultJson = json.loads(jsonText) 
	print("微信接口:",resultJson) 
	resultUser = WxUser.query.filter(WxUser.openid == resultJson['openid']).first()
	if resultUser is not None:
		jsonData = {'id': resultUser.id, 'openid': resultUser.openid, "avatarUrl": resultUser.avatarUrl,
					"nickName": resultUser.nickName,'session_key': resultJson['session_key']}
		resultJson = jsonData
	else:
		resultJson = {"openid": resultJson['openid'],'session_key': resultJson['session_key']}
	return resultJson



# 通过 openid 获取用户信息
@api.route("/wx/getUserInfoByOpenid", methods=['GET', 'POST'])
def wxGetUserInfoByOpenid():
	openid = request.args.get("openid")
	resultUser = WxUser.query.filter(WxUser.openid == openid).first()
	if resultUser is not None:
		jsonData = {'id': resultUser.id, 'openid': resultUser.openid, "avatarUrl": resultUser.avatarUrl,
					"nickName": resultUser.nickName}
		resultJson = {"code": 200, "obj": jsonData}
	else:
		resultJson = {"code": 500, "obj": ''}
	return resultJson

def cal_time(stamp1,stamp2):
    t1=time.localtime(stamp1)
    t2 = time.localtime(stamp2)
    t1=time.strftime("%Y-%m-%d %H:%M:%S",t1)
    t2 = time.strftime("%Y-%m-%d %H:%M:%S", t2)
    time1=datetime.datetime.strptime(t1,"%Y-%m-%d %H:%M:%S")
    time2 = datetime.datetime.strptime(t2, "%Y-%m-%d %H:%M:%S")
    return int((time2-time1).seconds / (24 * 60 * 60)) + 1

# 通过 openid 获取信息
@api.route("/wx/getInfo", methods=['POST'])
def getInfo():
	openid = request.args.get("openid")
	resultUser = WxUser.query.filter(WxUser.openid == openid).first()
	days = cal_time(int(resultUser.createDate),int(time.time()))
	label_count = len(talksSheet.query.filter(talksSheet.openid == openid).order_by(talksSheet.label,talksSheet.id.desc()).group_by(talksSheet.label).all())
	talk_count = len(talksSheet.query.filter(talksSheet.openid == openid).all())
	if resultUser is not None:
		jsonData = {'id': resultUser.id, 'openid': resultUser.openid, "avatarUrl": resultUser.avatarUrl,
					"nickName": resultUser.nickName,'createDate': resultUser.createDate,'days':days,'talk_count':talk_count,'label_count':label_count}
		resultJson = {"code": 200, "obj": jsonData}
	else:
		resultJson = {"code": 500, "obj": ''}
	return resultJson


# 更新微信用户信息
@api.route("/wx/updateUserInfo", methods=['GET','POST'])
def updateUserInfo():
	try:
		openid = request.args.get("openid")
		nickName = request.args.get("nickname")
		avatarUrl = request.args.get("avatarurl")
		User = WxUser.query.filter(WxUser.openid == openid).first()
		User.nickName = nickName
		User.avatarUrl = avatarUrl
		db.session.commit()
		return jsonify({'status': 200, 'msg': '更新成功！'})
	except:
		return jsonify({'status': 500, 'errmsg': '更新失败！'})




# 保存微信用户信息
@api.route("/wx/addUser", methods=['POST'])
def saveUserInfo():
	openid = request.args.get("openid")
	nickName = request.args.get("nickName")
	avatarUrl = request.args.get("avatarUrl")
	session_key = request.args.get("session_key")
	a = hashlib.md5()
	a.update(session_key.encode(encoding="utf-8"))
	md5key = a.hexdigest()  # sha1哈希加密
	create = int(time.time())
	if openid and nickName and avatarUrl and session_key :
		param = WxUser(nickName=nickName, openid=openid, avatarUrl=avatarUrl,createDate=create,session_key=md5key)
		db.session.add(param)
		db.session.commit()
		if param.id > 0:
			return jsonify({'status': 200, 'errmsg': '添加成功！'})
		return jsonify({'status': 500, 'errmsg': '添加失败！'})
	else:
		return jsonify({'status': 500, 'errmsg': '添加失败！'})


# 更新session_key
@api.route("/wx/updatekey", methods=['POST'])
def updatekey():
	try:
		session_key = request.args.get("session_key")
		openid = request.args.get("openid")
		a = hashlib.md5()
		a.update(session_key.encode(encoding="utf-8"))
		md5key = a.hexdigest()  # sha1哈希加密
		wxuser = WxUser.query.filter(WxUser.openid == openid).first()
		wxuser.session_key = md5key
		db.session.commit()
		return jsonify({'code': 200, 'msg': 'session_key更新成功！'})
	except:
		return jsonify({'code': 500, 'errmsg': 'session_key更新失败！'})


