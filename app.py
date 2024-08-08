from flask import Flask, render_template, request, jsonify, redirect, Response
import psycopg2
import helpers

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="milenbelanger",
        user="milenbelanger",
        password="")
    return conn

@app.get("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM books;')
    books = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', books=books)

@app.get("/<key>")
def redirect_to_long(key):
    errDict = {}
    conn = get_db_connection()
    cur = conn.cursor()
    #Check if url already present in table
    query = "SELECT * FROM urls WHERE key = %s;"
    cur.execute(query, (key,))
    urls = cur.fetchall()
    if len(urls) == 0:
        cur.close()
        conn.close()
        return jsonify({"error": f"Url Not Found"}), 404
    url = urls[0][1]
    return redirect(url)

@app.post("/")
def post():
    # Get url to be shortened
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data received"}), 400
    if not data.get("url"):
        return jsonify({"error": "Missing field: url"}), 400
    url = data["url"]

    # Connect To Database
    conn = get_db_connection()
    cur = conn.cursor()

    #Check if url already present in table
    query = "SELECT * FROM urls WHERE url = %s;"
    cur.execute(query, (url,))
    urls = cur.fetchall()
    
    
    errDict = {}
    key = None
    HOST = "http://127.0.0.1:5000/"
    # if url already present
    if urls:
        if len(urls) > 1:
            errDict.update({"error": f"More than one matching url \n{urls}"})
        else:
            key = urls[0][2]
    #if url not present
    else:
        #generate key
        key = helpers.generate_key()

        #insert key, url into db
        query = 'INSERT INTO urls (key, url) VALUES (%s, %s);' 
        cur.execute(query, (key, url,))
        conn.commit()
        
        #check if key, url has been added
        query = "SELECT * FROM urls WHERE url = %s;"
        cur.execute(query, (url,))
        urls = cur.fetchall()

        #if url has not been added
        if not urls:
            errDict.update({"error": f"Could not add to the database"})
        elif len(urls) > 1:
            errDict.update({"error": f"Added to database multiple times"})
        #if url has been added Successfully
        else:
            url = urls[0][1]
            key = urls[0][2]
    
    cur.close()
    conn.close()
    if errDict:
        return jsonify(errDict), 500
    else:
        return jsonify({"long_url": url, "key": key, "short_url": HOST+key}), 200
    
@app.route("/<key>", methods=["DELETE"])
def delete_key(key):
    errDict = {}
    conn = get_db_connection()
    cur = conn.cursor()

    query = "SELECT * FROM urls WHERE key = %s;"
    cur.execute(query, (key,))
    urls = cur.fetchall()
    if len(urls) == 0:
        cur.close()
        conn.close()
        return jsonify({"error": f"Url Not Found"}), 404
    query = "DELETE FROM urls WHERE key = %s;"
    cur.execute(query, (key,))
    conn.commit()
    return Response(status=200)