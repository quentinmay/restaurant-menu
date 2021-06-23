from flask import Flask, render_template, request, jsonify, send_file
import json
import base64
from PIL import Image
import io
import os
import stripe
# refer from: https://stripe.com/docs/legacy-checkout/flask
# bank account: https://stripe.com/docs/testing
# sudo PUBLISHABLE_KEY=pk_test_TYooMQauvdEDq54NiTphI7jx SECRET_KEY=sk_test_4eC39HqLyjWDarjtT1zdp7dc python3 flask-server.py

# stripe setting for payment
stripe_keys = {
  'secret_key': os.environ['SECRET_KEY'],
  'publishable_key': os.environ['PUBLISHABLE_KEY']
}

stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__, template_folder="public")

def authenticate_user(auth):
	credentials = "username:password"
	message_bytes = credentials.encode('ascii')
	base64_bytes = base64.b64encode(message_bytes)
	base64_credentials = base64_bytes.decode('ascii')

	if auth == "Basic " + base64_credentials:
		return True
	else:
		return False

@app.route('/', methods=['GET'])
def index():
	return render_template('tacoshop.html')

@app.route('/<filename>')
def open_file(filename, methods=['GET']):
		if request.method == 'GET':
			if filename.endswith('.json'):
				with open('public/' + filename) as jsonfile:
					jsondata = json.load(jsonfile)

				return jsonify(jsondata)
			# for payment
			if filename == 'mycart':
				return render_template('index.html', key=stripe_keys['publishable_key'])

			elif filename.endswith('.jpg'):
				return send_file('public/media/' + filename, mimetype='image/gif')

			elif filename == "favicon.ico":
				return send_file('public/media/' + filename, mimetype='image/gif')

			elif filename.endswith('.css'):
				return send_file('public/' + filename)

			else:
				return render_template(filename + '.html')

		elif request.method == 'POST':
			return "123"

@app.route('/upload', methods=['POST'])
def upload():
	auth = request.headers.get('Authorization')
	
	if not authenticate_user(auth):
		return "Access denied"

	dataJson = request.get_json()

	with open('./public' + dataJson["fileName"], 'w+') as fileToSave:
		json.dump(dataJson["menu"], fileToSave, ensure_ascii=True, indent=4)

	return "Data received: " + str(dataJson)

@app.route('/picture', methods=['POST'])
def picture():
	auth = request.headers.get('Authorization')
	
	if not authenticate_user(auth):
		return "Access denied"

	dataJson = request.get_json()

	image = base64.b64decode(dataJson["fileData"])
	img = Image.open(io.BytesIO(image))
	img.save("./public/media/" + dataJson["fileName"], 'jpeg')

	return "Data received: " + str(dataJson)


@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = 500

    customer = stripe.Customer.create(
        email='customer@example.com',
        source=request.form['stripeToken']
    )
    print('customer.id:', customer.id)
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )

    return render_template('charge.html', amount=amount)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
