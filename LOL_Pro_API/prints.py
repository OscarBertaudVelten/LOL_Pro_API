from cargo_fields import *
import json

def showCargoFields():
    print(json.dump(getCargoFields()))

showCargoFields()