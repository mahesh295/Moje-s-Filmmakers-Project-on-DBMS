from flask import Flask, render_template, request, redirect, Response, url_for
import pymysql
import csv

app = Flask(__name__)
# Database connection function
def get_connection():
    return pymysql.connect(
        host='localhost',
        port=3306,  # enter your localhost port Number
        user='root', # enter your user name
        password='password', # enter your password
        database='mojies' #enter your DATABASE where you created tables
    )

# Home page showing all movie details
@app.route('/')
def index():
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT m.title, c.hero, c.heroine, d.name, mc.box_office
        FROM MovieDetails m
        JOIN CastInfo c ON m.movie_id = c.movie_id
        JOIN DirectorInfo d ON m.director_id = d.director_id
        JOIN MovieCollections mc ON m.movie_id = mc.movie_id
    """)
    data = cur.fetchall()
    con.close()
    return render_template('index.html', data=data)

# View director details
@app.route('/directors')
def directors():
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT d.name, d.age, d.awards, d.total_movies, COUNT(m.movie_id)
        FROM DirectorInfo d
        LEFT JOIN MovieDetails m ON d.director_id = m.director_id
        GROUP BY d.director_id
    """)
    data = cur.fetchall()
    con.close()
    return render_template('directors.html', data=data)

# Box office report per director
@app.route('/report')
def report():
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT d.name, SUM(mc.box_office) AS total
        FROM DirectorInfo d
        JOIN MovieDetails m ON d.director_id = m.director_id
        JOIN MovieCollections mc ON m.movie_id = mc.movie_id
        GROUP BY d.name ORDER BY total DESC 
    """)
    data = cur.fetchall()
    con.close()
    return render_template('report.html', data=data)

# Add a new movie entry
@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        movie = request.form
        con = get_connection()
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO MovieDetails VALUES (%s, %s, %s, %s)", (
                movie['movie_id'], movie['title'], movie['director_id'], movie['release_year']
            ))
            cur.execute("INSERT INTO CastInfo VALUES (%s, %s, %s, %s)", (
                movie['cast_id'], movie['movie_id'], movie['hero'], movie['heroine']
            ))
            cur.execute("INSERT INTO MovieCollections VALUES (%s, %s, %s)", (
                movie['collection_id'], movie['movie_id'], movie['box_office']
            ))
            con.commit()
        except Exception as e:
            con.rollback()
            return f"Error: {e}"
        finally:
            con.close()
        return redirect('/')
    return render_template('add_movie.html')

@app.route('/leftjoin')
def leftjoin():
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT m.title, mc.box_office
        FROM MovieDetails m
        LEFT JOIN MovieCollections mc ON m.movie_id = mc.movie_id
    """)
    data = cur.fetchall()
    con.close()
    return render_template('leftjoin.html', data=data)

@app.route('/rightjoin')
def rightjoin():
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT m.title, c.hero, c.heroine, d.name, mc.box_office, m.movie_id
        FROM MovieDetails m
        JOIN CastInfo c ON m.movie_id = c.movie_id
        JOIN DirectorInfo d ON m.director_id = d.director_id
        JOIN MovieCollections mc ON m.movie_id = mc.movie_id
    """)
    data = cur.fetchall()
    con.close()
    return render_template('rightjoin.html', data=data)

@app.route('/delete_movie/<int:movie_id>')
def delete_movie(movie_id):
    con = get_connection()
    cur = con.cursor()
    try:
        # Delete from MovieCollections first due to FK constraints
        cur.execute("DELETE FROM MovieCollections WHERE movie_id = %s", (movie_id,))
        cur.execute("DELETE FROM CastInfo WHERE movie_id = %s", (movie_id,))
        cur.execute("DELETE FROM MovieDetails WHERE movie_id = %s", (movie_id,))
        con.commit()
    except Exception as e:
        con.rollback()
        return f"Error deleting: {e}"
    finally:
        con.close()
    return redirect('/')


@app.route('/export_csv')
def export_csv():
    con = get_connection()
    cur = con.cursor()
    cur.execute("""
        SELECT m.title, c.hero, c.heroine, d.name, mc.box_office
        FROM MovieDetails m
        JOIN CastInfo c ON m.movie_id = c.movie_id
        JOIN DirectorInfo d ON m.director_id = d.director_id
        JOIN MovieCollections mc ON m.movie_id = mc.movie_id
    """)
    data = cur.fetchall()
    con.close()

    def generate():
        yield 'Movie,Hero,Heroine,Director,Box Office (Cr)\n'
        for row in data:
            yield ','.join(map(str, row)) + '\n'

    return Response(generate(), mimetype='text/csv',
                    headers={"Content-Disposition": "attachment;filename=movies_report.csv"})

if __name__ == '__main__':
    app.run(debug=True)
