from apps import db

class Product(db.Model):


    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    id_Category = db.Column(db.Integer)
    id_Gender = db.Column(db.Integer)
    Name = db.Column(db.String(255))
    Description = db.Column(db.String(255))
    Price = db.Column(db.Float)
    Image = db.Column(db.String(255))

    @staticmethod
    def get_all():
        return Product.query.all()