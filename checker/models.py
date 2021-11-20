from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Category(db.Model):
    code = db.Column(db.String(10), primary_key=True, unique=True)
    name = db.Column(db.String(4096))
    parent_code = db.Column(db.ForeignKey('category.code', ondelete='CASCADE', onupdate='CASCADE'))

    parent = db.relationship('Category', remote_side=[code])
    sub_tasks = db.relationship('SubTask', secondary='sub_task_has_category')
    products = db.relationship('Product', secondary='product_has_category')

    def to_json(self):
        return {'code': self.code, 'name': self.name}


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(8196))


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    time = db.Column(db.DateTime, server_default=db.text("CURRENT_TIMESTAMP"))
    status = db.Column(db.String(64))

    def to_json(self):
        return {'id': self.id, 'time': self.time, 'status': self.status}


class ProductHasCategory(db.Model):
    product_id = db.Column('product_id', db.ForeignKey('product.id'), primary_key=True, nullable=False)
    category_code = db.Column('category_code', db.ForeignKey('category.code'), primary_key=True, nullable=False)


class SubTask(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    task_id = db.Column(db.ForeignKey('task.id'))
    product_id = db.Column(db.ForeignKey('product.id'))
    is_valid = db.Column(db.Boolean)

    product = db.relationship('Product')
    task = db.relationship('Task')

    def to_json(self):
        self.product: Product
        our_cats = db.session.query(Category).outerjoin(ProductHasCategory).filter(
            ProductHasCategory.product_id == self.product_id).all()
        user_cats = db.session.query(Category).outerjoin(SubTaskHasCategory).filter(
            SubTaskHasCategory.sub_task_id == self.product_id).all()
        return {
            'id': self.id,
            'isValid': self.is_valid,
            'defaultCategories': [cat.to_json() for cat in our_cats],
            'userCategories': [cat.to_json() for cat in user_cats]
        }


class SubTaskHasCategory(db.Model):
    sub_task_id = db.Column('sub_task_id', db.ForeignKey('sub_task.id'), primary_key=True, nullable=False)
    category_code = db.Column('category_code', db.ForeignKey('category.code'), primary_key=True, nullable=False)
