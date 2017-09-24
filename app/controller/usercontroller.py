from app.models.models import Users, Posts
from app.models import session
from datetime import datetime, timezone, timedelta
from app.controller.full_text_search import create_index


class UserController:
    def query(self, username, password):
        user = session.query(Users).filter_by(username=username, password=password).first()

        return user

    def query_byId(self, user_id):
        user = session.query(Users).filter_by(id=user_id).first()
        return user

    def query_byname(self, username):
        user = session.query(Users).filter_by(username=username).first()

        return user

    def update(self, user):
        session.add(user)
        session.commit()

    def add(self, username, password, nickname, description):
        user = Users()
        user.username = username
        user.password = password
        user.nickname = nickname
        user.description = description
        user.email = ''
        user.imgpath = 'default.jpg'
        session.add(user)
        session.commit()

        user.follow(user)
        session.add(user)
        session.commit()

        print('&&&&&&&&&&', user)

        return user

    def addpost(self, user_id, nickname, post_body):
        post = Posts()
        post.userid = user_id
        post.body = post_body
        post.timestamp = self.set_timpstamp()

        session.add(post)
        session.commit()

        create_index(user_id=user_id,
                     post_id=post.id,
                     nickname=nickname,
                     post_body=post.body)

        '''
        y1=sqlite3.connect('/Users/xiaolli/PycharmProjects/microblog/app/microblog.db')
        cur=y1.cursor()
        #cur.execute("DELETE  from users where username = 'xiaoli' or username = 'wang'")
        #y1.commit()
        #y1.close()
        #cur.execute("select * from posts")
        cur.execute("SELECT * FROM users")
        col_name = [tuple[0] for tuple in cur.description]
        print('@@@@@@',col_name)

        rows = cur.fetchall()
        for row in rows:
            print (row)

        #cur.execute("select * from posts")

        #cur.execute("DELETE FROM posts WHERE userid =1 or userid = 2")
        #y1.commit()
        cur.execute("SELECT * FROM posts")

        col_name = [tuple[0] for tuple in cur.description]
        print('@@@@@@',col_name)

        rows = cur.fetchall()
        for row in rows:
            print (row)

        #cur.execute("select * from posts")
        cur.execute("SELECT * FROM followers")
        col_name = [tuple[0] for tuple in cur.description]
        print('@@@@@@',col_name)

        rows = cur.fetchall()
        for row in rows:
            print (row)
        '''

        return post

    def set_timpstamp(self):
        dt = datetime.utcnow()
        # print("#1:",dt)
        dt = dt.replace(tzinfo=timezone.utc)
        # print("#2:", dt)
        tzutc_8 = timezone(timedelta(hours=8))
        # print("#3:",tzutc_8)
        local_dt = dt.astimezone(tzutc_8)
        # print("#4:", local_dt)

        return local_dt

    def search_posts(self, post_ids):
        posts = session.query(Posts).filter(Posts.id.in_(other=post_ids)).order_by(Posts.timestamp.desc()).all()

        return posts
