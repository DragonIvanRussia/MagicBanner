from flask import Flask, render_template, redirect, request, make_response, session, abort, jsonify
from data import db_session
from data.users import User
from data.news import Seeds
from forms.user import RegisterForm
import datetime
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.loginform import LoginForm
from forms.news import SaveSeed

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandex_123'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(Seeds).filter((Seeds.user == current_user))
    return render_template('base.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='регистрация', form=form, message='Пароли не совпадают')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='регистрация', form=form, message='такой пользователь уже есть')
        
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='регистрация', form=form)

@app.route('/cookie_test')
def cookie_test():
    visits_count = int(request.cookies.get('visits_count', 0))
    if visits_count:
        res = make_response(f'ggggggg {visits_count + 1}')
        res.set_cookie('visits_count', str(visits_count + 1), max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(f'Вы перешли первый раз')
        res.set_cookie('visits_count', str(1), max_age=60 * 60 * 24 * 365 * 2)
    return res    

@app.route('/session_test')
def session_test():
    visits_count = session.get('visit_count', 0)
    session['visit_count'] = visits_count + 1
    return make_response(f'hvdhvjdhjxvhjb {visits_count + 1} jhvbf')

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/saves', methods=['GET', 'POST'])
@login_required
def add_news():
    
    return render_template('404.html')

    form = SeedsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = Seeds()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('news.html', title='add news', form=form)

@app.route('/saves/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id: int):

    return render_template('404.html')

    form = SeedsForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        news: Seeds = db_sess.query(Seeds).filter(Seeds.id == id, Seeds.user == current_user).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news: Seeds = db_sess.query(Seeds).filter(Seeds.id == id, Seeds.user == current_user).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('news.html', title='Реадктирование новости', form=form)

@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_news(id):
    db_sess = db_session.create_session()
    news: Seeds = db_sess.query(Seeds).filter(Seeds.id == id, Seeds.user == current_user).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')

@app.route('/user_delete', methods=['GET', 'POST'])
@login_required
def delete_user():
    db_sess = db_session.create_session()
    print("DEBUG", current_user)
    if current_user.is_authenticated:
        logout_user()
        db_sess.delete(current_user)
        db_sess.commit()
    else:
        abort(403)
    return redirect('/')

if __name__ == "__main__":
    db_session.global_init("db/blogs.db")
    app.run(port='8080', host='0.0.0.0')
    
