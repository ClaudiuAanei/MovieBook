from flask import Blueprint, render_template, request, session, redirect, url_for
from . import db

admin = Blueprint("admin", __name__)

ADMIN_CREDENTIALS = {'admin': 'parola123'}

@admin.route('/adminpage')
def adminpage():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.adminlogin'))
    return render_template('admin_index.html')

@admin.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
            session['admin_logged_in'] = True
            return redirect(url_for('admin.adminpage'))
        else:
            return "Nume utilizator sau parolă greșită!"
    return render_template('admin_login.html')

@admin.route('/adminlogout')
def adminlogout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin.adminlogin'))
