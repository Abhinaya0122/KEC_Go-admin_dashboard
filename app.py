from flask import Flask, render_template, request, redirect, url_for
from firebase_config import initialize_firebase
from datetime import datetime
import firestore

app = Flask(__name__)

# Initialize Firestore
db = initialize_firebase()

# Home route
@app.route('/')
def index():
    # Similar to your current implementation
    total_orders = 0
    total_users = 0
    total_revenue = 0.0
    recent_orders = []

    users_ref = db.collection('users')
    users = users_ref.stream()
    
    for user in users:
        user_data = user.to_dict()
        orders_ref = user.reference.collection('orders')
        orders = orders_ref.stream()
        
        for order in orders:
            order_data = order.to_dict()
            total_orders += 1
            total_revenue += order_data.get('totalAmount', 0)

            recent_orders.append({
                'order_id': order.id,
                'createdAt': order_data.get('createdAt', ''),
                'totalAmount': order_data.get('totalAmount', 0)
            })

    total_users = len(list(users))

    return render_template('index.html', 
                           total_orders=total_orders, 
                           total_users=total_users, 
                           total_revenue=total_revenue, 
                           recent_orders=recent_orders,
                           year=datetime.now().year)

# Route to view and manage products
@app.route('/products')
def products():
    products_ref = db.collection('products')  # Reference to the 'products' collection in Firestore
    products = products_ref.stream()  # Retrieve all documents in the 'products' collection

    products_list = []  # Initialize an empty list to store product data
    for product in products:
        product_data = product.to_dict()  # Convert each Firestore document to a dictionary
        product_data['product_id'] = product.id  # Add product ID for reference
        products_list.append(product_data)  # Append the product data to the list

    return render_template('products.html', products=products_list)  # Render the products.html template with the product list


# Existing route to view all orders
@app.route('/dashboard/all')
def dashboard_all():
    users_ref = db.collection('users')
    users = users_ref.stream()

    all_orders = []

    for user in users:
        user_id = user.id
        orders_ref = db.collection('users').document(user_id).collection('orders')
        orders = orders_ref.stream()
        
        for order in orders:
            order_data = order.to_dict()
            order_data['order_id'] = order.id
            if 'createdAt' in order_data:
                created_at = order_data['createdAt']
                if isinstance(created_at, firestore.Timestamp):
                    created_at = created_at.to_datetime()
                order_data['createdAt'] = created_at.strftime("%B %d, %Y at %I:%M:%S %p")
            
            items = order_data.get('items', [])
            order_data['products'] = [
                {
                    'name': item.get('name'),
                    'quantity': item.get('quantity'),
                    'price': item.get('price'),
                    'total': item.get('quantity') * item.get('price')
                } for item in items
            ]
            order_data['user_id'] = user_id
            all_orders.append(order_data)

    return render_template('dashboard.html', orders=all_orders)

@app.route('/add_product', methods=['POST'])
def add_product():
    # Get form data
    name = request.form.get('name')
    price = float(request.form.get('price'))
    quantity = int(request.form.get('quantity'))
    description = request.form.get('description')
    imageUrl = request.form.get('imageurl')

    # Add product to Firestore
    products_ref = db.collection('products')
    products_ref.add({
        'name': name,
        'price': price,
        'quantity': quantity,
        'description':description,
        'imageUrl':imageUrl
    })

    return redirect('/')

@app.route('/delete_product', methods=['POST'])
def delete_product():
    # Get product ID
    product_id = request.form.get('product_id')

    # Delete product from Firestore
    db.collection('products').document(product_id).delete()

    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
