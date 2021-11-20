from typing import Tuple, List

from models import Category, db


def neuron_oracle(name, user_codes) -> Tuple[List[Category], bool]:
    is_valid = False
    categories: List[Category] = db.session.query(Category).filter(Category.code.in_(user_codes)).all()
    for cat in categories:
        if cat.name == name:
            is_valid = True

    if not user_codes:
        is_valid = None
    return categories, is_valid
