from flask import Flask,request
from flask import Flask
from core import operation as op
import threading
import iotpeer

app = Flask(__name__)
operation = op.Operation()
p2p_server=None

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
    return operation.latest_block.stringify_block()


@app.route('/authorizeme',methods=['POST'])
def authorize():

    if request.method=="POST":
        if "data" in request.form:
            data = request.form["data"]
            bc=operation.get_block_chain()
            bc=bc.split("\n")[:-1]
            for b in bc:
                if b.split(",")[3]==data:
                    return "Success"

    return "Failure"

@app.route('/aaddme',methods=['POST'])
def addme():
    if "data" in request.form:
        data=request.form["data"]
        # Broadcast new block to everyone
        iot=p2p_server.iot.iot1.send_data("NBLC","ABCD")
        return "Ok Requested on your behalf"


@app.route('/init')
def init():
    operation.init_block()
    return "Init successfully"


# @app.route('/stop')
# def stopp2p():
#     operation.stopp2p()
#     return "Stopped p2p"


if __name__ == '__main__':
    if operation.init_app():
        thread_flask = threading.Thread(target=app.run, args=(), kwargs={'port': 5001,'host':'0.0.0.0'})
        thread_flask.start()
        handlers = iotpeer.Handles(operation)
        p2p_server = iotpeer.p2pThread(handlers)
        p2p_server.start()

    else:
        print "initial process failed"
