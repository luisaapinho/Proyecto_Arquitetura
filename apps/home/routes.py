# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, redirect, url_for, flash, current_app
from apps.authentication.models import Users
from flask_login import login_required,current_user
from jinja2 import TemplateNotFound
from apps.home.models import Product
from apps.home.models import Category
from apps.home.models import ProductBySize
from apps.home.models import Size
from apps.home.models import Cart
from apps import db

@blueprint.route('/index')
def index():
    return render_template('home/index.html', segment='index')

@blueprint.route('/profile')
@login_required
def profile():
    return render_template('home/profile.html', user=current_user)

@blueprint.route('/update_username', methods=['POST'])
@login_required
def update_username():
    new_username = request.form['username']
    if new_username:
        user_id = current_user.id
        if Users.updateName(user_id, username=new_username):
            flash('Username updated successfully!', 'success')
        else:
            flash('Failed to update username.', 'danger')
    return redirect(url_for('home_blueprint.profile'))

@blueprint.route('/update_email', methods=['POST'])
@login_required
def update_email():
    new_email = request.form['email']
    if new_email:
        user_id = current_user.id
        if Users.updateEmail(user_id, email=new_email):
            flash('Email updated successfully!', 'success')
        else:
            flash('Failed to update email.', 'danger')
    return redirect(url_for('home_blueprint.profile'))

@blueprint.route('/update_password', methods=['POST'])
@login_required
def update_password():
    old_password = request.form['old_password']
    new_password = request.form['new_password']
    
    if old_password and new_password:
        user = current_user
        if Users.update_password(user, old_password, new_password):
            flash('Password updated successfully!', 'success')
        else:
            flash('Old password is incorrect.', 'danger')
    
    return redirect(url_for('home_blueprint.profile'))
    print("teste1")
    return render_template('home/index.html', segment='index')

@blueprint.route('/shop')
def shop():
        print("teste2")
        products = Product.get_all()
        categories = Category.get_all()
        print(products[0].Image)
        print(products)  # Check the products being retrieved
        return render_template('home/shop.html', segment='shop', products=products, categories=categories)

@blueprint.route('/shop/product/<int:product_id>')
def product_details(product_id):
    try:
        print(f"Fetching details for product_id: {product_id}")
        product = Product.get_by_id(product_id)
        if product is None:
            print("Product not found")
            return render_template('home/page-404.html'), 404

        # Fetch available sizes for the product
        available_sizes = db.session.query(Size).join(
            ProductBySize, Size.id_Size == ProductBySize.id_Size).filter(ProductBySize.id_Product == product_id).all()
        print(f"Available sizes: {available_sizes}")

        return render_template('home/product_details.html', product=product, available_sizes=available_sizes)
    except TemplateNotFound:
        print("Template not found")
        return render_template('home/page-404.html'), 404
    except Exception as e:
        print(f"Exception: {e}")
        return render_template('home/page-500.html'), 500
    

@blueprint.route('/add-to-cart', methods=['POST'])
@login_required
def add_to_cart():
    try:
        product_id = request.form.get('product_id')
        size_id = request.form.get('size_id')

        print(f"Product ID: {product_id}, Size ID: {size_id}")

        Cart.add_item(current_user.id, product_id, size_id)

        return redirect(url_for('home_blueprint.product_details', product_id=product_id))
        


    except Exception as e:
        print(f"Exception: {e}")
        return render_template('home/page-500.html'), 500
        

@blueprint.route('/cart')
@login_required
def cart():
    try:
        # Fetch cart items for the current user
        user_id = current_user.id  # Assuming `current_user` has an `id` attribute
        cart_items = Cart.get_by_user(user_id)
        
        # Collect product details and calculate total price
        cart_details = []
        total_price = 0
        for item in cart_items:
            product_size = ProductBySize.query.get(item.id_ProductSize)
            product = Product.query.get(product_size.id_Product)
            size = Size.query.get(product_size.id_Size)
            
            item_total = product.Price * item.Quantity
            total_price += item_total
            
            cart_details.append({
                'id_Cart': item.id_Cart,
                'product_name': product.Name,
                'product_description': product.Description,
                'product_image': product.Image,
                'product_price': product.Price,
                'size': size.Name,
                'quantity': item.Quantity,
                'item_total': item_total
            })
        
        print(cart_details)
        return render_template('home/cart.html', cart_details=cart_details, total_price=total_price)
    except TemplateNotFound:
        return render_template('home/page-404.html'), 404
    except Exception as e:
        print(f"Exception: {e}")
        return render_template('home/page-500.html'), 500
    

    
    

@blueprint.route('/delete_item_cart/<int:id>', methods=['POST'])
@login_required
def delete_item_cart(id):
    print(id)
    Cart.delete(id)
    return redirect(url_for('home_blueprint.cart'))



    
# views.py

@blueprint.route('/checkout', methods=['POST'])
@login_required
def checkout():
    try:
        user_id = current_user.id
        cart_items = Cart.get_by_user(user_id)

        # Loop through cart items and update the stock
        for item in cart_items:
            product_size = ProductBySize.query.get(item.id_ProductSize)
            
            if product_size.Stock < item.Quantity:
                flash(f'Not enough stock for product ID {product_size.id_Product}. Only {product_size.Stock} left.', 'danger')
                return redirect(url_for('home_blueprint.cart'))
            
            product_size.Stock -= item.Quantity
            db.session.add(product_size)
        
        db.session.commit()

        # Clear the user's cart after successful purchase
        for item in cart_items:
            db.session.delete(item)
        
        db.session.commit()

        flash('Purchase successful!', 'success')
        return redirect(url_for('home_blueprint.shop'))
    except Exception as e:
        db.session.rollback()
        print(f"Exception: {e}")
        flash('An error occurred during the purchase process. Please try again.', 'danger')
        return redirect(url_for('home_blueprint.cart'))





    

    
@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:
        if not template.endswith('.html'):
            template += '.html'
        segment = get_segment(request)
        return render_template("home/" + template, segment=segment)
    except TemplateNotFound:
        return render_template('home/page-404.html'), 404
    except:
        return render_template('home/page-500.html'), 500

def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None
