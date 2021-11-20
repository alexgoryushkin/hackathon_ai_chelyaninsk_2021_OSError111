from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import Insert

db = SQLAlchemy()


def universal_sqla_stringify(self):
    pks = [f"{column.name}={getattr(self, column.name)}" for column in
           list(filter(lambda column: column.primary_key, inspect(self.__class__).columns))]
    return f"{self.__class__.__name__}({', '.join(pks)})"


def universal_sqla_repr(self):
    return self.__str__()


db.Model.__str__ = universal_sqla_stringify
db.Model.__repr__ = universal_sqla_repr


@compiles(Insert, "postgresql")
def postgresql_on_conflict_do_nothing(insert, compiler, **kw):
    """ Обработчик на все insert, отменяет ошибку duplicate key. """
    statement = compiler.visit_insert(insert, **kw)
    returning_position = statement.find("RETURNING")
    if returning_position >= 0:
        return statement[:returning_position] + "ON CONFLICT DO NOTHING " + statement[returning_position:]
    else:
        return statement + " ON CONFLICT DO NOTHING"


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
        sub_tasks = db.session.query(SubTask).filter(SubTask.task_id == self.id).all()
        is_valid_count = 0
        in_valid_count = 0
        not_detected = 0
        for st in sub_tasks:
            if st.is_valid is True:
                is_valid_count += 1
            elif st.is_valid is False:
                in_valid_count += 1
            else:
                not_detected += 1
        return {
            'id': self.id,
            'time': self.time.strftime('%d.%m.%Y %H:%M:%S'),
            'status': self.status,
            'isValidCount': is_valid_count,
            'inValidCount': in_valid_count,
            'notDetected': not_detected
        }


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
