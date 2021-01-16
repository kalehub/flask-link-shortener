from flask import Flask, redirect,render_template, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlparse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///short_url.sqlite3'
app.secret_key = '78a42a49b52432320408842901314197206cbbe39d5cbc7194ff3345f98b03895e1743c62d0cea8b2e85df9f2ea0a19349397db14519e57ed77ce43996dc6ef7'

db = SQLAlchemy(app)
class Link(db.Model):
    url_id = db.Column('url_id', db.Integer, primary_key = True)
    original_url = db.Column(db.String(100))
    shorten_url = db.Column(db.String(100))
    def __init__(self,original_url, shorten_url):
        self.original_url = original_url
        self.shorten_url = shorten_url

@app.route('/')
def index():
    return render_template('add_url.html')

@app.route('/add_url/',methods=['POST', 'GET'])
def add_url():
    if request.method == 'POST':
        if not request.form['original_url'] or not request.form['shorten_url']:
            flash('fill all the field!')
            return redirect(url_for('index'))
        else:
            shorten_ = request.form['shorten_url']
            # check if shorten-link is already added into db
            # if already added -> error message
            url_taken = db.session.query(Link).filter(Link.shorten_url == shorten_).first()
            if (url_taken):
                flash('Shorten url is already taken!')
                return redirect(url_for('index'))
                
            # else -> proceed to adding
            else:
                link = Link(request.form['original_url'], request.form['shorten_url'])
                db.session.add(link)
                db.session.commit()
                flash('Shorten link is successfully created!')
                return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/<link>')
def find_url(link):
    record_available = db.session.query(Link.original_url).filter(Link.shorten_url == link).first()
    # go_to_link = 'http://'
    if (record_available):
        for r in record_available:
            p_goto = urlparse(r)
            print(p_goto)
            if p_goto.scheme == '':
                _goto = p_goto._replace(scheme='http')
                s_goto = str(_goto.scheme)+':'+'//'+str(_goto.path)
                return redirect(s_goto)
            else:
                return redirect(r)
            
        return r'_goto'
    else:
        return render_template('url_not_found.html')


if __name__ == '__main__':
    app.run(debug=True)