from apps import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(255))
    price = db.Column(db.Float)
    image = db.Column(db.String(255))

    @staticmethod
    def get_all():
        return Product.query.all()