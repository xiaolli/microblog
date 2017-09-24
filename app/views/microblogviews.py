from app import app
from flask import render_template, flash, redirect, url_for, g, request
from app.views.forms import LoginForm, UserForm, NewUserForm, PostForm, SearchForm
from flask_login import login_required, current_user, login_user
from app.controller.usercontroller import UserController
from app.controller.full_text_search import query as search_by_text
# from datetime import datetime,timedelta,timezone
from os.path import join
from os import remove
from app.models import session
# from app.models.models import Posts
from werkzeug.utils import secure_filename


@app.route('/hello')
def hello():
    return 'Hello World!'


@app.route('/html')
def html():
    user = {'nickname': 'Miguel'}  # fake user
    return '''
    <html>
    <head>
    <title>HomePage</title>
    </head>
    <body>
    <h1>Hello,''' + user['nickname'] + '''</h1>
    </body>
    </html>
    '''


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
@login_required
def index(page=1):
    '''
    user = {'nickname':'Miguel'}  #fake user
    template_name ='index.html'
    return render_template(template_name,title='Home',user=user)
    '''
    userController = UserController()
    form = PostForm()
    user = current_user
    if form.validate_on_submit():
        post_body = form.post.data
        user_id = user.id
        user_nickname = user.nickname
        # userController = UserController()
        userController.addpost(user_id=user_id, nickname=user_nickname, post_body=post_body)
        flash('Your post is now living!')

        return redirect(url_for('index'))

    # fakearray of posts
    '''posts=[{'author':{'nickname':'John'},'body':'Beautiful day in Portland!'},
           {'author':{'nickname':'Susan'},'body':'The Avengers movie was so coolbbbbbb!!'}]'''

    followed_posts_results = current_user.followed_posts(page=page)
    # posts =current_user.show_all_posts()
    # posts = current_user.show_all_posts()
    posts = followed_posts_results['posts']

    has_pre_page = followed_posts_results['has_pre_page']
    pre_page_num = followed_posts_results['pre_page_num']
    has_next_page = followed_posts_results['has_next_page']
    next_page_num = followed_posts_results['next_page_num']

    template_name = 'posts.html'

    return render_template(template_name, title='Home', user=user, posts=posts, form=form,
                           has_pre_page=has_pre_page, pre_page_num=pre_page_num,
                           has_next_page=has_next_page, next_page_num=next_page_num)
    # return redirect('/posts')


@app.route('/posts')
@login_required
def posts():
    # user = {'nickname':'Miguel'}  #fakename
    user = current_user
    # fakearray of posts
    posts = [{'author': {'nickname': 'John'}, 'body': 'Beautiful day in Portland!'},
             {'author': {'nickname': 'Susan'}, 'body': 'The Avengers movie was so cool!!'}]

    template_name = 'posts.html'
    return render_template(template_name, title='Posts', user=user, posts=posts)


@app.route('/dologin', methods=['GET', 'POST'])
def doLogin():
    form = LoginForm()

    if form.validate_on_submit():
        flash('username="' + form.username.data + '",password=' + str(form.password.data))

        return redirect('/')
    else:
        template_name = 'login.html'
        return render_template(template_name, form=form, title='SignIn')


@app.route('/user/<username>')
@app.route('/user/<username>/<int:page>')
@login_required
def user(username, page=1):
    userController = UserController()
    user = userController.query_byname(username=username)
    if user == None:
        flash('User:' + username + 'not found')
        return redirect('/')

    # posts = [{'author':user,'body':'Test post #1'},{'author':user,'body':'Test post #2'}]
    # posts = current_user.followed_posts()
    followed_posts_results = current_user.followed_posts(page=page)
    # posts =current_user.show_all_posts()
    # posts = current_user.show_all_posts()

    posts = followed_posts_results['posts']

    has_pre_page = followed_posts_results['has_pre_page']
    pre_page_num = followed_posts_results['pre_page_num']
    has_next_page = followed_posts_results['has_next_page']
    next_page_num = followed_posts_results['next_page_num']

    return render_template('user.html',
                           user=user,
                           posts=posts,
                           has_pre_page=has_pre_page, pre_page_num=pre_page_num,
                           has_next_page=has_next_page, next_page_num=next_page_num
                           )


