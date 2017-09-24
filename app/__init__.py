from flask import Flask
from app import config
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler,RotatingFileHandler

app = Flask(__name__)
app.config.from_object(config)

#注册LOGIN管理
lm = LoginManager()
lm.session_protection = 'strong'
lm.login_view = 'auth.login'
lm.init_app(app)


app.secret_key = 'something is secret for others'

from app.views import microblogviews
from app.views import authorview

#注册Blueprint模块
app.register_blueprint(authorview.auth,url_prefix='/auth')

#发送邮件
if not app.debug:
    credentials = None
    if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        credentials=(app.config['MAIL_USERNAME'],app.config['MAIL_PASSWORD'])
    mail_hander =SMTPHandler((app.config['MAIL_SERVER'],app.config['MAIL_POST']),
                             'no-reply@'+app.config['MAIL_SERVER'],app.config['ADMINS'],
                             'microblogfailure',credentials)
    mail_hander.setLevel(logging.ERROR)
    app.logger.addHandler(mail_hander)

#打开一个伪造的邮箱服务器,当邮箱服务器运行后，应用程序发送的邮件将会被接收到并且显示在命令行窗口上
#python3 -m smtpd -n -c DebuggingServerlocalhost:25

#记录LOG
if not app.debug:
    file_hander =RotatingFileHandler(app.config['LOG_FILE'],'a',1*1024*1024,10)
    file_hander.setFormatter(logging.Formatter('%(asctime)s%(levelname)s:%(message)s[in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_hander.setLevel(logging.INFO)
    app.logger.addHandler(file_hander)
    app.logger.info('microblog startup')