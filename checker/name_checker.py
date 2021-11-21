from typing import Tuple, List, Optional

import classifier
from models import Category, db
from sqlalchemy.sql import or_, and_

def neuron_oracle(name, user_codes) -> Tuple[List[Category], Optional[bool]]:
    our_cats = classifier.predict(name, threshold=0.4)
    categories: List[Category] = db.session.query(Category).filter(
        or_(and_(Category.name.in_(our_cats), Category.parent_code != None),
            Category.name.in_(our_cats))
    ).all()
    our_cats = [cat.code for cat in categories]
    # print(name, 'our_cats', our_cats, 'user_codes', user_codes)

    if not user_codes:
        return categories, None

    if len(our_cats) != len(user_codes):
        return categories, False

    is_valid = False
    for cat in user_codes:
        if not cat in our_cats:
            break
    else:
        is_valid = True

    return categories, is_valid
