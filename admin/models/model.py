from exts import db


# 用户模型
class Admin(db.Model):
    tableName = 'admin'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    userName = db.Column(name='userName', nullable=False)
    password = db.Column(db.String(30), nullable=False)


# 微信用户模型
class WxUser(db.Model):
    tableName = 'wxuser'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    openid = db.Column(name='openid', nullable=False)
    nickName = db.Column(name='nickName', nullable=False)
    avatarUrl = db.Column(name='avatarUrl', nullable=False)
    session_key = db.Column(name='session_key', nullable=False)
    createDate = db.Column(name='createDate', nullable=False)


# 说说表模型
class talksSheet(db.Model):
    __tableName__ = 'talksSheet'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    openid = db.Column(name='openid', nullable=False)
    publish = db.Column(name='publish', nullable=False)
    username = db.Column(name='username', nullable=False)
    status = db.Column(name='status', nullable=False)
    publishDate = db.Column(name='publishDate', nullable=False)
    description = db.Column(name='description', nullable=False)
    mediaUrl = db.Column(name='mediaUrl', nullable=False)
    thumbUp = db.Column(name='thumbUp', nullable=False)
    label = db.Column(name='label', nullable=False)
    location = db.Column(name='location', nullable=False)
    
