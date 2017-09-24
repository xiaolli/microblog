import unittest
from app.controller.usercontroller import UserController
from app.models.models import Users
from app.models import session
from datetime import datetime

class UsersTestCase(unittest.TestCase):
    def test_get_imgpath(self):
        userController = UserController()
        user = userController.query_byname('test2')
        img_path = user.get_imgpath()
        self.assertEqual(img_path,'../static/resources/default.jpg')

    def test_follow(self):
        u1 = Users()
        u1.username = 'json'
        u1.password ='123456'
        u1.nickname = 'Json'
        u1.description = 'This is Json'
        u1.email='Json@json.com'
        u1.imgpath ='default.jpg'
        u1.last_seen =datetime.utcnow()

        u2 = Users()
        u2.username = 'kathy'
        u2.password = '123456'
        u2.nickname ='Kathy'
        u2.description = 'This is Kathy'
        u2.email = 'Kathy@kathy.com'
        u2.imgpath = 'default.jpg'
        u2.last_seen = datetime.utcnow()

        session.add(u1)
        session.add(u2)
        session.commit()


        self.assertNotEqual(u1.unfollow(u2), None)

        u =  u1.follow(u2)
        print(u1)
        print(u2)
        print(u)
        session.add(u)
        session.commit()

        self.assertEqual(u1.is_following(u2), True)
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u2.followed.count(), 0)

if __name__=='__main__':
    unittest.main()