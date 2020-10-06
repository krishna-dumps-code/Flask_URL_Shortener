from flask import Flask, render_template, redirect, url_for, flash, request, session, abort
import json
import os.path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "bhfk8ohxzx658dfig4"


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('home.html', codes=session.keys())


@app.route('/your-url', methods=['POST', 'GET'])
def your_url():
    if request.method == 'POST':
        urls = {}

        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

            if request.form['short_name'] in urls.keys():
                flash('This short name is taken. Please try another one!')
                return redirect('/')

        if 'URL' in request.form.keys():
            urls[request.form['short_name']] = {'url': request.form['URL']}
        else:
            f = request.files['file']
            full_name = request.form['short_name'] + \
                secure_filename(f.filename)
            f.save('D:/Projects/FLASK_URL SHORTENER/static/uploaded_files/' + full_name)
            urls[request.form['short_name']] = {'file': full_name}

        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
            session[request.form['short_name']] = True
        return render_template('your-url.html', short_name=request.form['short_name'])

    return redirect(url_for('home'))


@app.route('/<string:short_name>')
def redirect_to_url(short_name):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
        if short_name in urls.keys():
            if 'url' in urls[short_name].keys():
                return redirect(urls[short_name]['url'])
            else:
                return redirect(url_for('static', filename='uploaded_files/' + urls[short_name]['file']))

        return abort(404)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
