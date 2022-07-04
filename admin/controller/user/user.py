import hashlib

from flask import request, Blueprint, jsonify, render_template

from exts import db
from models.model import WxUser

user = Blueprint('user', __name__)


# 用户添加view
@user.route('/addView')
def addView():
    return render_template('/user/addView.html')




# 查询用户数据
@user.route("/listView/<int:page>", methods=['GET', 'POST'])
def listView(page=1):
    users = WxUser.query.order_by(WxUser.id.desc()).paginate(page, per_page=10)
    return render_template('/user/listView.html', infos=users.items, pagination=users)



# 删除用户信息
@user.route('/delete', methods=['POST'])
def delete():
    # 从request对象中读取表单内容：
    userId = request.form['id']
    # 先查询再更新
    resultUser = WxUser.query.filter(WxUser.id == userId).first()
    db.session.delete(resultUser)
    db.session.commit()
    print(resultUser)
    if resultUser.id > 0:
        return jsonify({'status': 200, 'errmsg': '删除成功！'})
    return jsonify({'status': 500, 'errmsg': '删除失败！'})
