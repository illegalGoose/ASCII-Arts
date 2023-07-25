from flask import Flask, request, Response, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import jinja2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ascii.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Art(db.Model):
    title = db.Column(db.String(100), primary_key = True) #100 - максимум символов
    art = db.Column(db.Text, primary_key = True)
    created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f"<art {self.id}>"

@app.route("/")  
def render_front(title="", art="", error=""):
    t = jinja_env.get_template("front.html")
    arts = Art.query.order_by(Art.created.desc()).all()
    return t.render(title=title, art=art, error=error, arts=arts)      

@app.route("/", methods=['GET', 'POST'])
def form():
    t = jinja_env.get_template("front.html")
    if request.method == 'POST':
        title = request.form["title"]
        art = request.form["art"]
        if title and art:
            a = Art(title=title, art=art)
            db.session.add(a)
            db.session.commit()
            return redirect("/")
        else:
            error = "We need both a title and some artwork"
            return t.render(error=error, title=title, art=art) 
    return t.render()

if __name__ == "__main__":
    app.run()