import os
import threading
from typing import Tuple, List

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from name_checker import neuron_oracle
from models import db, Category, Task, SubTask
from file_parser import file_to_farsh, extract_categories_from_file

app = Flask(__name__)
print('cors disabled')
CORS(app)

app.config['UPLOAD_FOLDER'] = 'uploads'
# app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.environ['POSTGRES_USER']}:" \
                                        f"{os.environ['POSTGRES_PASSWORD']}@" \
                                        f"postgres.service:5432/" \
                                        f"{os.environ['POSTGRES_DB']}"
db.app = app
db.init_app(app)

# TODO: Скачивание xlsx

# db.drop_all()
# db.create_all()
#
# extract_categories_from_file(
#     db,
#     r'uploads/Реестр деклараций ПОСУДА ЕП РФ без 4000-8500.xlsx'
# )
# extract_categories_from_file(
#     db,
#     r'uploads/Реестр 327 тыс. деклараций ЕП РФ без 140000-200000.xlsx'
# )


@app.route('/api/express', methods=['POST'])
def express():
    data = request.json
    print(data)
    categories, is_valid = neuron_oracle(data['name'].strip(), data['codes'])

    return jsonify({
        'сategories': [cat.to_json() for cat in categories],
        'isValid': is_valid
    }), 200


@app.route('/api/category_search', methods=['GET'])
def category_search():
    categories = db.session.query(Category).filter(
        Category.name.ilike(f"%{request.args['like']}%"),
        Category.parent_code != None
    ).order_by(Category.code).limit(10).all()
    return jsonify({
        'categories': [cat.to_json() for cat in categories]
    }), 200


@app.route('/api/tasks', methods=['POST'])
def create_tasks():
    if 'file' not in request.files or not request.files['file'] or not request.files['file'].filename:
        print('\'file\' not found in request.files')
        return jsonify({
            'message': '\'file\' not found in request.files'
        }), 400
    file = request.files['file']
    file_ext = file.filename.split('.')[1]
    if file_ext != 'xlsx':
        print(f"bad ext {file_ext!r}")
        return jsonify({
            'message': f"Bad ext {file_ext!r}"
        }), 400

    filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(filename)
    print(f'File saved as {filename}')

    task = Task(status='run')
    db.session.add(task)
    db.session.commit()

    thread = threading.Thread(None, target=file_to_farsh, args=(db, filename, file_ext, task))
    thread.start()
    # file_to_farsh(db, filename, file_ext, task)

    return jsonify({
        'task': task.to_json()
    }), 200


@app.route('/api/tasks', methods=['GET'], defaults={'task_id': None})
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_tasks(task_id):
    if task_id == 0:
        task = db.session.query(Task).order_by(Task.id.desc()).first()
        return jsonify({
            'task': task.to_json() if task else None
        }), 200

    if task_id:
        query = db.session.query(SubTask).filter(SubTask.task_id == task_id)
    else:
        query = db.session.query(Task)

    if 'take' in request.args:
        query = query.limit(request.args['take'])
    if 'skip' in request.args:
        query = query.offset(request.args['skip'])

    return jsonify({
        'subTasks' if task_id else 'tasks': [task.to_json() for task in query.all()]
    }), 200


print('app ok')
