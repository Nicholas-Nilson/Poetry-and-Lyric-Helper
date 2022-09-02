from flask import Flask
import os


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.update(
    SECRET_KEY='onomatopoeia',
    SITE_NAME="Poetry and Lyric Word Helper",
    SITE_DESCRIPTION="A search app for finding words matching any or all of; rhyme, syllables, stresses.",
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir) + '/data/wordsdb.db'
)




