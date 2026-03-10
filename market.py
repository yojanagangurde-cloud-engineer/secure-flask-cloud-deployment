import os

from flask import Flask, render_template, redirect, render_template_string, url_for, request, session
from models import db, User, Product, Order

app = Flask(__name__)
app.secret_key = "supersecretkey123"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@db:5432/market_db"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

items = [
    {'id': 1, 'name': 'Shirt', 'price': '$30', 'image': 'shirt.jpg'},
    {'id': 2, 'name': 'Shoes', 'price': '$150', 'image': 'shoes.jpg'},
    {'id': 3, 'name': 'Dress', 'price': '$45', 'image': 'dress.jpg'},
    {'id': 4, 'name': 'Jacket', 'price': '$75', 'image': 'jacket.jpg'},
    {'id': 5, 'name': 'Hat', 'price': '$25', 'image': 'hat.jpg'},
    {'id': 6, 'name': 'Jeans', 'price': '$70', 'image': 'jeans.jpg'},
    {'id': 7, 'name': 'Bag', 'price': '$120', 'image': 'bag.jpg'},
    {'id': 8, 'name': 'Cap', 'price': '$20', 'image': 'cap.jpg'},
    {'id': 9, 'name': 'Sunglasses', 'price': '$60', 'image': 'sunglasses.jpg'},
    {'id': 10, 'name': 'Watch', 'price': '$85', 'image': 'watch.jpg'},
    {'id': 11, 'name': 'Suit Coat', 'price': '$350', 'image': 'suit_coat.jpg'},
    {'id': 12, 'name': 'Long Coat', 'price': '$75', 'image': 'long_coat.jpg'},

]

cart = [] #shopping cart to hold added items

# Home page
@app.route("/")
@app.route("/home")
def home_page():
    featured_items = [items[1], items[2], items[4]]
    return render_template('home.html', items=featured_items, cart_count=len(cart))

# Shop page
@app.route("/shop")
def shop_page():
    return render_template('shop.html', items=items, cart_count=len(cart))

# Add to cart / Buy Now
@app.route("/buy_now/<int:item_id>", methods=["POST"])
def buy_now(item_id):
    product = next((item for item in items if item['id'] == item_id), None)
    if product:
        cart.append(product)
    return redirect(url_for('cart_page'))

#cart page
@app.route("/cart")
def cart_page():
    total = sum(int(item['price'].strip('$')) for item in cart)
    return render_template("cart.html", cart=cart, cart_count=len(cart), total=total)

#checkout page
@app.route("/checkout", methods=["GET", "POST"])
def checkout_page():
    if not cart:
        return redirect(url_for('shop_page'))

    total = sum(int(item['price'].strip('$')) for item in cart)

    if request.method == "POST":

        name = request.form.get("name")
        address = request.form.get("address")
        payment = request.form.get("payment")

        new_order = Order(user_name=name, address=address, total=total)
        db.session.add(new_order)
        db.session.commit()

        cart.clear()

        return render_template_string("""
            <div style="text-align:center; margin-top:300px; font-family:sans-serif;">
                <h2>Thank You, {{ name }}!</h2>
                <p>Your order has been placed successfully.</p>
                <p>Shipping to: {{ address }}</p>
                <a href="{{ url_for('home_page') }}">Go to Home</a>
            </div>
        """, name=name, address=address)

    return render_template("checkout.html", cart=cart, total=total, cart_count=len(cart))

# Login page
@app.route("/login", methods=["GET", "POST"])
def login_page():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")
        name = email.split("@")[0]

        user = User.query.filter_by(email=email,password=password).first()

        if user:
            session['user_name'] = user.name

            return render_template_string("""
            <div style="text-align:center; margin-top:300px; font-family:sans-serif;">
                <h2>Welcome Back, {{ name }}!</h2>
                <p>You have successfully logged in.</p>
                <p>Keep shopping!</p>
                <a href="{{ url_for('home_page') }}">Go to Home</a>
            </div>
        """ , name=name, email=email)

        else:
            return render_template_string("""
            <div style="text-align:center; margin-top:300px; font-family:sans-serif;">
                <h2>Invalid Login!</h2>
                <p>No account exists with email:{{ email }}</p>
                <p>Please <a href="{{ url_for('register_page') }}">register</a> first.</p>
                <a href="{{ url_for('login_page') }}">Try Different Credentials</a>
            </div>
        """ , name=name, email=email)

    return render_template("login.html")

# Register page
@app.route("/register", methods=["GET", "POST"])
def register_page():

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template_string("""
                <div style="text-align:center; margin-top:300px; font-family:sans-serif;">
                    <h2>User Already Exists</h2>
                    <p>{{email}} is already registered.</p>
                    <a href="{{ url_for('login_page') }}">Please log in instead</a>
                    <a href="{{ url_for('register_page') }}">or Try a Different Email</a>

                </div>
            """)

        new_user = User(name=name, email=email, password=password)


        db.session.add(new_user)
        db.session.commit()

        session['user_name'] = name

        return render_template_string("""
            <div style="text-align:center; margin-top:300px; font-family:sans-serif;">
                <h2>Welcome, {{ name }}!</h2>
                <p>You have successfully registered.</p>
                <p>Keep shopping!</p>
                <a href="{{ url_for('home_page') }}">Go to Home</a>
            </div>
        """, name=name)

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop('user_name', None)
    return redirect(url_for('home_page'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5001)