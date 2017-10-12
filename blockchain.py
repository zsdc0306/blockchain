from flask import Flask
from core import block, operation

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/requestblock')
def request_new():
    pass


@app.route('/blockchain')
def get_blockchain():
    return operation.get_block_chain()


@app.route('/getlastestblock')
def get_last_block():
    return operation.get_latest_block()


if __name__ == '__main__':
    app.run()
