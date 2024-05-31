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
        product = Product.get_by_id(product_id)
        print(product)
        if product is None:
            return render_template('home/page-404.html'), 404
        return render_template('home/product_details.html', product=product)
    except TemplateNotFound:
        return render_template('home/page-404.html'), 404
    except Exception as e:
        print(e)
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
