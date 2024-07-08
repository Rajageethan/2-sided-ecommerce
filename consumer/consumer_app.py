from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from forms import consumer_signup as BuyerSignupForm, consumer_login as BuyerLoginForm
from flask_login import  LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from geopy.distance import geodesic
from flask_mail import Mail, Message
import secrets
import base64



app = Flask(__name__)
app.config['SECRET_KEY'] = ' ' #feel free to use a stronger key
app.config['MYSQL_HOST'] = '127.0.0.1' #use your host
app.config['MYSQL_USER'] = 'root' #use your user
app.config['MYSQL_PASSWORD'] = 'root' #use your password
app.config['MYSQL_DB'] = 'HGH' #use your DB


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '' #use your mail
app.config['MAIL_PASSWORD'] = '' #use your password

app.secret_key = '' #feel free to use a stronger key

mysql = MySQL(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email
        
        

    @staticmethod
    def get(user_id):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM consumer WHERE consumer_id = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        if not user_data:
            return None
        return User(user_data[0], user_data[1], user_data[2])
       



@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/buyer_signup', methods=['GET', 'POST'])
def buyer_signup():
    buyer_form = BuyerSignupForm()
    if request.method == 'POST':
        if buyer_form.is_submitted():
            username = buyer_form.username.data
            password = buyer_form.password.data
            confirm_password = buyer_form.confirm_password.data
            phone_number = buyer_form.phone_number.data
            email = buyer_form.email.data
            town = buyer_form.town.data
            state = buyer_form.state.data
            pincode = buyer_form.pincode.data
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO consumer (consumer_name, password, phone_number, email, town, state, pincode) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (username, hashed_password, phone_number, email, town, state, pincode))
        mysql.connection.commit()
        cursor.close()
        flash('Account created successfully!', 'success')
        return redirect(url_for('buyer_login'))
    return render_template('buyer_signup.html', form=buyer_form)


@app.route('/', methods=['GET', 'POST'])
def buyer_login():
    buyer_login_form = BuyerLoginForm()
    if request.method == 'POST':
        if buyer_login_form.is_submitted():
            username = buyer_login_form.username.data
            password = buyer_login_form.password.data

            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM consumer WHERE consumer_name = %s", (username,))
            user = cursor.fetchone()
            cursor.close()

            if user and bcrypt.check_password_hash(user[3], password):
                user_obj = User(user[0], user[1], user[2])
                login_user(user_obj)
                flash('Login successful!', 'success')

                latitude = request.form.get('latitude')
                longitude = request.form.get('longitude')

                if latitude is not None and longitude is not None:
                    session['latitude'] = float(latitude)
                    session['longitude'] = float(longitude)

                else:
                    flash('Latitude and longitude are required.', 'danger')

                global consumer_id
                consumer_id = user[0]
                return redirect(url_for('consumer_home'))
            
        else:
            flash('Login failed. Check your username and password.', 'danger')

    return render_template('buyer_login.html', form=buyer_login_form)



@app.route('/consumer_home')
@login_required
def consumer_home():
    consumer_latitude = session.get('latitude')
    consumer_longitude = session.get('longitude')

    if consumer_latitude is not None or consumer_longitude is not None:
         flash('Latitude and longitude are required.', 'danger')
         return redirect(url_for('buyer_login'))
    
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()

    return render_template('buyer_home.html', current_user=current_user, products=products)


@app.route('/place_order/<int:product_id>', methods=['POST'])
@login_required
def place_order(product_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.close()

    if product:
        quantity = int(request.form['quantity'])
        total_price = quantity * product[5]  
        consumer_name = current_user.username
        consumer_email = current_user.email
        product_name = product[2]  
        farmer_id = product[1]

        
        c = mysql.connection.cursor()
        c.execute("SELECT email FROM consumer WHERE consumer_name = %s", (current_user.username,))
        consumer_email_row = c.fetchone()
        c.close()

        if consumer_email_row:
            consumer_email = consumer_email_row[0]
        else:
           
            flash('Consumer email not found!', 'danger')
            return redirect(url_for('consumer_home'))

        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT email FROM farmers WHERE farmer_id = %s", (farmer_id,))
        farmer_email_row = cursor.fetchone()
        cursor.close()

        if farmer_email_row:
            farmer_email = farmer_email_row[0]
        else:
            
            flash('Farmer email not found!', 'danger')
            return redirect(url_for('consumer_home'))

       
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO orders (product_id, consumer_name, quantity, total_price, farmer_id, product_name) VALUES (%s, %s, %s, %s, %s, %s)",
                       (product_id, consumer_name, quantity, total_price, farmer_id, product_name))
        mysql.connection.commit()
        cursor.close()

        
        msg = Message('New Order', sender='homegrownheaven6@gmail.com', recipients=[farmer_email])
        msg.body = f'You have received a new order for {product_name} from {consumer_name}. Quantity: {quantity}. Total Price: {total_price}.'
        mail.send(msg)

        flash('Order placed successfully!', 'success')
    else:
        flash('Product not found!', 'danger')

    return redirect(url_for('consumer_home'))

    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('buyer_login'))



if __name__ == '__main__':
	app.run(debug=True, port=3000)