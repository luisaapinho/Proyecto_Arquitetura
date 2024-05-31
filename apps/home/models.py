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
