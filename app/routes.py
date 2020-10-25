from flask import render_template, flash, redirect, url_for, jsonify, make_response
from app import app
from datetime import date
from app.forms import LoginForm, EditWordlistForm, AddWordlistForm
from flask_login import current_user, login_user
from app.models import User, Wordlist, Word
from flask_login import logout_user, current_user, logout_user, login_required
from flask import request
from werkzeug.urls import url_parse
from flask_login import login_required
from app import db

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/')
@app.route('/index', methods=["GET", "POST"])
@login_required
def index():
    form=AddWordlistForm()
    if form.validate_on_submit():
        wordlist=Wordlist(title=request.form.get('title'), learner=current_user)
        db.session.add(wordlist)
        db.session.commit()
        print(request.form)
        flash('New wordlist added')
        return redirect(url_for('index'))
    wordlists = current_user.wordlists.all()
    return render_template('index.html',title='Home', wordlists=wordlists, form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page=request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page=url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html',title="Sign In", form=form)

@app.route('/edit/<int:wordlist_id>', methods=['GET', 'POST'])
@login_required
def edit(wordlist_id):
    wordlist = Wordlist.query.get_or_404(wordlist_id)
    form=EditWordlistForm()
    #form.title.data = wordlist.title
    if request.method == 'POST' and form.validate_on_submit():
        wordlist.title = form.title.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('index'))
    elif request.method=='GET':
        form.title.data=wordlist.title
    return render_template('edit.html', title="Update Wordlist Title", form=form, wordlist=wordlist)

@app.route('/index/<int:wordlist_id>', methods=["GET", "POST"])
@login_required
def wordlists(wordlist_id):
    wordlist = Wordlist.query.get_or_404(wordlist_id)
    wl_words = wordlist.words 
    print(wl_words)
    if wordlist:
        return render_template('wordlist.html', title=wordlist.title, wordlist=wordlist, wl_words=wl_words)
    else:
        msg = 'No wordlists were found'
        return render_template('wordlist.html', msg=msg)

@app.route('/delete_wordlist/<int:wordlist_id>', methods=["GET", "POST"])
@login_required
def delete_wordlist(wordlist_id):
    wordlist=Wordlist.query.get_or_404(wordlist_id)
    if wordlist.learner != current_user:
        abort(403)
    db.session.delete(wordlist)
    db.session.commit()
    flash("Wordlist deleted!", "success")
    return redirect(url_for('index'))
   
@app.route('/search', methods=["GET", "POST"])
@login_required
def search():
    if request.method == "GET":
        wordlist_collection = current_user.wordlists.all()
        return render_template("search.html", wordlist_collection=wordlist_collection)
    else:
        selected_wl=request.form.get('my_wordlist')
        print("post method here")
        #target_wl=Wordlist.query.get(int(selected_wl))
        # print(target_wl)
        # search_word=request.form.get('search-word')
        # print("word that was searched", search_word)
        # print("id of wordlist", int(selected_wl))
        req = request.get_json()
        print("my word attributes are:", req)
        print(req['name'])
        print(req['type'])
        print(req['definition'])
        print(req['selected_wordlist'])
        wl = Wordlist.query.get(int(req['selected_wordlist']))
        print(wl)
        w = Word(name=req['name'], part=req['type'], definition=req['definition'])
        wl.words.append(w)
        db.session.commit()
        return redirect(url_for("index"))

@app.route('/delete_word/<int:word_id>', methods=["GET", "POST"])
@login_required
def delete_word(word_id):
    word=Word.query.get_or_404(word_id)
    db.session.delete(word)
    db.session.commit()
    flash("Word deleted!", "success")
    return redirect(url_for('index'))

    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))