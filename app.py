from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import time
import pymysql
from datetime import datetime, date

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
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    dni = db.Column(db.String(20), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    admission_date = db.Column(db.Date, nullable=False)
    health_insurance = db.Column(db.String(120), nullable=True)
    reason = db.Column(db.Text, nullable=True)
    symptom_start = db.Column(db.Date, nullable=True)
    hpo = db.Column(db.Text, nullable=True)
    diagnosed = db.Column(db.Boolean, default=False)
    diagnosis = db.Column(db.String(255), nullable=True)
    video_url = db.Column(db.String(255), nullable=True)
    studies_link = db.Column(db.String(255), nullable=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dni = request.form['dni']
        birth_date = datetime.strptime(request.form['birth_date'], '%Y-%m-%d').date()
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        admission_date = datetime.strptime(request.form['admission_date'], '%Y-%m-%d').date()
        health_insurance = request.form.get('health_insurance', '')
        reason = request.form.get('reason', '')
        symptom_start_str = request.form.get('symptom_start')
        symptom_start = datetime.strptime(symptom_start_str, '%Y-%m-%d').date() if symptom_start_str else None
        hpo = request.form.get('hpo', '')
        diagnosed = bool(request.form.get('diagnosed'))
        diagnosis = request.form.get('diagnosis', '') if diagnosed else ''
        video_url = request.form.get('video_url', '')
        studies_link = request.form.get('studies_link', '')
        patient = Patient(
            first_name=first_name,
            last_name=last_name,
            dni=dni,
            birth_date=birth_date,
            age=age,
            admission_date=admission_date,
            health_insurance=health_insurance,
            reason=reason,
            symptom_start=symptom_start,
            hpo=hpo,
            diagnosed=diagnosed,
            diagnosis=diagnosis,
            video_url=video_url,
            studies_link=studies_link,
        )
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
