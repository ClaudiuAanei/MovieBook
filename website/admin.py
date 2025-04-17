from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from flask_login import logout_user
from .movies_requests import update_popular_movies, update_popular_series
from .models import User, RandomMovie, SaveMovie
from . import db

ADMIN_CREDENTIALS = {'admin': 'parola123'}
users_per_page = 10
users_on_pages = {}
pagini = 1

admin = Blueprint("admin", __name__)


@admin.route('/adminpage')
def adminpage():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.adminlogin'))
    logout_user()
    page = request.args.get('page')
    if page:
        pages = get_pagination_pages(int(page), pagini)
        users_on_page = pagination(int(page))
        if request.method == "GET":
            return render_template('admin_index.html', users= users_on_page, pages= pages, current_page = int(page))
    else:
        return render_template('admin_index.html', users= pagination(1), pages= get_pagination_pages(1, pagini), current_page = 1)


@admin.route('/admin/update', methods= ['GET'])
def update():
    updates = request.args.get('update')
    if request.method == 'GET':
        if updates == 'movies':
            update_popular_movies()
            flash('Movies Trending Successful updated')
        elif updates == 'series':
            update_popular_series()
            flash('Series Trending Successful updated')
        return redirect(url_for('admin.adminpage'))
    return render_template('admin_index.html')


@admin.route('/admin/remove_account', methods= ['GET','POST'])
def remove_account():
    if request.method == "POST":
        email = request.form["email"]
        remove_user(email)
    else:
        email = request.args.get("email")
        remove_user(email)
    return redirect(url_for('admin.adminpage'))


def remove_user(email):
    user = db.session.execute(db.select(User).where(User.email == email)).scalar()
    if user:
        # Stergerea activitatilor uitlizatorului
        db.session.query(RandomMovie).filter_by(movie_owner=user.id).delete()
        db.session.query(SaveMovie).filter_by(user_who_saved_movie=user.id).delete()
        # Stergerea utilizatorului

        db.session.delete(user)
        db.session.commit()
        flash(f'User: {user.name} With Id: {user.id} and email {user.email} is successful deleted.')
    else:
        flash('User does not exists in database.')


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



def pagination(key): # trimite users in ruta principala si verifica conditiile acolo, asa vei inlatura global
    users = db.session.execute(db.select(User).order_by(User.email)).scalars().all()
    if users:
        global pagini
        pagini = int(len(users) / users_per_page) + 1
        index = 0
        index2 = 0
        for i in range(1, pagini + 1):
            index2 += users_per_page
            lista_items = []
            for j in range(index, index2):
                try:
                    lista_items.append(users[j])
                except IndexError:
                    break
            users_on_pages[i] = lista_items
            index += users_per_page

        return users_on_pages[key]
    else:
        return {}

def get_pagination_pages(current_page, total_pages, delta=1):
    pages = []
    for i in range(1, total_pages + 1):
        if i == 1 or i == total_pages or abs(i - current_page) <= delta:
            pages.append(i)
        elif pages[-1] != '...':
            pages.append('...')
    return pages
