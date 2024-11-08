from flask import Flask, render_template, redirect, url_for, session, request, flash
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  # Replace with a real secret key

# Configure Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))  # Default to 587 if MAIL_PORT is not set
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

# Dummy data for shoes
shoes = [
    {'id': 1, 'name': 'Running Shoes', 'price': 80, 'description': 'Perfect for running', 'image': 'images/running_shoes.jpg'},
    {'id': 2, 'name': 'Basketball Shoes', 'price': 120, 'description': 'Ideal for the court', 'image': 'images/basketball_shoes.jpg'},
    {'id': 3, 'name': 'Casual Sneakers', 'price': 60, 'description': 'Great for everyday wear', 'image': 'images/casual_sneakers.jpg'},
    {'id': 4, 'name': 'Formal Shoes', 'price': 100, 'description': 'Elegant and professional', 'image': 'images/formal_shoes.jpg'},
    {'id': 5, 'name': 'Sandals', 'price': 40, 'description': 'Comfortable for summer', 'image': 'images/sandals.jpg'}
]

# Home route displaying all shoes
@app.route('/')
def index():
    return render_template('index.html', shoes=shoes)

# Route for shoe details
@app.route('/shoe/<int:shoe_id>')
def shoe_detail(shoe_id):
    shoe = next((s for s in shoes if s['id'] == shoe_id), None)
    if shoe:
        return render_template('shoe_detail.html', shoe=shoe)
    else:
        return "Shoe not found", 404

# Route to add a shoe to the cart
@app.route('/add_to_cart/<int:shoe_id>')
def add_to_cart(shoe_id):
    shoe = next((s for s in shoes if s['id'] == shoe_id), None)
    if shoe:
        cart = session.get('cart', [])
        cart.append(shoe)
        session['cart'] = cart
        flash(f"{shoe['name']} has been added to your cart!")
    else:
        flash("Shoe not found.")
    return redirect(url_for('index'))

# Route for buying a shoe
@app.route('/buy/<int:shoe_id>')
def buy_shoe(shoe_id):
    shoe = next((s for s in shoes if s['id'] == shoe_id), None)
    if shoe:
        # Send notification email to the owner
        try:
            msg = Message(f"New Purchase: {shoe['name']}",
                          recipients=['ndiritus532@gmail.com'])  # Replace with owner's email
            msg.body = f"A customer has purchased {shoe['name']} for ${shoe['price']}."
            mail.send(msg)
            flash("Purchase successful! Notification sent to the owner.")
        except Exception as e:
            flash("Purchase successful! However, notification could not be sent.")
            print(f"Error sending email: {e}")
        return redirect(url_for('index'))
    else:
        return "Shoe not found", 404

# Cart page
@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    total_price = sum(item['price'] for item in cart)
    return render_template('cart.html', cart=cart, total_price=total_price)

# Route to clear cart
@app.route('/clear_cart')
def clear_cart():
    session['cart'] = []
    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug=True)
