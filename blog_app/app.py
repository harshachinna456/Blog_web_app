from datetime import datetime
from flask import Flask, redirect, render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable = False)
    content = db.Column(db.Text, nullable = False)
    author = db.Column(db.String(30), nullable = False, default = "Unknown")
    date_posted = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return 'Blog post' + str(self.id)



all_posts= [
    {
        'title':'ML',
        'content': 'machine learning is ability to learn from data and predict, without any hard coding',
        'author': 'Harsha'
    },
    {
        'title':'AI',
        'content': 'The ability of computer to mimic human brain',
        'author':'Yashwanth'
    },
    {
        'title':'PYTHON',
        'content': 'Python is interpreted language',
        'author': 'Mohith'
    
    },
    {
        'title':'NURALN ETWORKS',
        'content': 'These works like nurons in human brain',    
    },
]



@app.route("/")
def index():
    return render_template('index.html')


@app.route("/posts", methods=['GET', 'POST'])
def posts(): 
    all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
    return render_template('posts.html', posts=all_posts)



@app.route("/posts/new", methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')


@app.route("/posts/delete/<int:id>",)
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route("/posts/edit/<int:id>",methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)



if __name__ == '__main__':
    app.run(debug=True)