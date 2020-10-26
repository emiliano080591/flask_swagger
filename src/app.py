from flask import Flask, jsonify,render_template,request
from flask_socketio import SocketIO,emit,disconnect
from flasgger import Swagger,swag_from

async_mode=None
app = Flask(__name__)
app.config['SECRET_KEY']='secret'
socketio=SocketIO(app,async_mode=async_mode)

template = {
  "swagger": "2.0",
  "info": {
    "title": "My API",
    "description": "API for my data",
    "contact": {
      "responsibleOrganization": "ME",
      "responsibleDeveloper": "Me",
      "email": "me@me.com",
      "url": "www.me.com",
    },
    "termsOfService": "http://me.com/terms",
    "version": "0.0.1"
  },
  "host": "mysite.com",  # overrides localhost:500
  "basePath": "/api",  # base bash for blueprint registration
  "schemes": [
    "http",
    "https"
  ],
  "operationId": "getmyData"
}
swagger = Swagger(app,template=template)

@app.route('/')
def index():
  return render_template('index.html',async_mode=socketio.async_mode)

@app.route('/colors/<palette>/')
@swag_from('colors.yml')
def colors(palette):
    all_colors = {
        'cmyk': ['cian', 'magenta', 'yellow', 'black'],
        'rgb': ['red', 'green', 'blue']
    }
    if palette == 'all':
        result = all_colors
    else:
        result = {palette: all_colors.get(palette)}

    return jsonify(result)

"""
Métodos que manejan las conexiones de websockets con socket io
"""

#Método que recibe la primera conexion con el cliente
@socketio.on('connect', namespace='/test')
def test_connect():
  #print(request.sid)
  emit('my response', {'data': 'Connected'})

#Método que responde a un cliente en particular
@socketio.on('my event', namespace='/test')
def test_message(message):
  emit('my response', {'data': message['data']})

#Método que responde a todos los clientes(broadcast)
@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
  emit('my response', {'data': message['data']}, broadcast=True)

#Método que desconecta a un cliente
@socketio.on('disconnect', namespace='/test')
def test_disconnect():
  disconnect('/test')
  print('Client disconnected ')

#Método que muestra los errores de ejecucion de socket io
@socketio.on_error(namespace='/test')
def chat_error_handler(e):
    print('An error has occurred: ' + str(e))

if __name__ == '__main__':
    socketio.run(app,debug=True)