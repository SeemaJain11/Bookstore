from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)

@app.route('/')
def home():
    books = Book.query.all()
    return render_template('home.html', books=books)

@app.route('/create', methods=['GET', 'POST'])
def create_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']
        price = float(request.form['price'])  # Convert string to float


        new_book = Book(title=title, author=author, description=description, price=price)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_book.html')

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
