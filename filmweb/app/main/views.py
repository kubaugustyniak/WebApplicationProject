
from flask import render_template, redirect, url_for, request, Response, jsonify
from flask_login import current_user
from . import main
from ..models import Comment,Film,Directors,Actors, Film_directors,Film_actors, Score
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
    films=Film.query.filter_by(is_series=False).all()
    return render_template('Top_films.html', films=films)

@main.route('/top_series', methods=['GET','POST'])
def top_series():
    series=Film.query.filter_by(is_series=True).all()
    return render_template('Top_series.html', series=series)


@main.route('/rating/<int:id>', methods=['GET','POST'])
def rating(id):
    score=Score()
    score.filmscore =request.values['value']
    score.film_id=id
    score.user_id=current_user.id
    db.session.add(score)
    db.session.commit()

    film_rates=Score.query.filter_by(film_id=id).all()
    sum = 0
    for rate in film_rates:
        sum += rate.filmscore

    avg=sum/len(film_rates)

    film=Film.query.filter_by(id=id).first()
    film.score=avg

    db.session.add(film)
    db.session.commit()

    film = Film.query.filter_by(id=id).first()

    return jsonify(film.score)



@main.route('/post_title', methods=['GET','POST'])
def search():
    if request.method == "POST":

        text = request.form['text']

        if not text:
            text=" ";

        return redirect(url_for('main.search_films', title=text))




@main.route('/search_films/<string:title>', methods=['GET','POST'])
def search_films(title):
        films = Film.query.filter(Film.title.like("%{0}%".format(title))).all()

        if len(films)==0:
          empty=True
        else:
            empty=False

        return render_template('search_films.html', films=films,empty=empty)

