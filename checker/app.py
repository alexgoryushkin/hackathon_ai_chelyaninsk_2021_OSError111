import os
import threading
from datetime import datetime
from typing import Tuple, List

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from sqlalchemy import func
from werkzeug.utils import secure_filename

import classifier
from name_checker import neuron_oracle
from models import Category, Task, SubTask, SessionManager, metadata, engine
from file_parser import file_to_farsh, extract_categories_from_file

app = Flask(__name__)
print('cors disabled')
CORS(app)

app.config['UPLOAD_FOLDER'] = '/uploads'

print('default_datasets', os.listdir('/default_datasets'))
classifier.init('/default_datasets/goods_fixed.csv')
with SessionManager() as session:
    # session.drop_all()
    metadata.create_all(engine)
    if not session.query(Category).first():
        start_time = datetime.now()
        extract_categories_from_file(
            session,
            r'/default_datasets/Реестр деклараций ПОСУДА ЕП РФ без 4000-8500.xlsx'
        )
        extract_categories_from_file(
            session,
            r'/default_datasets/Реестр 327 тыс. деклараций ЕП РФ без 140000-200000.xlsx'
        )
        print(f"Load categories to database for {datetime.now() - start_time}")

@app.route('/api/express', methods=['POST'])
def express():
    with SessionManager() as session:
        data = request.json
        print(data)
        categories, is_valid = neuron_oracle(session, data['name'].strip(), data['codes'])

        return jsonify({
            'сategories': [cat.to_json() for cat in categories],
            'isValid': is_valid
        }), 200


@app.route('/api/category_search', methods=['GET'])
def category_search():
    with SessionManager() as session:
        categories = session.query(Category).filter(
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

    with SessionManager() as session:
        task = Task(status='run')
        session.add(task)
        session.commit()

        thread = threading.Thread(None, target=file_to_farsh, args=(filename, file_ext, task.id))
        thread.start()
        # file_to_farsh(db, filename, file_ext, task)

        return jsonify({
            'task': task.to_json(session)
        }), 200


@app.route('/api/tasks', methods=['GET'], defaults={'task_id': None})
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_tasks(task_id):

    with SessionManager() as session:
        if task_id == 0:
            task = session.query(Task).order_by(Task.id.desc()).first()
            return jsonify({
                'task': task.to_json(session) if task else None
            }), 200

        if task_id:
            count_tasks = None
            if 'isValid' in request.args:
                query = session.query(SubTask).filter(SubTask.task_id == task_id, SubTask.is_valid==request.args['isValid'] )
            else:
                query = session.query(SubTask).filter(SubTask.task_id == task_id)
        else:
            count_tasks = session.query(func.count(Task.id)).scalar()
            query = session.query(Task).order_by(Task.id)

        if 'take' in request.args:
            query = query.limit(request.args['take'])
        if 'skip' in request.args:
            query = query.offset(request.args['skip'])

        return jsonify({
            'count': count_tasks,
            'subTasks' if task_id else 'tasks': [task.to_json(session) for task in query.all()]
        }), 200


print('app ok')

@app.route("/", defaults={'_': ''})
@app.route("/<path:_>")
def main_route(_):
    return render_template("index.html")
