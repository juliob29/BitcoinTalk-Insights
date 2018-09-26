"""
Script that manges the scheduled running of 
a model and its updating in the server application.
"""
import time 
import schedule 
import requests

from sanic.log import logger
from skill.word2vec import Model


def train_and_query():
    """
    Trains the word2vec model, generating a new
    tained model file into the specified MODELS_PATH
    path. Then hits the /update endpoint for updating
    the model with the latest available data.
    """
    Model().train()
    try:
        r = requests.get('http://localhost:8000/update')
        if r.status_code != 200:
            logger.info("Failure!")
        try:
            if r.json()['success'] == True:
                logger.info("Success is good!")
            else:
                logger.error('JSON does not have Success as True')
        except ValueError: 
            logger.error("There is no JSON Object")

    except requests.exceptions.ConnectionError:
        logger.error("No connection Found.")


if __name__ == '__main__':
    #
    #  Schedule the tain_and_query function
    #  and run it on the scheduler time.
    #
    schedule.every().monday.at("2:00").do(train_and_query)

    while True:
        schedule.run_pending()
        time.sleep(1)
