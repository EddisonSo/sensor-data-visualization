from map_server import app as map_app


app = map_app 

if __name__ == "__main__":
    app.run(host='0.0.0.0')
