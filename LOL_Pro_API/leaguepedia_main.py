from flask import Flask
import cargo_fields

app = Flask(__name__)



@app.route('/cargoFields')
def getCargoFields():
    return cargo_fields.getCargoFields()




app.run("localhost", 3030)