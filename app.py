import os
from flask import Flask
from flask import request
from flask import redirect
from flask import session
from flask import render_template
from models import db # models안에 db라는 변수를 가져온것
from models import Fcuser
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm, LoginForm

app = Flask(__name__)



@app.route('/logout', methods=['GET']) 
def logout():
    session.pop('userid', None)
    return redirect('/')


@app.route('/login', methods=['GET', 'POST']) # 이 2개를 허용하겠다.
def login():
    form = LoginForm()
    if form.validate_on_submit(): # 유효성검사까지 완료해서 post방식으로 넘어왔다는 가정하에~

        session['userid'] = form.data.get('userid')

        return redirect('/')

    return render_template('login.html', form=form) # get으로 왔을때 view에 form넘겨준다





@app.route('/register', methods=['GET', 'POST']) # 이 2개를 허용하겠다.
def register():
    form = RegisterForm()
    if form.validate_on_submit(): # 유효성검사까지 완료해서 post방식으로 넘어왔다는 가정하에~

        # 디비에 반영
        fcuser = Fcuser() # db객체 생성
        fcuser.userid = form.data.get('userid')
        fcuser.username = form.data.get('username')
        fcuser.password = form.data.get('password')

        db.session.add(fcuser) # db에 추가
        db.session.commit() # 커밋. TearDown옵션이 있어서 없어도 되지만..
        print('Success!')

        return redirect('/')

    return render_template('register.html', form=form) # get으로 왔을때 view에 form넘겨준다



@app.route('/')
def hello():
    userid = session.get('userid', None)

    return render_template('hello.html', userid=userid) # 플라스크 내부의 jinja2 템플릿


if __name__ == "__main__": # python app.py 이렇게 실행되게 하려는 설정
    basedir = os.path.abspath(os.path.dirname(__file__)) # 이 파일의 절대경로
    dbfile = os.path.join(basedir, 'db.sqlite') # 이 경로에 디비 파일을 하나 만들겠다.


    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True # TearDown이란 사용자에게 응답을 마쳤을때를 말한다. 이때 커밋을 해주겠다는 옵션임.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 오류방지로 해준다함. 정확히는 모름
    app.config['SECRET_KEY'] = 'qwe7qw98ewq89e7wq89e7wq89ewq' # csrf토큰 설정법

    csrf = CSRFProtect()
    csrf.init_app(app)

    db.init_app(app) # config값들 초기화
    db.app = app  # models.py의 db변수에 app설정해줌
    db.create_all() # 디비 생성

    app.run(host='127.0.0.1', port=5000, debug=True)

