from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users
from apps.authentication.util import verify_pass

class Product(db.Model):


    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    id_Category = db.Column(db.Integer)
    Name = db.Column(db.String(255))
    Description = db.Column(db.String(255))
    Price = db.Column(db.Float)
    Image = db.Column(db.String(255))

    @staticmethod
    def get_all():
        return Product.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Product.query.get(id)
    
class Category(db.Model):

    __tablename__ = 'category'

    id_Category = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255))

    @staticmethod
    def get_all():
        return Category.query.all()
    


class ProductBySize(db.Model):


    __tablename__ = 'productpersize'

    id_ProductSize = db.Column(db.Integer, primary_key=True)
    id_Product = db.Column(db.Integer)
    id_Size = db.Column(db.Integer)
    Stock = db.Column(db.Integer)

    @staticmethod
    def get_all():
        return ProductBySize.query.all()
    
    @staticmethod
    def get_by_id(id):
        return Product.query.get(id)
    

class Size(db.Model):
     
    __tablename__ = 'sizes'

    id_Size = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255))

    @staticmethod
    def get_all():
        return Size.query.all()
    
class Cart(db.Model):
    __tablename__ = 'cart'

    id_Cart = db.Column(db.Integer, primary_key=True)  # Added a primary key
    id_User = db.Column(db.Integer, db.ForeignKey('users.id'))  # Assuming there is a user model
    id_ProductSize = db.Column(db.Integer, db.ForeignKey('productpersize.id_ProductSize'))
    Quantity = db.Column(db.Integer, default=1)

    product_size = db.relationship('ProductBySize', backref='cart', lazy=True)

    @staticmethod
    def get_by_user(user_id):
        return Cart.query.filter_by(id_User=user_id).all()
    
    @staticmethod
    def add_item(user_id, product_id, size_id):
        product_size = ProductBySize.query.filter_by(id_Product=product_id, id_Size=size_id).first()
        if not product_size:
            raise ValueError("Invalid product or size")

        cart_item = Cart.query.filter_by(id_User=user_id, id_ProductSize=product_size.id_ProductSize).first()
        if cart_item:
            cart_item.Quantity += 1
        else:
            cart_item = Cart(id_User=user_id, id_ProductSize=product_size.id_ProductSize, Quantity=1)
            db.session.add(cart_item)
        
        db.session.commit()
        return cart_item
    
    @staticmethod
    def delete(id):
        cart_item = Cart.query.get(id)
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            return True
        else:
            return False