@app.before_request
def before_request():
    # current_user
    if current_user.is_authenticated:
        userController = UserController()

        current_user.last_seen = userController.set_timpstamp()

        userController.update(current_user)
        g.search_form = SearchForm()


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = UserForm()
    if form.validate_on_submit():
        current_user.nickname = form.nickname.data
        current_user.decription = form.description.data
        file = form.image.data
        if file:
            fileName = str(current_user.username) + secure_filename(file.filename)
            path = join(app.config['UPLOAD_FOLDER'], fileName)
            if current_user.imgpath != 'default.jpg':
                try:
                    remove(join(app.config['UPLOAD_FOLDER'], current_user.imgpath))
                except:
                    print("There is no file to be deleted")

            file.save(path)
            current_user.imagpath = fileName

            flash('Your changes have been saved!')

            return redirect(url_for('edit'))

    else:
        form.nickname.data = current_user.nickname
        form.description.data = current_user.description

        return render_template('edit.html', form=form, title='Edit User')


@app.route('/newuser', methods=['GET', 'POST'])
def newuser():
    form = NewUserForm()
    if form.validate_on_submit():
        username = form.username.data
        userController = UserController()
        user = userController.query_byname(username)
        if user:
            flash('The username is signned up,please use another username')
            return render_template('newuser.html', form=form, title='Sign Up')
        else:
            password = form.password.data
            nickname = form.nickname.data
            description = form.description.data
            user = userController.add(username=username,
                                      password=password,
                                      nickname=nickname,
                                      description=description)

            login_user(user)
            return redirect(url_for('user', username=username))

    return render_template('newuser.html', form=form, title='Sign Up')


@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    session.rollback()
    return render_template('500.html'), 500


'''
@app.route('/follow/<userid>')
@login_required
def follow(userid):
    userController = UserController()
    print("#user_id =",userid)

    #user = userController.query_byname(userid)
    user = userController.query_byId(userid)
    print("follow_user:", user)

    if user is None:
        flash('User %s is not found!' %user.nickname)
        return redirect(url_for('index'))

    if user == current_user:
        flash('You can\'t follow yourself!')
        return redirect(url_for('user',username=user.nickname))

    u= current_user.follow(user)
    if u is None:
        flash('Can not follow' +  user.nickname + '.')
        return redirect(url_for('user',username=user.nickname))

    #session.add(u)
    #session.commit()

    flash('You are now following' + user.nickname + '!')
    return redirect(url_for('user',username=user.nickname))

@app.route('/unfollow/<userid>')
@login_required
def unfollow(userid):
    userController = UserController()
    print("#user_id =", userid)
    #user = userController.query_byname(username)
    user = userController.query_byId(userid)
    print("unfollow_user:",user)

    if user is None:
        flash('User %s is not found' %user.nickname)
        return redirect(url_for('index'))

    if user == current_user:
        flash('You can\'t unfollow yourself!')
        return redirect(url_for('user',username=user.nickname))

    u = current_user.unfollow(user)
    if u is None:
        flash('Can not follow' + user.nickname +'.')
        return redirect(url_for('user',username=user.nickname))

    #session.add(u)
    #session.commit()

    flash('You have stopped following ' + user.nickname + '!')
    return redirect(url_for('user',username=user.nickname))

'''


@app.route('/follow/<username>')
@login_required
def follow(username):
    userController = UserController()

    user = userController.query_byname(username)

    if user is None:
        flash('User %s is not found!' % username)
        return redirect(url_for('index'))

    if user == current_user:
        flash('You can\'t follow yourself!')
        return redirect(url_for('user', username=username))

    u = current_user.follow(user)
    if u is None:
        flash('Can not follow' + username + '.')
        return redirect(url_for('user', username=username))

    # session.add(u)
    # session.commit()

    flash('You are now following' + username + '!')
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    userController = UserController()
    user = userController.query_byname(username)

    if user is None:
        flash('User %s is not found' % username)
        return redirect(url_for('index'))

    if user == current_user:
        flash('You can\'t unfollow yourself!')
        return redirect(url_for('user', username=username))

    u = current_user.unfollow(user)
    if u is None:
        flash('Can not follow' + username + '.')
        return redirect(url_for('user', username=username))

    # session.add(u)
    # session.commit()

    flash('You have stopped following' + username + '!')
    return redirect(url_for('user', username=username))


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()

    if form.validate_on_submit():

        return redirect(url_for('search_results', query=form.search.data))

    else:
        return redirect(url_for('index'))


@app.route('/search_results/<query>')
@login_required
def search_results(query):
    print("query:", query)
    results = search_by_text(query)
    print('results:', results)
    post_ids = []

    for item in results:
        post_ids.append(item['post_id'])

    if len(post_ids) == 0:
        flash('Word: '+query + ' is not matched!')
        return redirect(url_for('index'))

    else:
        userController = UserController()
        posts = userController.search_posts(post_ids=post_ids)


        template_name = 'search_results.html'

        return render_template(template_name, title='Search Resluts', posts=posts, query=query)
