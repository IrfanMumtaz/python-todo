from flask import Flask, render_template, request, jsonify, url_for, redirect
from flask_pymongo import PyMongo
import sys, time
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_DBNAME']='todo'
app.config['MONGO_URI']='mongodb://todo_task:todo_task*123*@ds111082.mlab.com:11082/todo'

mongo = PyMongo(app)



@app.route('/')
def index():
    _tasks = mongo.db.tasks.find().sort({'created_at': mongo.DESCENDING})
    return  render_template('index.html', tasks=_tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    if request.method == 'POST':
        data = {'task': request.form['task'], 'created_at': time.strftime('%d-%m-%Y %H:%M:%S'), 'updated_at': time.strftime('%d-%m-%Y %H:%M:%S')}
        mongo.db.tasks.insert(data)
        return redirect(url_for('index'))

@app.route('/destroy_task')
def task_destroy():
    if request.method == 'GET':
        id = request.args.get('id')
        mongo.db.tasks.delete_one({'_id': ObjectId(id)})
        return redirect(url_for('index'))


app.run(debug=True)