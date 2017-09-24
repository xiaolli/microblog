from app.models.models import Users
from app.models import DBSession,session
#增加数据库
user = Users()
user.username ='xiaolli'
user.password ='test'
user.nickname='xiaoliang'
user.email='xiaolli@cn.ibm.com'
user.description ='This is a test user'

session.add(user)

user =Users()
user.username = 'test2'
user.password ='yyy'
user.nickname='xl'
user.email = 'xxx@cn.ibm.com'
user.description = 'this is a test user'

session.add(user)
session.commit()
session.close()

#查询数据库里的所有数据，返回一个LIST对象
users = session.query(Users).all()
print(users)

#查询单个数据，get的数据从1开始
user = session.query(Users).get(1)
print(user)

#更新数据
user.password = '2222'
session.add(user)
session.commit()
session.close()

#查询Users中username=xiaolli的全部数据，返回LIST对象

user_f = session.query(Users).filter_by(username='xiaolli').all
print(user_f)

#删除数据

#user= session.query(Users).get(2)
#print(user)

#session.delete(user)
#session.commit()
#session.close()

users= session.query(Users).all()
print(users)
