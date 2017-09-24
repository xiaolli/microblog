import os.path


CSRF_ENABLED =True
SECRET_KEY = 'you-will-never-guess'

UPLOAD_FOLDER= '/Users/xiaolli/PycharmProjects/microblog/app/static/resources'


#email server

MAIL_SERVER = 'localhost'
MAIL_POST = 25
MAIL_USERNAME =None
MAIL_PASSWORD =None
POSTS_PER_PAGE = 3
#Administartor list
ADMINS = ['you@example.com']

basedir = os.path.abspath(os.path.dirname(__file__))
WHOOSH_BASE=os.path.join(basedir,'search.db')
MAX_SEARCH_RESULTS = 10

#日志
LOG_FILE='/Users/xiaolli/PycharmProjects/microblog/app/tmp/microblog.log'