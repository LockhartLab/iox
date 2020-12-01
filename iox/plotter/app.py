"""

"""

# TODO 0. error handling
# TODO 1. syntax highlighting
# TODO 2. load query
# TODO 3. save plots
# TODO 4. smart indentation
# TODO 5. pop out plots?
# TODO 6. history?
# TODO 7. stand-alone application? electron?

from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from glob import iglob
from hashlib import md5
import plotly.express as px
import os
from iox.google import BigQuery

# Some variables for uploading files
ALLOWED_EXTENSIONS = {'sql'}

# Create initial connection to Flask
app = Flask(__name__)
# app.config['SESSION_TYPE'] = 'filesystem'

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'3\x8eYn\x94\xe5\xdb\xba\xa5\xd6\x910\xe6fv\xab'

#
bq = BigQuery()


# Check that the file we upload is allowed
def allowed_file(fname):
    return '.' in fname and fname.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Index
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Save the file securely
        # file = request.files.get('namdlog', None)
        # if file is None or not allowed_file(file.filename):
        #     return redirect(request.url)
        # fname = os.path.join('static', secure_filename(file.filename))
        # file.save(fname)

        # Get arguments
        sql = request.form.get('sql', None)
        if sql is None:
            return redirect(request.url)

        # Run query
        df = bq.query(sql)

        # Product plot
        html = px.line(df).to_html()

        # Return
        return jsonify({'plot_html': html})

    # noinspection PyUnresolvedReferences
    return render_template('index.html')


# Run the app
if __name__ == '__main__':
    # Run
    app.run()
