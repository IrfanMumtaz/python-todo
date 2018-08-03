from flask import Flask, render_template, request, jsonify, url_for, redirect
from flask_cors import CORS
from flask_pymongo import PyMongo, pymongo
import sys, time
from bson.json_util import dumps, ObjectId

app = Flask(__name__)
app.config['MONGO_DBNAME']='todo'
app.config['MONGO_URI']='mongodb://todo_task:todo_task*123*@ds111082.mlab.com:11082/todo'

mongo = PyMongo(app)

cors = CORS(app, resources={r'/ajax/*': {"origins": '*'}})



@app.route('/')
def index():
    _tasks = mongo.db.tasks.find().sort('created_at', pymongo.DESCENDING)
    return  render_template('index.html', tasks=_tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    if request.method == 'POST':
        tasks = mongo.db.tasks
        data = {
            'task': request.form['task'],
            'status': 'view', 
            'created_at': time.strftime('%d-%m-%Y %H:%M:%S'), 
            'updated_at': time.strftime('%d-%m-%Y %H:%M:%S')
            }
        tasks.insert(data)
        return redirect(url_for('index'))

@app.route('/destroy_task')
def task_destroy():
    if request.method == 'GET':
        id = request.args.get('id')
        tasks = mongo.db.tasks
        result = tasks.find_one({'_id': ObjectId(id)})
        tasks.remove(result)
        return redirect(url_for('index'))


@app.route('/ajax/task_update', methods=['POST'])
def task_update():
    id = request.form['id']
    tasks = mongo.db.tasks
    result = tasks.find_one({'_id': ObjectId(id)})

    if result['status'] == 'completed':
        result['status'] = 'view'
        res = {"status": 'view'}
    else:
        result['status'] = 'completed'
        res = {"status": 'completed'}

    result['updated_at'] = time.strftime('%d-%m-%Y %H:%M:%S')

    tasks.save(result)

    return jsonify({'status': res})

@app.route('/actives')
def actives():
    tasks = mongo.db.tasks
    _tasks = tasks.find({'status': 'view'}).sort('created_at', pymongo.DESCENDING)
    return  render_template('index.html', tasks=_tasks)

@app.route('/completes')
def completes():
    tasks = mongo.db.tasks
    _tasks = tasks.find({'status': 'completed'}).sort('created_at', pymongo.DESCENDING)
    return  render_template('index.html', tasks=_tasks)

@app.route('/clear_completes')
def clear_completes():
    tasks = mongo.db.tasks
    tasks.remove({'status': 'completed'})
    return redirect(url_for('index'))



app.run(debug=True)