from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import time
import pymysql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+pymysql://{os.environ.get('MYSQL_USER','user')}:"
    f"{os.environ.get('MYSQL_PASSWORD','password')}@"
    f"{os.environ.get('MYSQL_HOST','db')}/"
    f"{os.environ.get('MYSQL_DATABASE','patients')}")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


def wait_for_db():
    """Block until the MySQL service is available."""
    while True:
        try:
            conn = pymysql.connect(
                host=os.environ.get('MYSQL_HOST', 'db'),
                user=os.environ.get('MYSQL_USER', 'user'),
                password=os.environ.get('MYSQL_PASSWORD', 'password'),
                database=os.environ.get('MYSQL_DATABASE', 'patients'),
            )
            conn.close()
            break
        except pymysql.err.OperationalError:
            print("Waiting for database to be ready...")
            time.sleep(1)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        notes = request.form.get('notes','')
        patient = Patient(name=name, age=age, notes=notes)
        db.session.add(patient)
        db.session.commit()
        return redirect('/')
    patients = Patient.query.all()
    return render_template('index.html', patients=patients)

if __name__ == '__main__':
    wait_for_db()
    # Ensure database tables are created within the application context
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0')
