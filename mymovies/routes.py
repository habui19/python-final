from flask import render_template, url_for, flash, redirect, request, abort
from mymovies import app, db, bcrypt
from mymovies.forms import RegistrationForm, LoginForm, MovieForm
from mymovies.models import User, Movie
from flask_login import login_user, current_user, logout_user, login_required
from mymovies.movies import add_movies, show_rec

@app.route("/")
@app.route("/home")
def home():
    try:
        movies = Movie.query.filter_by(user=current_user).all()
    except:
        flash('Please Log in', 'danger')
        return redirect(url_for('login'))
    return render_template('home.html', title='Home', movies=movies)

@app.route("/about")
def about():
    return render_template('about.html', title='About')

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
    return redirect(url_for('about'))

@app.route("/movie/new", methods=["GET", "POST"])
@login_required
def new_movie():
    form = MovieForm()
    if form.validate_on_submit():
        movie_data = add_movies(form.url.data, form.rating.data)
        movie = Movie(title=movie_data[0], genre=movie_data[1], imdb_rating=movie_data[2],
                        self_rating=movie_data[3], duration=movie_data[4], release_date=movie_data[5], user=current_user)
        try: 
            db.session.add(movie)
            db.session.commit()
            flash(f'Movie added!', 'success')
            return redirect(url_for('home'))
        except:
            flash(f'You already added this movie!', 'danger')
    return render_template('add_movie.html', title='Add Movie', form=form, legend='Add Movie')

@app.route("/sort/<string:order>")
def sort(order):
    movies = Movie.query.order_by(getattr(Movie,order).desc()).all()
    return render_template('home.html', title='Home', movies=movies)

@app.route("/recommend")
def recommend():
    genre = db.session.execute('SELECT movie.genre, COUNT(movie.genre) AS most_frequent FROM movie WHERE self_rating > 6 GROUP BY movie.genre ORDER BY most_frequent DESC LIMIT 1;').fetchone()
    recommendations = show_rec(genre[0])
    
    return render_template('recommendation.html', title='Recommendation', recommendations=recommendations)


@app.route("/note/<int:note_id>")
def note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)
    return render_template("note.html", title=note.title, note=note)

@app.route("/note/<int:note_id>/update", methods=["GET", "POST"])
@login_required
def update_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)
    form = NoteForm()
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()
        flash('Note updated!', 'success')
        return redirect(url_for('note', note_id=note.id))
    elif request.method == "GET":
        form.title.data = note.title
        form.content.data = note.content
    return render_template('create_note.html', title='Update Note', form=form, legend='Update Note')

@app.route("/note/<int:note_id>/delete", methods=["POST"])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted', 'success')
    return redirect(url_for('home'))

@app.route("/note/<int:note_id>/questions", methods=["GET", "POST"])
@login_required
def questions(note_id):
    note = Note.query.get_or_404(note_id)
    if note.author != current_user:
        abort(403)
    questions = generate(note.content)
    return render_template("note.html", title=note.title, note=note, questions=questions)