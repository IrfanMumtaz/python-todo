from flask import Flask, render_template, request, jsonify, url_for, redirect
from flask_pymongo import PyMongo
import sys

app = Flask(__name__)
app.config['MONGO_DBNAME']='todo'
app.config['MONGO_URI']='mongodb://todo_task:todo_task*123*@ds111082.mlab.com:11082/todo'
# app.config['MONGO_DBNAME'] = 'miti'
# app.config['MONGO_URI'] = 'mongodb://qasim:qasim@ds143030.mlab.com:43030/miti'
mongo = PyMongo(app)



@app.route('/')
def index():
    _tasks = mongo.db.tasks.find()
    return  render_template('index.html', tasks=_tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    if request.method == 'POST':
        data = {'task': request.form['task']}
        mongo.db.tasks.insert(data)
        return redirect(url_for('index'))

@app.route('/destroy_task')
def task_destroy():
    if request.method == 'GET':
        id = request.args.get('id')
        mongo.db.tasks.remove({'id': { '$oid': id }})
        return ''


app.run(debug=True)