from qiniu import Auth, put_file, BucketManager
from exts import Access_key, Aecret_key, Bucket_name,basedir
from flask import jsonify


class Qiniu():
    def __init__(self,openid,date):
        self.openid = openid
        self.date = date
        self.auth = Auth(Access_key, Aecret_key)

    def upload(self,filename):
        key = f'talks/{self.openid}/{self.date}/{filename}'
        token = self.auth.upload_token(Bucket_name, key, 600)
        localfile = f'{basedir}/uploadfile/{self.openid}/{self.date}/{filename}'
        ret, info = put_file(token, key, localfile, version='v2') 
        ret['status_code'] = info.status_code
        return ret

    def delete(self,filename):
        bucket = BucketManager(self.auth)
        bucket_name = 'ztydisk'
        key = f'talks/{self.openid}/{self.date}/{filename}'
        print(key)
        info = bucket.delete(bucket_name, key)
        return jsonify({'status_code':'info.status_code'})




