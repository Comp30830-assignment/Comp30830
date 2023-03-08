

from flask import Flask, render_template
# app=Flask(__name__)

# @app.route("/")
# def hello():
#     return "Hello World!!!!"

# if __name__=="__main__":
#     app.run(debug=True)
    
    
app=Flask(__name__, static_url_path='')
@app.route('/page')
def page():
    #return app.send_static_file('index.html')#only use in the static files
    #return "Hello!!!!cat!!!!"
    return render_template('test_part.html')

@app.route('/')
def index():
#     return "Hello!!!!cat!!!!"
      return '<h1>Hi!</h1>'

#這句話要放在最後才能運作整個程序
if __name__=="__main__":
    app.run(debug=True)
    


# @app.route('/')
# def contact():
#     return app.send_static_file('/sample/index.html')

# @app.route('/contact')
# def contact():
#     return app.send_static_file('/sample/index.html')

# @app.route('/stations')
# def stations():
#     return list of stations

# @app.route('/station/<int:station_id>')
# def station(station_id):
#     return 'Retrieving info for Station: {}'.format(station_id)