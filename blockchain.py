from flask import Flask,request
from flask import Flask
from core import operation as op

app = Flask(__name__)
operation = op.Operation()


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


@app.route('/sendblock/<data>')
def receive_block(data):
    if operation.receive_block(data):
        return "Success"
    else:
        return "Fail to update the blockchain, need to resolve the conflict"

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
        iot=operation.p2p_server.iot.iot1.send_data("NBLC","ABCD")
        return "Ok Requested on your behalf"


@app.route('/init')
def init():
    operation.init_block()
    return "Init successfully"

@app.route('/stop')
def stopp2p():
    operation.stopp2p()
    return "Stopped p2p"

if __name__ == '__main__':
    if operation.init_app():
        import threading
        fs=threading.Thread(target=app.run,args=(),kwargs={'port':5001})
        fs.start()
        #app.run(port=5001)
    else:
        print "initial process failed"
