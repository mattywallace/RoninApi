from flask import Flask, jsonify 
import models 
DEBUG=True 
PORT=8000

app = Flask(__name__)


@app.route('/json-test')
def testjson():
	return jsonify(['matthew', 'mark', 'luke', 'john'])


if __name__ == '__main__':
	models.initialize()
	app.run(debug=DEBUG, port=PORT)