from flask import render_template, redirect, url_for
from flask_login import current_user
from . import main
from ..models import Comment,Film,Directors,Actors, Film_directors,Film_actors
from .forms import CommentForm
from .. import db

@main.route('/', methods=['GET','POST'])
def index():

    return render_template('index.html')

@main.route('/film/<int:id>', methods=['GET','POST'])
def film(id):
    film = Film.query.filter_by(id=id).first()
    film_directors=Film_directors.query.filter_by(film_id=id).all()
    directors=[]
    for fd in film_directors:
        director=Directors.query.filter_by(id=fd.director_id).first()
        directors.append(director)
    film_actors=Film_actors.query.filter_by(film_id=id).all()
    actors=[]
    for fa in film_actors:
        actor= Actors.query.filter_by(id=fa.actor_id).first()
        actors.append(actor)

    form = CommentForm()
    if form.validate_on_submit():
        comment= Comment(body=form.body.data,
                         author=current_user._get_current_object(), film_id=id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('.film',id=id))
    comments = Comment.query.filter_by(film_id=id).order_by(Comment.timestamp.desc()).all()
    return render_template('film.html',film=film, form=form, comments=comments, directors=directors, actors=actors)

@main.route('/top_films', methods=['GET','POST'])
def top_films():
    films=Film.query.all()
    return render_template('Top_films.html', films=films)

@main.route('/top_series', methods=['GET','POST'])
def top_series():
    series=Film.query.filter_by(is_series=True).all()
    return render_template('Top_series.html', series=series)