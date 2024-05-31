from apps import db

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
    

