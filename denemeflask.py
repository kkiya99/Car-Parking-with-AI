from flask import Flask, request
app = Flask(__name__)

@app.route('/api/reset',methods=["POST"])
def hello():
    return {"Sensors":[6,38,7,2,2,1,1,2],"Relative":[10,1],"Angle":-15}

@app.route('/api/Action/SetAction',methods=["POST"])
def hellox():
    return {"Sensors":[6,38,7,2,2,1,1,2],"Relative":[10,1],"Angle":-15}

if __name__ == '__main__':
    app.run(port=8084)