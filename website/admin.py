from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from sqlalchemy import and_, func
from flask_login import logout_user
from .movies_requests import update_popular_movies, update_popular_series
from .models import User, RandomMovie, SaveMovie
from . import db

ADMIN_CREDENTIALS = {'admin': 'parola123'}


admin = Blueprint("admin", __name__)


@admin.route('/adminpage')
def adminpage():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.adminlogin'))

    logout_user()
    page = get_safe_page()

    users_on_page, total_pages = paginate_users(int(page))
    pages = get_pagination_pages(int(page), total_pages)

    return render_template('admin_index.html',
                           users= users_on_page,
                           total_pages = total_pages,
                           pages= pages,
                           current_page = int(page))

@admin.route('/admin/edit', methods= ['GET','POST'])
def edit_user():
    if request.method == 'POST':
        user_id = request.args.get('user_id')
        user_to_update = db.get_or_404(User, user_id)

        name = request.form.get('name')
        email = request.form.get('email')
        option = request.form.get('confirm')

        if name:
            user_to_update.name = name
        if email:
            user_to_update.email = email

        user_to_update.confirmation = bool(int(option))
        db.session.commit()
        flash('Update was successful.')
        return redirect(url_for('admin.adminpage'))

    user_id = request.args.get('user_id')
    user = db.get_or_404(User, user_id)

    return render_template('edit_user.html', user = user)

@admin.route('/admin/clean-users')
def clean_users():
    from datetime import datetime
    today = datetime.now().date()

    unconfirmed_users = db.session.execute(
        db.select(User.id).where(
            and_(
                User.confirmation.is_(False),
                func.date(User.date_created) != today
            )
        )
    ).scalars().all()

    if not unconfirmed_users:
        flash("No unconfirmed users found.")
        return redirect(url_for('admin.adminpage'))

    db.session.query(RandomMovie).filter(RandomMovie.movie_owner.in_(unconfirmed_users)).delete(
        synchronize_session=False)
    db.session.query(SaveMovie).filter(SaveMovie.user_who_saved_movie.in_(unconfirmed_users)).delete(
        synchronize_session=False)

    db.session.query(User).filter(User.id.in_(unconfirmed_users)).delete(synchronize_session=False)

    db.session.commit()
    flash(f"{len(unconfirmed_users)} unconfirmed user(s) successfully deleted.")
    return redirect(url_for('admin.adminpage'))


@admin.route('/admin/update', methods= ['GET'])
def update():
    updates = request.args.get('update')
    if updates == 'movies':
        update_popular_movies()
        flash('Movies Trending Successful updated')
    elif updates == 'series':
        update_popular_series()
        flash('Series Trending Successful updated')
    return redirect(url_for('admin.adminpage'))


@admin.route('/admin/remove_account', methods= ['GET','POST'])
def remove_account():
    email = request.form.get("email") or request.args.get("email")
    if email:
        remove_user(email)
    return redirect(url_for('admin.adminpage'))


def remove_user(email):
    user = db.session.execute(db.select(User).where(User.email == email)).scalar()
    if user:

        db.session.query(RandomMovie).filter_by(movie_owner=user.id).delete()
        db.session.query(SaveMovie).filter_by(user_who_saved_movie=user.id).delete()

        db.session.delete(user)
        db.session.commit()
        flash(f"User {user.name} (ID: {user.id}, email: {user.email}) was successfully deleted.")
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


def paginate_users(page, per_page=10):
    users = db.session.execute(db.select(User).order_by(User.email)).scalars().all()
    if users:
        total_pages = (len(users) - 1) // per_page + 1

        if page < 1 or page > total_pages:
            page = 1

        start = (page - 1) * per_page
        end = start + per_page
        return users[start:end], total_pages
    else:
        return [], 1


def get_pagination_pages(current_page, total_pages, delta=1):
    pages = []
    for i in range(1, total_pages + 1):
        if i == 1 or i == total_pages or abs(i - current_page) <= delta:
            pages.append(i)
        elif pages[-1] != '...':
            pages.append('...')
    return pages


def get_safe_page():
    try:
        return int(request.args.get('page', 1))
    except (ValueError, TypeError):
        return 1