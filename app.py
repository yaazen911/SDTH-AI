from flask import Flask, render_template, request, redirect, session, url_for
from datetime import datetime
import joblib
from sensor_sim import simulate_trip_summary
import random

DEMO_MODE = True
model = joblib.load('model.pkl')
from models import db, User, Truck, Trip

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sdth.db'
app.secret_key = 'change_this_secret_key_later'
db.init_app(app)
 
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['user_id'] = user.id
            session['role'] = user.role
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('driver_home'))
        else:
            return render_template('login.html', error='بيانات الدخول غير صحيحة')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/driver')
def driver_home():
    if 'user_id' not in session or session['role'] != 'driver':
        return redirect(url_for('login'))

    # هل عند السائق رحلة نشطة الحين؟
    trip = Trip.query.filter_by(driver_id=session['user_id'], status='active').first()
    truck = db.session.get(Truck, trip.truck_id) if trip else None

    return render_template('driver.html', trip=trip, truck=truck,
                           message=request.args.get('message'))

@app.route('/start_shift', methods=['POST'])
def start_shift():
    if 'user_id' not in session or session['role'] != 'driver':
        return redirect(url_for('login'))

    qr_code = request.form['qr_code'].strip()
    truck = Truck.query.filter_by(qr_code=qr_code).first()

    if not truck:
        return redirect(url_for('driver_home', message='كود الشاحنة غير صحيح'))
    if truck.status == 'in_use':
        return redirect(url_for('driver_home', message='الشاحنة مستخدمة حالياً'))

    trip = Trip(driver_id=session['user_id'], truck_id=truck.id,
                start_time=datetime.now(), status='active')
    truck.status = 'in_use'
    db.session.add(trip)
    db.session.commit()
    return redirect(url_for('driver_home'))

@app.route('/end_shift', methods=['POST'])
def end_shift():
    if 'user_id' not in session or session['role'] != 'driver':
        return redirect(url_for('login'))

    trip = Trip.query.filter_by(driver_id=session['user_id'], status='active').first()
    if trip:
        # محاكاة بيانات القيادة ثم تصنيفها بالموديل
        style = request.form.get('style', 'safe')
        features = simulate_trip_summary(style)
        prediction = model.predict([features])[0]

        trip.end_time = datetime.now()
        trip.status = 'completed'
        trip.behavior_result = 'reckless' if prediction == 1 else 'safe'
        truck = db.session.get(Truck, trip.truck_id)
        truck.status = 'available'
        db.session.commit()
    return redirect(url_for('driver_home'))

@app.route('/admin')
def admin_dashboard():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    return "مرحباً بك في لوحة تحكم الإدمن"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)