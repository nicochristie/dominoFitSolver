import os
from flask import url_for

class Config:
    HTML_TEMPLATE = 'index.html.j2'
    CSS_TEMPLATE = 'static/css/style.css'
    FILE_NAME = 'dominoFit.svg'
    FILE_PATH = 'static'
    START_COLS = 6
    START_ROWS = 6
