import schedule
import configparser
import logging
from FetcherPlumber import FetcherPlumber
import traceback


from Transformer_plumber import Transformer_plumber


def doETL():

    fetch_plumber = FetcherPlumber()
    transform_plumber = Transformer_plumber()

    fetch_plumber.SourceToStagingJob()
    transform_plumber.execute()

if __name__ == "__main__":

    try:
        config = configparser.ConfigParser()
        config.read('Config')
        timeInterval = int(config.get('TimeSettings', 'frequencyMinutes'))

        if (timeInterval >= 0):
            schedule.every(timeInterval).minutes.do(doETL)
            while 1:
                schedule.run_pending()
        else:
            raise ValueError('timeInterval is less than zero!')

    except Exception as e:
        logging.basicConfig(filename='Fetcher.log', level=logging.ERROR)
        logging.error('There is an exception in the code Schedular !')
        logging.error(e)
        logging.error(traceback.format_exc())



