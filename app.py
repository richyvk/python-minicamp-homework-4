from flask import Flask, render_template, request, redirect, url_for
import records

app = Flask(__name__)

DB = 'sqlite:///database.db'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/movie/', methods=['GET', 'POST'])
def movie():
    if request.method == 'POST':

        m_title = request.form.get('title')
        m_year = request.form.get('year')
        m_genre = request.form.get('genre')
        m_description = request.form.get('description')
        m_rating = request.form.get('rating')
        print(m_title, m_year, m_genre, m_description, m_rating)

        try:
            print("Adding record")
            db = records.Database(DB)
            print("Connected to DB")
            query = ('INSERT INTO movies (title, year, genre, '
                     'description, rating) VALUES(:title, :year, '
                     ':genre, :description, :rating)')
            print(query)
            db.query(query, title=m_title, year=m_year, genre=m_genre,
                     description=m_description, rating=m_rating)
            print("Success: record added")
        except:
            db.rollback()
            print("Error adding record")
        finally:
            return redirect(url_for('index'))
    else:
        return render_template('add-movie.html')
