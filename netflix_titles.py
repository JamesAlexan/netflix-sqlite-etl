import sqlite3
import csv

conn = sqlite3.connect('netflix_titledb.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Director;
DROP TABLE IF EXISTS Casting;
DROP TABLE IF EXISTS Type;
DROP TABLE IF EXISTS Country;
DROP TABLE IF EXISTS Movie;

CREATE TABLE Director(
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE Casting(
    id INTEGER PRIMARY KEY,
    title TEXT UNIQUE
);

CREATE TABLE Type(
    id INTEGER PRIMARY KEY,
    title TEXT UNIQUE
);

CREATE TABLE Country(
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE Movie(
    show_id TEXT UNIQUE,
    type_id INTEGER,
    title TEXT UNIQUE,
    director_id INTEGER,
    cast_id INTEGER,
    country_id INTEGER,
    date_added TEXT,
    release_year INTEGER,
    rating TEXT,
    duration TEXT,
    listed_in TEXT,
    description TEXT
)
''')

handle = open('netflix_titles.csv', encoding='utf-8')
reader = csv.reader(handle)

count = 0
for pieces in reader:

    count = count + 1
    if count==1: continue

    if len(pieces)<12: continue

    show_id = pieces[0]
    type = pieces[1]
    title = pieces[2]
    director = pieces[3]
    cast = pieces[4]
    country = pieces[5]
    date_added = pieces[6]
    release_year = pieces[7]
    rating = pieces[8]
    duration = pieces[9]
    listed_in = pieces[10]
    description = pieces[11]

    print(show_id, type, director, cast, country, date_added, release_year, rating, duration, listed_in, description)

    cur.execute('''INSERT OR IGNORE INTO Type(title)
        VALUES (?)''',(type,))
    cur.execute('SELECT id FROM Type WHERE title = ?',(type,))
    type_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Director(name)
        VALUES (?)''',(director,))
    cur.execute('SELECT id FROM Director WHERE name = ?',(director,))
    director_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Casting(title)
        VALUES (?)''',(cast,))
    cur.execute('SELECT id FROM Casting WHERE title = ?',(cast,))
    cast_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Country(name)
        VALUES (?)''',(country,))
    cur.execute('SELECT id FROM Country WHERE name = ?',(country,))
    country_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Movie
        (show_id, type_id, title, director_id, cast_id, country_id, date_added, release_year, rating, duration, listed_in, description)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
        (show_id, type_id, title, director_id, cast_id, country_id, date_added, release_year, rating, duration, listed_in, description))

    conn.commit()


#SELECT Movie.title, Type.title, Director.name, Casting.title, Country.name from
#Movie join Type join Director join Casting join Country on Movie.type_id=Type.id and
#Movie.director_id=Director.id and Movie.cast_id=Casting.id and Movie.country_id=Country.id