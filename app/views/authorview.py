from flask_login import login_required,current_user,login_user,logout_user
from flask import Blueprint,redirect,flash,render_template
from app import lm
from app.controller.usercontroller import UserController
from app.views.forms import LoginForm

auth = Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    #如果已经LOGIN，重定向到首页
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()

    if form.validate_on_submit():
        # flash('username="'+ form.username.data + '", password=' + str(form.password.data))
        username = form.username.data
        password = form.password.data
        user_controller= UserController()

        user =user_controller.query(username=username,password=password)

        #是否是注册用户

        if user:
            login_user(user)
            return redirect('/')

        else:
            flash('username or password is wrong')
            return redirect('auth/login')

    else:
        template_name = 'login.html'
        return render_template(template_name,title='Sign In',form=form)



@auth.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash('user is logout')
    return redirect('/auth/login')

@lm.user_loader
def user_load(user_id):
    user_controller= UserController()
    user = user_controller.query_byId(user_id=int(user_id))
    return user






