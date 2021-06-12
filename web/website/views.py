from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from injector import inject
import pandas as pd
import numpy as np
import time
import os
from .config import Config
from .knn_model import get_anime_rows, get_recommendation
from .embedding_model import InitializedModel
from .models import Bookmark
from .forms import RemoveBookmarkForm
from . import db

bp = Blueprint('views', __name__)


def load_df(full_df=True, sort_score=False):
    if full_df:
        df = pd.read_csv(os.path.join(Config.DATA_PATH, 'full_anime_info.csv'))
    else:
        df = pd.read_csv(os.path.join(Config.DATA_PATH, 'anime_info.csv'))

    if sort_score:
        df.sort_values('Score', ascending=False,
                       inplace=True, ignore_index=True)

    # fix missing scores
    fix_scores(df)
    return df


def fix_scores(df):
    df['Score'] = df['Score'].apply(lambda x: format(x, ".2f"))
    df['Score'].replace('nan', r'N/A', inplace=True)


def df_row2dict(df):
    # to change a single DataFrame row into dictionary format
    return df.to_dict(orient='records')[0]


def get_top_animes(top_k=48):
    df = load_df(full_df=False, sort_score=True)
    return df.head(top_k)


def find_bookmark(anime_id, return_bookmarked=False):
    # Only check for bookmark if user is logged in
    bookmark, bookmarked = None, None
    if current_user.is_authenticated:
        bookmark = Bookmark.query.filter_by(
            user_id=current_user.id, anime_id=anime_id).first()
        bookmarked = True if bookmark else False
    if return_bookmarked:
        return bookmarked
    return bookmark


def add_or_remove_bookmark(anime_id):
    bookmark = find_bookmark(anime_id)
    if bookmark:
        db.session.delete(bookmark)
        db.session.commit()
    else:
        bookmark = Bookmark(user_id=current_user.id, anime_id=anime_id)
        db.session.add(bookmark)
        db.session.commit()


@bp.route('/home')
@bp.route('/')
def home():
    df = get_top_animes()
    return render_template('home.html', anime_info_df=df)


@bp.route('/about')
def about():
    return render_template('about.html')


@bp.route('/query')
def search():
    # Convert to string to only search by name
    anime_name = request.args.get('anime_name', type=str)
    print(f"\n[INFO] Anime to search for: {anime_name}\n", )
    df = load_df()
    df = get_anime_rows(df, anime_name)
    # To replace unknown values into a max value to sort by popularity
    df['Popularity'].replace(0, 20000, inplace=True)
    df.sort_values('Popularity', ignore_index=True, inplace=True)
    return render_template('search.html', anime_info_df=df)


@bp.route('/anime/<int:anime_id>', methods=['GET', 'POST'])
def anime(anime_id):
    if request.method == "GET":
        df = load_df()
        df = df.loc[df['MAL_ID'] == anime_id]
        anime_info = df_row2dict(df)

        bookmarked = find_bookmark(anime_id, return_bookmarked=True)

        return render_template('anime.html', anime_info=anime_info, bookmarked=bookmarked)

    if request.method == "POST":
        add_or_remove_bookmark(anime_id)
        return redirect(url_for('views.anime', anime_id=anime_id))


@inject
@bp.route('/recommend/<int:anime_id>', methods=['GET', 'POST'])
def recommend(anime_id, model: InitializedModel):
    # Using dependency injection resulted in much faster loading times
    if request.method == "GET":
        start_time = time.time()
        # anime_row, rec_df = get_recommendation(anime_id, k=21)
        anime_row, rec_df = model.get_recommendation(anime_id, k=30)
        fix_scores(rec_df)
        time_elapsed = time.time() - start_time
        print(f"[INFO] Time elapsed for recommendation: "
              f"{time_elapsed:.2f} seconds.\n")
        anime_info = df_row2dict(anime_row)
        rec_df.reset_index(drop=True, inplace=True)

        bookmarked = find_bookmark(anime_id, return_bookmarked=True)

        return render_template('recommend.html',
                               anime_info=anime_info,
                               bookmarked=bookmarked,
                               rec_df=rec_df)

    if request.method == "POST":
        add_or_remove_bookmark(anime_id)
        return redirect(url_for('views.recommend', anime_id=anime_id))


@bp.route('/bookmarks', methods=['GET', 'POST'])
@login_required
def bookmarks():
    df = load_df(full_df=False)
    remove_bookmark_form = RemoveBookmarkForm()
    if request.method == "GET":
        page = request.args.get('page', 1, type=int)
        per_page = 10
        bookmarks = Bookmark.query.filter_by(user_id=current_user.id).order_by(
            Bookmark.date_created.desc()).paginate(page=page, max_per_page=per_page)

        # Create a dictionary to sort the df by the order of the bookmarks
        anime_ids_dict = {bm.anime_id: i for i,
                          bm in enumerate(bookmarks.items)}
        bookmark_df = df.loc[df['MAL_ID'].isin(anime_ids_dict.keys())].copy()
        bookmark_df['Order'] = bookmark_df['MAL_ID'].map(anime_ids_dict)
        bookmark_df.sort_values('Order', inplace=True)

        # Create index to show the each bookmark number in the sorted order
        start_idx = (page - 1) * per_page
        end_idx = (page - 1) * per_page + len(bookmark_df)
        bookmark_df.index = np.arange(start_idx, end_idx)

        # bookmark_df.reset_index(drop=True, inplace=True)
        return render_template('bookmarks.html',
                               remove_bookmark_form=remove_bookmark_form,
                               df=bookmark_df,
                               bookmarks=bookmarks)

    if request.method == "POST":
        # Get the page to redirect to the current page after deleting bookmark
        page = request.args.get('page', 1, type=int)
        df_length = request.form.get('df_length', type=int)
        # redirect to the first page if there is no more bookmark
        #   at the current page
        if df_length == 1:
            page = 1

        anime_id = request.form.get('anime_id_to_remove', type=int)
        bookmark = find_bookmark(anime_id)
        if bookmark:
            print(f"\nRemoving bookmark for Anime ID: {anime_id}\n")
            db.session.delete(bookmark)
            db.session.commit()
            anime_name = df.loc[df['MAL_ID'] == anime_id, 'Name'].values[0]
            flash(f'Removed "{anime_name}" from bookmarks.',
                  category='success')
        return redirect(url_for('views.bookmarks', page=page))
