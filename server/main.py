# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
