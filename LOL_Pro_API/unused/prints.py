from LOL_Pro_API.unused.cargo_fields import *
import json

def showCargoFields():
    print(json.dump(getCargoFields()))

showCargoFields()