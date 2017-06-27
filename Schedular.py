import schedule
import configparser
import logging

from FetcherPlumber import FetcherPlumber

if __name__ == "__main__":

    try:
        config = configparser.ConfigParser()
        config.read('Config')
        timeInterval = int(config.get('TimeSettings', 'frequencyMinutes'))

        plumber = FetcherPlumber()

        # for debugging pupose
        #plumber.SourceToStagingJob();

        if (timeInterval > 0):
            schedule.every(timeInterval).minutes.do(plumber.SourceToStagingJob)
            while 1:
                schedule.run_pending()

        else:
            raise ValueError('timeInterval is less than equal to zero!')

    except Exception as e:
        print(e)
        logging.basicConfig(filename='Fetcher.log', level=logging.ERROR)
        logging.error('There is an exception in the code Schedular !')
        logging.error(e)