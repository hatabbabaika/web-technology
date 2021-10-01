import os.path
import constants
from db.demiurge import create
from logic.api import api_app

if __name__ == '__main__':
    if not os.path.exists(constants.DB_NAME):
        # init db structure
        create()

    api_app.run()