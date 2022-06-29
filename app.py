from flask import Flask, render_template, request, jsonify, make_response
from pymongo import MongoClient
import jwt
import certifi
from functools import wraps



app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
# 암호화에 넣을 시크릿 키 ( 아래 두개의 차이점은 무엇일까,,,)
SECRET_KEY = 'hello'
# app.config['SECRET_KEY'] = 'hello'


client = MongoClient('mongodb+srv://test:sparta@cluster0.7ehbb.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=certifi.where())
db = client.dbsparta


def token_required(f):
    @wraps(f)
    def decorated(args,**kwargs):
        token = request.args.get('token')
        if not token:
            return render_template('login.html')
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'])
        except:
            return render_template('login.html')

        return f()(args,**kwargs)
    return decorated


# 메인화면
@app.route("/")
@token_required
def index():
    return render_template('index.html')



if __name__ == '__main__':
    app.run('0.0.0.0', port=5500, debug=True)