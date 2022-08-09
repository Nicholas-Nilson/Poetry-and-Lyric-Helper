# NEEDS: app name, SQL db location, site name, site description
from flask import Flask
from os.path import join, dirname, realpath

app = Flask(__name__)
app.config.update(
    SECRET_KEY='onomatopoeia',
    SITE_NAME = "Poetry and Lyric Word Helper",
    SITE_DESCRIPTION = "A search app for finding words matching any or all of; rhyme, syllables, scansion.",
    MYSQL_HOST = 'ZipCoders-MacBook-Pro.local',
    MYSQL_USER = 'nick',
    MYSQL_PASSWORD = 'nick123',
    MYSQL_DB = 'project_of_passion',
)