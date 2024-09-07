from flask import render_template, redirect, url_for, flash
from app import app, db
from datetime import datetime
from app.forms import LoginForm, RegistrationForm, AddStudentForm, BorrowForm, DisplayStudentForm, DeactivateStudentForm
from app.models import Student, Loan

# This file contains all the route definitions for the web app, e.g., login, registration, borrow item etc.


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/datetime')
def date_time():
    now = datetime.now()
    return render_template('datetime.html', title='Date & Time', now=now)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login for {form.username.data}', 'success')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Registration for {form.username.data} received', 'success')
        return redirect(url_for('index'))
    return render_template('registration.html', title='Register', form=form)


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    form = AddStudentForm()
    if form.validate_on_submit():
        new_student = Student(username=form.username.data, firstname=form.firstname.data,
                              lastname=form.lastname.data, email=form.email.data)
        db.session.add(new_student)
        try:
            db.session.commit()
            flash(f'New Student added: {form.username.data} received', 'success')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            if Student.query.filter_by(username=form.username.data).first():
                form.username.errors.append('This username is already taken. Please choose another')
            if Student.query.filter_by(email=form.email.data).first():
                form.email.errors.append('This email address is already registered. Please choose another')
    return render_template('add_student.html', title='Add Student', form=form)


@app.route('/borrow', methods=['GET', 'POST'])
def borrow():
    form = BorrowForm()
    if form.validate_on_submit():
        new_loan = Loan(device_id=form.device_id.data,
                        student_id=form.student_id.data,
                        borrowdatetime=datetime.now())
        db.session.add(new_loan)
        try:
            db.session.commit()
            flash(f'New Loan added', 'success')
            return redirect(url_for('index'))
        except:
            db.session.rollback()

    return render_template('borrow.html', title='Borrow', form=form)


@app.route('/displaystudentinfo', methods=['GET', 'POST'])
def display():
    form = DisplayStudentForm()
    if form.validate_on_submit():
        students = Student.query.all()
        check = True
        # flash(f'{students}')
        for student in students:
            flash(f'Student ID: {student.student_id}, Active: {student.active}, Firstname: {student.firstname}, '
                  f'Lastname: {student.lastname}, Username: {student.username} Email: {student.email}, '
                  f'Loans: ', 'success')

    return render_template('displaystudents.html', title='Display Students', form=form)


@app.route('/deactivate', methods=['GET', 'POST'])
def deactivate_student():
    form = DeactivateStudentForm()
    if form.validate_on_submit():
        to_deactivate = form.student_id.data
        student_id = Student.query.filter_by(student_id=to_deactivate)
        # student_id(active=False)       <--- I tried to set the student id object's active value to false
        try:
            db.session.commit()
            flash('Success, student deactivated', 'success')
        except:
            db.session.rollback()
            flash('Failed, student not deactivated', 'success')

    return render_template('deactivate_student.html', title='Deactivate Student', form=form)
