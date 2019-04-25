from flask import render_template, redirect, url_for
from flask_login import current_user
from . import main
from ..models import Comment,Film
from .forms import CommentForm
from .. import db

@main.route('/', methods=['GET','POST'])
def index():

    return render_template('index.html')

@main.route('/film', methods=['GET','POST'])
def film():
    film = Film.query.filter_by(id=1).first()
    form = CommentForm()
    if form.validate_on_submit():
        comment= Comment(body=form.body.data,
                         author=current_user._get_current_object())
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('.film'))
    comments = Comment.query.order_by(Comment.timestamp.desc()).all()
    return render_template('film.html',film=film, form=form, comments=comments)

@main.route('/top_films', methods=['GET','POST'])
def top_films():
    films=Film.query.filter_by(is_series=False).order_by(Film.score.desc())
    return render_template('Top_films.html', films=films)

@main.route('/top_series', methods=['GET','POST'])
def top_series():
    series=Film.query.filter_by(is_series=True).order_by(Film.score.desc())
    return render_template('Top_series.html', series=series)