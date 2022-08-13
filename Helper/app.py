# NEEDS: app name, SQL db location, site name, site description
from flask import Flask, render_template, request, url_for, redirect
import os
from os.path import join, dirname, realpath

basedir = os.path.abspath(os.path.dirname(__file__))
# print(basedir)
# print('sqlite:///' + os.path.join(basedir) + '/data/words.db')
app = Flask(__name__)
app.config.update(
    SECRET_KEY='onomatopoeia',
    SITE_NAME="Poetry and Lyric Word Helper",
    SITE_DESCRIPTION="A search app for finding words matching any or all of; rhyme, syllables, stresses.",
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir) + '/data/wordsdb.db'
)
