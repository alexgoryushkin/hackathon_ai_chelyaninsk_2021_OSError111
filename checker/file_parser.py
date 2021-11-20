import string

from openpyxl import load_workbook

from name_checker import neuron_oracle
from models import Task, SubTask, Product, SubTaskHasCategory, Category, ProductHasCategory

product_name_column_name = 'Общее наименование продукции'
product_code_column_name = 'Раздел ЕП РФ (Код из ФГИС ФСА для подкатегории продукции)'


def file_to_farsh(db, filename, file_ext, task):
    if file_ext == 'xlsx':
        xlsx = load_workbook(filename)
        tab = xlsx.worksheets[0]
        product_name_column = None
        product_code_column = None


        for sym in string.ascii_uppercase:
            cell = tab[f'{sym}1'].value
            print(cell)
            if cell and product_name_column_name in cell:
                print('product_name_column', cell)
                product_name_column = sym
            if cell and product_code_column_name in cell:
                print('product_code_column', cell)
                product_code_column = sym
            if product_name_column  and product_code_column:
                break

        if not product_name_column or not product_code_column:
            raise RuntimeError(f'product_name_column={product_name_column} product_code_column={product_code_column}')

        db.session.add(task)
        db.session.commit()

        i = 2
        while True:
            name = tab[f'{product_name_column}{i}'].value.strip()
            cat_codes = tab[f'{product_code_column}{i}'].value.strip()
            if name:
                product = Product(name=name)
                db.session.add(product)
                db.session.commit()
                sub_task = SubTask(task_id=task.id, product_id=product.id, is_valid=False)
                db.session.add(sub_task)
                db.session.commit()
                user_codes = []
                user_categories = []
                for cat_code in cat_codes.split(';'):
                    user_codes.append(cat_code.strip())
                    category = db.session.query(Category).filter(Category.code == cat_code).first()
                    if category:
                        user_categories.append(category)
                        stc = SubTaskHasCategory(sub_task_id=sub_task.id, category_code=category.code)
                        db.session.add(stc)
                        db.session.commit()

                our_categories, is_valid = neuron_oracle(name, user_codes)
                for category in our_categories:
                    phc = ProductHasCategory(product_id=product.id, category_code=category.code)
                    db.session.add(phc)
                sub_task.is_valid = is_valid
                db.session.commit()
                db.session.flush()

                i += 1
            else:
                print('doc end')
                break

        task.status = 'done'
        db.session.commit()
        db.session.flush()
    else:
        raise NotImplementedError('xlsx only plz')


# def extract_categories_from_file(db, filename):
#
#     xlsx = load_workbook(filename)
#     tab = xlsx.worksheets[1]
#     category_name_column = None
#     category_code_column = None
#     subcategory_name_column = None
#     subcategory_code_column = None
#
#     for sym in string.ascii_uppercase:
#         cell = tab[f'{sym}1'].value
#         print(cell)
#         if cell and 'Код из ФГИС ФСА для подкатегории продукции' in cell:
#             subcategory_code_column = sym
#         if cell and 'Подкатегория продукции' in cell:
#             subcategory_name_column = sym
#         if cell and 'Категория продукции' in cell:
#             category_name_column = sym
#         if cell and 'Раздел ЕП РФ (Код)' in cell:
#             category_code_column = sym
#         if subcategory_name_column and subcategory_code_column:
#             break
#
#     if not subcategory_name_column or not subcategory_code_column:
#         raise RuntimeError(f'subcategory_name_column={subcategory_name_column} '
#                            f'subcategory_code_column={subcategory_code_column}')
#
#
#
#     i = 2
#     while True:
#         #             category_name_column = sym
#         #         if cell and 'Раздел ЕП РФ (Код)' in cell:
#         #             category_code_column = sym
#
#
#         if category_name_column and category_code_column:
#             cat_name = tab[f'{category_name_column}{i}'].value.strip().replace("\xc2\xa0", " ")
#             cat_code = tab[f'{category_code_column}{i}'].value.strip()
#
#             if not db.session.query(Category).filter(Category.code == cat_code):
#                 category = Category(code=cat_code, name=cat_name)
#                 db.session.add(category)
#                 db.session.commit()
#
#         if subcategory_name_column and subcategory_code_column:
#             cat_name = tab[f'{subcategory_name_column}{i}'].value.strip()
#             cat_code = tab[f'{subcategory_code_column}{i}'].value.strip()
#             if category_name_column and category_code_column:
#                 if not db.session.query(Category).filter(Category.code == cat_code):
#                     category = Category(code=cat_code, name=cat_name)
#                     db.session.add(category)
#                     db.session.commit()
#
#
#     i = 2
#     while True:
#         id = tab[f'A{i}'].value
#         name = tab[f'B{i}'].value
#         code = tab[f'C{i}'].value
#         sub_cat: str = tab[f'D{i}'].value
#         if id:
#             cat_f_writer.writerow([code.strip(), sub_cat.strip()])
#             i += 1
#         else:
#             print('doc end')
#             break
#
#     tab = xlsx.worksheets[0]
#
#     with  open('posuda_cat_product.csv', 'a', newline='', encoding='utf8') as cat_prod_f:
#         cat_prod_f_writer = csv.writer(cat_prod_f, delimiter=',', quoting=csv.QUOTE_ALL)
#         i = 1
#         while True:
#             id = tab[f'A{i}'].value
#             name = tab[f'B{i}'].value
#             code = tab[f'C{i}'].value
#             sub_cat: str = tab[f'D{i}'].value
#             if id:
#                 cat_prod_f_writer.writerow([sub_cat.strip(), code.strip(), name.strip()])
#                 i += 1
#             else:
#                 print('doc end')
#                 break
