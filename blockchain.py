from flask import Flask
from core import operation

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/requestblock/<data>')
def request_new(data):
    try:
        operation.generate_block(data)
        return "New block generated."
    except Exception as e:
        return e.message


@app.route('/blockchain')
def get_blockchain():
    return str(operation.get_block_chain())


@app.route('/getlastestblock')
def get_last_block():
    return operation.get_latest_block()


@app.route('/sendblock/<data>')
def receive_block(data):
    if operation.receive_block_chain(data):
        return "Success"
    else:
        return "Fail to update the blockchain, need to resolve the conflict"


@app.route('/init')
def init():
    operation.init_block()
    return "Init successfully"

if __name__ == '__main__':
    app.run()
