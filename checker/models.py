# coding: utf-8
import os
import warnings
from contextlib import contextmanager

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, text, inspect
from sqlalchemy import create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import Insert

Base = declarative_base()
metadata = Base.metadata


def universal_sqla_stringify(self):
    pks = [f"{column.name}={getattr(self, column.name)}" for column in
           list(filter(lambda column: column.primary_key, inspect(self.__class__).columns))]
    return f"{self.__class__.__name__}({', '.join(pks)})"


def universal_sqla_repr(self):
    return self.__str__()


Base.__str__ = universal_sqla_stringify
Base.__repr__ = universal_sqla_repr


@compiles(Insert, "postgresql")
def postgresql_on_conflict_do_nothing(insert, compiler, **kw):
    """ Обработчик на все insert, отменяет ошибку duplicate key. """
    statement = compiler.visit_insert(insert, **kw)
    returning_position = statement.find("RETURNING")
    if returning_position >= 0:
        return statement[:returning_position] + "ON CONFLICT DO NOTHING " + statement[returning_position:]
    else:
        return statement + " ON CONFLICT DO NOTHING"


class Category(Base):
    __tablename__ = 'category'
    code = Column(String(10), primary_key=True, unique=True)
    name = Column(String(4096))
    parent_code = Column(ForeignKey('category.code', ondelete='CASCADE', onupdate='CASCADE'))

    parent = relationship('Category', remote_side=[code])
    sub_tasks = relationship('SubTask', secondary='sub_task_has_category')
    products = relationship('Product', secondary='product_has_category')

    def to_json(self):
        return {'code': self.code, 'name': self.name}


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(8196))


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, unique=True)
    time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    status = Column(String(64))

    def to_json(self, session):
        sub_tasks = session.query(SubTask).filter(SubTask.task_id == self.id).all()
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


class ProductHasCategory(Base):
    __tablename__ = 'product_has_category'
    product_id = Column('product_id', ForeignKey('product.id'), primary_key=True, nullable=False)
    category_code = Column('category_code', ForeignKey('category.code'), primary_key=True, nullable=False)


class SubTask(Base):
    __tablename__ = 'sub_task'
    id = Column(Integer, primary_key=True, unique=True)
    task_id = Column(ForeignKey('task.id'))
    product_id = Column(ForeignKey('product.id'))
    is_valid = Column(Boolean)

    product = relationship('Product')
    task = relationship('Task')

    def to_json(self, session):
        self.product: Product
        our_cats = session.query(Category).outerjoin(ProductHasCategory).filter(
            ProductHasCategory.product_id == self.product_id).all()
        user_cats = session.query(Category).outerjoin(SubTaskHasCategory).filter(
            SubTaskHasCategory.sub_task_id == self.product_id).all()
        return {
            'id': self.id,
            'isValid': self.is_valid,
            'productName': self.product.name,
            'defaultCategories': [cat.to_json() for cat in our_cats],
            'userCategories': [cat.to_json() for cat in user_cats]
        }


class SubTaskHasCategory(Base):
    __tablename__ = 'sub_task_has_category'
    sub_task_id = Column('sub_task_id', ForeignKey('sub_task.id'), primary_key=True, nullable=False)
    category_code = Column('category_code', ForeignKey('category.code'), primary_key=True, nullable=False)


engine = create_engine(
    f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@postgres.service:5432/"
    f"{os.environ['POSTGRES_DB']}", pool_pre_ping=True, pool_size=32, max_overflow=64
)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def SessionManager():
    db = SessionLocal()
    try:
        yield db
    except:
        warnings.warn("auto-rollbacking")
        db.rollback()
        raise
    finally:
        db.close()
