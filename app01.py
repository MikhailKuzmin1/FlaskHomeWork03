from flask import Flask, render_template, request
from models import db, User
from forms import RegisterForm
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)
app.config['SECRET_KEY'] = b'27fcaef01a1adaf56289ec4bf374e013f55082cb9916d4caeaecd360f8f1a98b'
csrf = CSRFProtect(app)


@app.route('/')
def index():
    return 'Welcom!'


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        second_name = form.second_name.data
        email = form.email.data
        password = form.password.data
        password_hash = generate_password_hash(password)
        user = User(name=name, second_name=second_name, email=email, password=password_hash) 
        db.session.add(user)
        db.session.commit()
    return render_template('register.html', form=form)





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)