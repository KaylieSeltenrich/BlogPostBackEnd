import mariadb
from flask import Flask, request, Response
import json 
import dbcreds
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/blog', methods=['GET','POST','PATCH','DELETE'])
def blogpost():
      
    if request.method == 'GET':
        conn = None
        cursor = None
        items = None
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM blogposts")
            items = cursor.fetchall()

        except Exception as error:
            print("Something went wrong: ")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(items != None):
                return Response(json.dumps(items, default=str), mimetype="application/json", status=200)
            else: 
                return Response("Something went wrong!", mimetype="text/html", status=500)
    
    elif request.method == 'POST':
        conn = None
        cursor = None
        blogpost_content = request.json.get("content")
        blogpost_creator = request.json.get("created_by")
        rows = None
        
        try:
            conn = mariadb.connect(host=dbcreds.host, password=dbcreds.password, user=dbcreds.user, port=dbcreds.port, database=dbcreds.database)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO blogposts(content,created_by) VALUES (?,?)", [blogpost_content, blogpost_creator])
            conn.commit()
            rows = cursor.rowcount
        
        except Exception as error:
            print("Something went wrong (this is lazy): ")
            print(error)
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close()
            if(rows == 1):
                return Response("Blog Post Created", mimetype="text/html", status=201)
            else:
                return Response("Something went wrong!", mimetype="text/html", status=500)
    
    elif request.method == 'PATCH':
        
