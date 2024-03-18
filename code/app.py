from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from db import db
from flask_login import LoginManager
import webbrowser

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.template_folder = 'templates'
app.config['SECRET_KEY'] = 'your_secret_key_here'

db.init_app(app)

login_manager = LoginManager(app)


if __name__ == '__main__':

    from user import user_bp
    app.register_blueprint(user_bp)
    print('網站建立完成，如果沒有自動建立網站，請在網址輸入127.0.0.1:5000/login_view')

    from user.model import user 

    with app.app_context():
        db.create_all()

        if user.query.count() == 0:
            new_user = user(name="admin", password="admin", serial_number=10)
            db.session.add(new_user)
            db.session.commit()

    @login_manager.user_loader
    def load_user(user_id):
        return user.query.get(int(user_id))
    
    webbrowser.open('http://127.0.0.1:5000')
    app.run(debug=False)



