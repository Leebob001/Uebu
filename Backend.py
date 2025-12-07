from flask import Flask,request,jsonify
import os
from dotenv import load_dotenv
from flask_cors import CORS
#import stripe
import mysql.connector

load_dotenv()

application = Flask(__name__)

# เรียก API ใน env
sk = os.getenv("key")

CORS(application, resources={r"/pay": {"origins": "*"}})

# check ว่า API มาไหม
if sk == None:
    print("❌Not Found SK")
else :
    print("✅Found SK")
    print(sk)

@application.route('/signup', methods=['POST'])
def signup() :
    
    name = request.get_json('name')
    password = request.get_json('password')
    email = request.get_json('email')

    #new_user = User(name=name, email=email)
    #new_user.set_password(password)

@application.route('/pay', methods=['POST'])
def pay() :

    price = request.get_json('amount')
    pk = request.get_json('omiseToken')

    try:
        response = request.post(
            'api.omise.co',
            auth=(sk, ''), # Secret Key เป็น Username, Password ว่างเปล่า
            headers={
                'Content-Type': 'application/json'
            },
            data=jsonify.dumps({
                'amount': price,
                'currency': 'THB',
                'card': pk, # ใช้ Token ที่ได้รับมา
                'description': ''
            })
        )

        """
        charge_result = response.json()

        if charge_result.get('status') == 'successful':
            return jsonify({
                'status': 'successful',
                'message': 'Payment was successful',
                'transaction_id': charge_result.get('id')
            })
        else:
            error_message = charge_result.get('failure_message', 'Unknown error')
            return jsonify({
                'status': 'failed',
                'message': error_message
            }), 400
        """

    except request.exceptions.RequestException as e:
        print("status: error")
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    application.run(debug=True, port=5001)