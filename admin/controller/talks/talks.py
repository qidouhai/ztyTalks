from flask import request, Blueprint, jsonify, render_template

from exts import db
from models.model import talksSheet
import time

talks = Blueprint('talks', __name__)


# 查询说说数据
@talks.route("/listView", methods=['GET', 'POST'])
def listView():
    dataw = talksSheet.query.order_by(talksSheet.label,talksSheet.id.desc()).group_by(talksSheet.label).all()
    label_list = []
    for item in dataw:
        label_list.append(item.label)
    print(label_list)
    return render_template('/talks/listView.html',label_list=label_list)


# 查询说说数据
@talks.route("/list", methods=['GET', 'POST'])
def list():
    page = request.args.get("page")
    limit = request.args.get("limit")
    label = request.args.get("label")
    username = request.args.get("username")
    keyword = request.args.get("keyword")
    dataw = None
    if keyword is not None and keyword != "" and label is not None and label != "":
        dataw = talksSheet.query.filter(talksSheet.description.like(f'%{keyword}%'),
                                                talksSheet.label == label).order_by(
            talksSheet.id.desc()).paginate(int(page), per_page=int(limit), error_out=False)
    elif label is not None and label != "":
        dataw = talksSheet.query.filter(talksSheet.label == label).order_by(
            talksSheet.id.desc()).paginate(int(page), per_page=int(limit), error_out=False)
    elif keyword is not None and keyword != "":
        dataw = talksSheet.query.filter(talksSheet.description.like(f'%{keyword}%')).order_by(
            talksSheet.id.desc()).paginate(int(page), per_page=int(limit), error_out=False)
    elif username is not None and username != "":
        dataw = talksSheet.query.filter(
            talksSheet.username == username).order_by(
            talksSheet.id.desc()).paginate(int(page), per_page=int(limit), error_out=False)
    else:
        dataw = talksSheet.query.order_by(
            talksSheet.id.desc()).paginate(int(page), per_page=int(limit), error_out=False)
    jsonData = []
    for pet in dataw.items:
        publishDate = ''
        if pet.publishDate is not None:
            publishDate = time.strftime('%Y-%m-%d', time.localtime(int(pet.publishDate))) 
        o = {
                'id': pet.id, 
                "username": pet.username, 
                "status": pet.status, 
                "publish": pet.publish, 
                "location": pet.location,
                "description": pet.description,
                "mediaUrl": pet.mediaUrl,
                "thumbUp": pet.thumbUp,
                "label": pet.label, 
                "publishDate": publishDate
            }
        jsonData.append(o)
    p = {'page': dataw.page, "data": jsonData, "count": dataw.total, "code": 0}
    return jsonify(p)


# 修改说说
@talks.route("/editView/<int:id>", methods=['GET', 'POST'])
def editView(id):
    dataw = talksSheet.query.filter(talksSheet.id == id).paginate()
    data = dataw.items[0]
    return render_template('/talks/editView.html', id=id,data = data)



# 修改说说
@talks.route('/edit', methods=['POST'])
def edit():
    # 从request对象中读取表单内容：
    talksId = request.form['id']
    status = request.form['status']
    description = request.form['description']
    mediaurl = request.form['mediaurl']
    label = request.form['label']
    # 先查询再更新
    resulttalks = talksSheet.query.filter(talksSheet.id == talksId).first()
    resulttalks.status = status
    resulttalks.description = description
    resulttalks.mediaUrl = mediaurl
    resulttalks.label = label
    db.session.commit()
    print(resulttalks)
    if resulttalks.id > 0:
        return jsonify({'status': 200, 'errmsg': '修改成功！'})
    return jsonify({'status': 500, 'errmsg': '修改失败！'})


# 删除说说
@talks.route('/delete', methods=['POST'])
def delete():
    # 从request对象中读取表单内容：
    talksId = request.form['id']
    # 先查询再更新
    resulttalks = talksSheet.query.filter(talksSheet.id == talksId).first()
    db.session.delete(resulttalks)
    db.session.commit()
    print(resulttalks)
    if resulttalks.id > 0:
        return jsonify({'status': 200, 'errmsg': '删除成功！'})
    return jsonify({'status': 500, 'errmsg': '删除失败！'})

