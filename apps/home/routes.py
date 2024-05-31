# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.home.models import Product
from apps.home.models import Category
from apps.home.models import ProductBySize
from apps.home.models import Size
from apps import db

@blueprint.route('/index')
@login_required
def index():
    print("teste1")
    return render_template('home/index.html', segment='index')

@blueprint.route('/shop')
@login_required
def shop():
        print("teste2")
        products = Product.get_all()
        categories = Category.get_all()
        print(products[0].Image)
        print(products)  # Check the products being retrieved
        return render_template('home/shop.html', segment='shop', products=products, categories=categories)

@blueprint.route('/shop/product/<int:product_id>')
@login_required
def product_details(product_id):
    try:
        print(f"Fetching details for product_id: {product_id}")
        product = Product.get_by_id(product_id)
        if product is None:
            print("Product not found")
            return render_template('home/page-404.html'), 404

        # Fetch available sizes for the product
        available_sizes = db.session.query(Size).join(ProductBySize, Size.id_Size == ProductBySize.id_Size).filter(ProductBySize.id_Product == product_id).all()
        print(f"Available sizes: {available_sizes}")

        return render_template('home/product_details.html', product=product, available_sizes=available_sizes)
    except TemplateNotFound:
        print("Template not found")
        return render_template('home/page-404.html'), 404
    except Exception as e:
        print(f"Exception: {e}")
        return render_template('home/page-500.html'), 500

    
@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
