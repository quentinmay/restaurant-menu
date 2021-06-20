from flask import Flask, render_template, request, jsonify
import json
app = Flask(__name__, template_folder="public")

@app.route('/', methods=['POST', 'GET'])
def index():
	if request.method == 'GET':
		return render_template('tacoshop.html')
	elif request.method == 'POST':
		jsondata = request.get_json(force=True) 
		return "Data received: " + str(jsondata)

@app.route('/<filename>')
def open_file(filename):
		if filename.endswith('.json'):
			with open('public/' + filename) as jsonfile:
				jsondata = json.load(jsonfile)

			return jsonify(jsondata)
			#return render_template(filename)
		else:
			return render_template(filename + '.html')


if __name__ == "__main__":
    app.run(debug=True)
