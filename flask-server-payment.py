from flask import Flask, render_template, request, jsonify, send_file
import json
import base64
from PIL import Image
import io
import os
import stripe
from config import stripe_keys, user_info
from helpers import success_response, error_response, check_json
# refer from: https://stripe.com/docs/legacy-checkout/flask
# bank account: https://stripe.com/docs/testing
# sudo PUBLISHABLE_KEY=pk_test_TYooMQauvdEDq54NiTphI7jx SECRET_KEY=sk_test_4eC39HqLyjWDarjtT1zdp7dc python3 flask-server.py

# stripe setting for payment
# stripe_keys = {
#   'secret_key': os.environ['SECRET_KEY'],
#   'publishable_key': os.environ['PUBLISHABLE_KEY']
# }

# stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__, template_folder="public")

def authenticate_user(auth):
	credentials = user_info["username"] + ":" + user_info["password"]
	message_bytes = credentials.encode('ascii')
	base64_bytes = base64.b64encode(message_bytes)
	base64_credentials = base64_bytes.decode('ascii')

	if auth == "Basic " + base64_credentials:
		return True
	else:
		return False

@app.route('/', methods=['GET'])
def index():
	return render_template('default.html')

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
				return render_template('template.html')


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


# @app.route('/charge', methods=['POST'])
# def charge():
#     # Amount in cents
#     amount = 500

#     customer = stripe.Customer.create(
#         email='customer@example.com',
#         source=request.form['stripeToken']
#     )
#     print('customer.id:', customer.id)
#     charge = stripe.Charge.create(
#         customer=customer.id,
#         amount=amount,
#         currency='usd',
#         description='Flask Charge'
#     )

#     return render_template('charge.html', amount=amount)

@app.route('/confirmation')
def confirmation_page():
    id = request.args.get('id', default="", type=str)
    amount = request.args.get('amount', default="", type=str)
    email = request.args.get('email', default="", type=str)
    product = request.args.get('product', default="", type=str)

    return render_template('confirmation.html', id=id, email=email, product=product, amount=amount)


@app.route('/public/charge', methods=['POST'])
def charge_api():
    if request.method == 'POST':
        # grab json from request body
        json = request.json
        # check if all keys present, return error if any missing
        result = check_json(
            json, ['email', 'stripe_token', 'description', 'amount'])
        if result:
            return error_response("missing {}".format(result))
        # add stripe api key
        stripe.api_key = stripe_keys['secret_key']
        try:
            # create customer ID
            customer = stripe.Customer.create(
                email=json['email'],
                source=json['stripe_token']
            )
            # create charge
            charge = stripe.Charge.create(
                customer=customer.id,
                amount=json['amount'],
                currency='usd',
                description=json['description']
            )
            # jsonify'd 200 success
            return success_response(charge)

        except stripe.error.StripeError as e:
            # jsonify'd 500 error
            return error_response(e)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=user_info["port_config"])
