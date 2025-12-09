from flask import Flask,request,jsonify,render_template,redirect,url_for,make_response
import os
from dotenv import load_dotenv
from flask_cors import CORS
from PIL import Image as PILImage
#import stripe
import mysql.connector

load_dotenv()

application = Flask(__name__)

# เรียก API ใน env
sk = os.getenv("key")

server = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'uebu'
}

CORS(application)

# check ว่า API มาไหม
if sk == None:
    print("❌Not Found SK")
else :
    print("✅Found SK")
    print(sk)

"""
@application.route('/')
def index():
    # แสดงหน้าฟอร์ม HTML
    return render_template('index.html')
"""
"""
@application.route('/signup', methods=['POST'])
def signup() :
    
    name = request.get_json('name')
    password = request.get_json('password')
    email = request.get_json('email')

    #new_user = User(name=name, email=email)
    #new_user.set_password(password)

    try :
        # --- ขั้นตอนใหม่: เชื่อมต่อและบันทึกข้อมูล ---
        conn = mysql.connector.connect(**server)
        cursor = conn.cursor()

        # คำสั่ง SQL สำหรับ INSERT (สมมติว่ามีตารางชื่อ 'products' และมีคอลัมน์ name, detail, price)
        sql = "INSERT INTO product (USERNAME, PASSWORD, EMAIL) VALUES (%s, %s, %s)"
        val = (name, password, email)
        
        cursor.execute(sql, val)

        # ยืนยันการบันทึกข้อมูล (Commit)
        conn.commit()
        
        # ปิดการเชื่อมต่อ
        cursor.close()
        conn.close()

        # *** ต้องมี return กลับไปให้ Frontend ***
        response_data = f"Data processed for: {name}, {email}, {password}"
        response = make_response(response_data, 200)

        # Anti-Cache Headers (เพื่อให้แน่ใจว่าไม่ติด 304)
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
        
    except mysql.connector.Error as err:
        return f"เกิดข้อผิดพลาด: {err}"
"""

"""
    if request.method == 'POST':
        # รับข้อมูลจากฟอร์ม
        first_name = request.form['fname']
        last_name = request.form['lname']

        # เชื่อมต่อฐานข้อมูล
        try:
            conn = mysql.connector.connect(**server)
            cursor = conn.cursor()

            # คำสั่ง SQL สำหรับ INSERT
            sql = "INSERT INTO users (first_name, last_name) VALUES (%s, %s)"
            val = (first_name, last_name)
            
            # รันคำสั่ง SQL (Python รองรับ Prepared Statements โดยอัตโนมัติเมื่อใช้ %s)
            cursor.execute(sql, val)
            
            # ยืนยันการบันทึกข้อมูล (Commit)
            conn.commit()
            
            cursor.close()
            conn.close()

            return "บันทึกข้อมูลสำเร็จด้วย Python Flask!"

        except mysql.connector.Error as err:
            return f"เกิดข้อผิดพลาด: {err}"

    return redirect(url_for('index'))
"""

@application.route('/product', methods=['POST'])
def product() :
    name = request.form.get('name')
    detail = request.form.get('detail')
    price = request.form.get('price')
    image = request.files.get('image') 

    try:
        # --- ขั้นตอนใหม่: เชื่อมต่อและบันทึกข้อมูล ---
        conn = mysql.connector.connect(**server)
        cursor = conn.cursor()

        # คำสั่ง SQL สำหรับ INSERT (สมมติว่ามีตารางชื่อ 'products' และมีคอลัมน์ name, detail, price)
        sql = "INSERT INTO product (NAME, DETAIL, EXPECTED_PRICE) VALUES (%s, %s, %s)"
        val = (name, detail, price)
        
        cursor.execute(sql, val)

        # ยืนยันการบันทึกข้อมูล (Commit)
        conn.commit()
        
        # ปิดการเชื่อมต่อ
        cursor.close()
        conn.close()

        # *** ต้องมี return กลับไปให้ Frontend ***
        response_data = f"Data processed for: {name}, {detail}, {price}"
        response = make_response(response_data, 200)

        # Anti-Cache Headers (เพื่อให้แน่ใจว่าไม่ติด 304)
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    
    except mysql.connector.Error as err:
        # หากเกิด Error จาก MySQL
        print(f"Error connecting to DB or executing query: {err}")
        return jsonify({'error': f'Database error: {err}'}), 500

    except Exception as e:
        # ใช้ Exception ที่เจาะจงเพื่อจับ error ได้ดีขึ้น
        print(f'Error processing request: {str(e)}')
        return make_response(f'Server Error: {str(e)}', 500)

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