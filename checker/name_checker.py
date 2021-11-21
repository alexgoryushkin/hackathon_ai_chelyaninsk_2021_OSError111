from typing import Tuple, List, Optional

import classifier
from models import Category
from sqlalchemy.sql import or_, and_


def neuron_oracle(session, name, user_codes) -> Tuple[List[Category], Optional[bool]]:
    our_cat = classifier.predict(name, threshold=0.4)
    categories: List[Category] = session.query(Category).filter(
        or_(and_(Category.name == our_cat, Category.parent_code != None),
            Category.name == our_cat)
    ).all()
    our_cats = [cat.code for cat in categories]

    if not user_codes:
        return categories, None

    if len(our_cats) != len(user_codes):
        return categories, False

    is_valid = False
    for cat in user_codes:
        if cat in our_cats:
            is_valid = True
            break

    return categories, is_valid
