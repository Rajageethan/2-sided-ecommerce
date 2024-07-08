from flask import Flask, jsonify, render_template, request, flash, redirect, url_for, session, Request
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from forms import farmer_signup as FarmerSignupForm
from flask_login import  LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import secrets, requests
from datetime import date


app = Flask(__name__)
app.config['SECRET_KEY'] = '' #feel free to use a stronger key
app.config['MYSQL_HOST'] = '127.0.0.1' #use your host
app.config['MYSQL_USER'] = 'root' #use your user
app.config['MYSQL_PASSWORD'] = 'root' #use your password
app.config['MYSQL_DB'] = 'HGH' #use your DB

app.secret_key = ''#feel free to use a stronger key

mysql = MySQL(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.email = email
        self.username = username
        

    @staticmethod
    def get(user_id):

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM farmers WHERE farmer_id = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()

        if not user_data:
            return None
        return User(user_data[0], user_data[1], user_data[2])

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/farmer_signup', methods=['GET', 'POST'])
def farmer_signup():
    farmer_form = FarmerSignupForm()
    if request.method == 'POST':
        if farmer_form.is_submitted():
                username = request.form['username']
                password = request.form['password']
                confirm_password = request.form['confirm_password']
                phone_number = request.form['phone_number']
                email = request.form['email']
                flat = request.form['flat_no']
                street = request.form['street']
                town = request.form['town']
                state = request.form['state']
                country = request.form['country']
                pincode = request.form['pincode']

                address = f"{flat} {street}, {town}, {state}, {pincode}, {country}"

                geo_api_key = "" #your key

                url = f"https://us1.locationiq.com/v1/search?key={geo_api_key}&q={address}&format=json"
                response = requests.get(url)


                if response.status_code == 200:
                    data = response.json()
                    if data and data[0]:
                        latitude = data[0]["lat"]
                        longitude = data[0]["lon"]

                    else:
                        latitude = None
                        longitude = None

                else:
                    latitude = None
                    longitude = None

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO farmers (name, password, phone_number, email, town, state, pincode, address, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (username, hashed_password, phone_number, email, town, state, pincode, address, latitude, longitude))
        mysql.connection.commit()
        cursor.close()
        flash('Account created successfully!', 'success')
        return redirect(url_for('farmer_login'))
    return render_template('farmer_signup.html', form=farmer_form)

@app.route('/', methods=['GET', 'POST'])
def farmer_login():
    if request.method == 'POST':
        print(request.form)
        email = request.form.get('email')
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM farmers WHERE email = %s", (email,)) 
        user = cursor.fetchone()
        cursor.close()

        if user and bcrypt.check_password_hash(user[3], password):
            user_obj = User(user[0], user[1], user[2])
            login_user(user_obj)
            flash('Login successful!', 'success')
            global farmer_id
            farmer_id = user[0]
            return redirect(url_for('farmer_home'))
            
        else:
            flash('Login failed. Check your username and password.', 'danger')

    return render_template('farmer_login.html')

@app.route('/farmer_home')
@login_required
def farmer_home():
    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM orders WHERE farmer_id = %s", (current_user.id,))
    orders = cursor.fetchall()
    
    cursor.execute("SELECT * FROM products WHERE farmer_id = %s", (current_user.id,))
    listings  = cursor.fetchall()

    cursor.close()

    return render_template('farmer_home.html', current_user=current_user, listings = listings, orders=orders)

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('farmer_home'))

@app.route('/add_product', methods=['POST'])
@login_required
def add_product():
    if request.method == 'POST':
        product_name = request.form['product-name']
        product_category = request.form['product-category']
        product_description = request.form['product-description']
        product_price = request.form['product-price']
        product_image = request.form['product-image']
        date_today = date.today()
        
        farmer_id = current_user.id

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO products (farmer_id, product_name, description, category, price, image_url, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (farmer_id, product_name, product_description, product_category, product_price, product_image, date_today))
        mysql.connection.commit()
        cursor.close()

        flash("Product added successfully!", 'success')

    return redirect(url_for('farmer_home'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('farmer_login'))


if __name__ == '__main__':
    app.run(debug=True, port=6969)

