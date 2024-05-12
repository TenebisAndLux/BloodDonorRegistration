from flask import Flask, send_from_directory, render_template, request, redirect
from flask_restful import Api, Resource, reqparse
from config import host, user, password, port, db_name
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Post {self.username}>'


@app.route('/donors', methods=['GET', 'POST'])
def donors():
    if request.method == 'POST':
        search_surname = request.form.get('surname')
        search_name = request.form.get('name')
        search_street = request.form.get('street')
        search_patronymic = request.form.get('patronymic')
        search_blood = request.form.get('blood')
        search_rh = request.form.get('rh')
        search_house = request.form.get('house')
        search_blood_bank_registration_number = request.form.get('blood_bank_registration_number')
        search_birth_date = request.form.get('birth_date')

        if search_surname or search_name or search_patronymic or search_blood or search_rh or search_house or search_blood_bank_registration_number or search_birth_date:
            donors = Post.query.filter(
                (Post.surname.like(f'%{search_surname}%') if search_surname else False) |
                (Post.name.like(f'%{search_name}%') if search_name else False) |
                (Post.street.like(f'%{search_street}%') if search_street else False) |
                (Post.patronymic.like(f'%{search_patronymic}%') if search_patronymic else False) |
                (Post.blood.like(f'%{search_blood}%') if search_blood else False) |
                (Post.rh.like(f'%{search_rh}%') if search_rh else False) |
                (Post.house.like(f'%{search_house}%') if search_house else False) |
                (Post.blood_bank_registration_number.like(f'%{search_blood_bank_registration_number}%') if search_blood_bank_registration_number else False) |
                (Post.birth_date.like(f'%{search_birth_date}%') if search_birth_date else False)
            ).all()
        else:
            donors = Post.query.all()

    else:
        donors = Post.query.all()

    history = BloodHistory.query.all()

    return render_template('index.html', donors=donors, history=history)


class BloodHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    volume = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<BloodHistory {self.id}>'


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
