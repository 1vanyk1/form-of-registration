from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from data import db_session
from data.users import User
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
def home_page():
    param = {}
    db_session.global_init("db/blogs.sqlite")
    session = db_session.create_session()
    for job in session.query(Jobs).all():
        param['jobs'] = param.get('jobs', []) + [[job.id, job.job, job.team_leader, job.work_size, job.collaborators, job.is_finished]]
    return render_template('list_of_jobs.html', **param)


@app.route('/success')
def success():
    param = {}
    return render_template('success.html', title='Регистрация', **param)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    db_session.global_init("db/blogs.sqlite")
    session = db_session.create_session()
    if request.method == 'POST' and form.validate() and form.is_submitted():
        if form.password.data != form.password2.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = form.age.data
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data
        user.email = form.email.data
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/success')
    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
