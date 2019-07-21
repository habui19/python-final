from flask import render_template, url_for, flash, redirect, request, abort
from mymovies import app, db, bcrypt
from mymovies.forms import RegistrationForm, LoginForm, MovieForm, SearchForm
from mymovies.models import User, Movie
from flask_login import login_user, current_user, logout_user, login_required
from mymovies.movies import add_movies, show_rec
from mymovies.movie_match import search_movie

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login Successful', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/search", methods=["GET", "POST"])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        results = search_movie(form.titletype.data, form.genre.data)
        return render_template('results.html', title='Search Results', results=results)
    return render_template('search.html', title='Search', form=form)

@app.route("/movies")
@login_required
def movies():
    movies = Movie.query.filter_by(user=current_user).all()

    return render_template('movies.html', title='Movies', movies=movies)

@app.route("/movie/new", methods=["GET", "POST"])
@login_required
def new_movie():
    form = MovieForm()
    if form.validate_on_submit():
        try: 
            movie_data = add_movies(form.url.data, form.rating.data)
            movie = Movie(title=movie_data[0], genre=movie_data[1], imdb_rating=movie_data[2],
                            self_rating=movie_data[3], duration=movie_data[4], release_date=movie_data[5], user=current_user)
            db.session.add(movie)
            db.session.commit()
            flash(f'Movie added!', 'success')
            return redirect(url_for('movies'))
        except:
            flash('Cannot add this movie. Please try another one!', 'danger')

    return render_template('add_movie.html', title='Add Movie', form=form, legend='Add Movie')

@app.route("/sort/<string:order>")
def sort(order):
    movies = Movie.query.order_by(getattr(Movie,order).desc()).all()
    return render_template('movies.html', title='Movies', movies=movies)

@app.route("/recommend")
@login_required
def recommend():
    if Movie.query.first() is None:
        flash(f'Please add some movies first!', 'danger')
        return redirect(url_for('new_movie'))
    genre = db.session.execute('SELECT movie.genre, COUNT(movie.genre) AS most_frequent FROM movie WHERE self_rating >= 6 GROUP BY movie.genre ORDER BY most_frequent DESC LIMIT 1;').fetchone()
    if genre is None:
        flash(f'Please add some movies that you like!', 'danger')
        return redirect(url_for('new_movie'))
    recommendations = show_rec(genre[0])
    
    return render_template('recommendation.html', title='Recommendation', recommendations=recommendations, genre=genre[0])

@app.route("/movies/<int:movie_id>/delete")
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if movie.user != current_user:
        abort(403)
    db.session.delete(movie)
    db.session.commit()
    flash('Movie deleted', 'success')
    return redirect(url_for('movies'))