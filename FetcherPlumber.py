from os import walk
import configparser
import logging
import sys
import time
import traceback

from Fetcher import Fetcher

class FetcherPlumber(object):

    def SourceToStagingJob(self):

        logging.basicConfig(filename='Fetcher.log', level=logging.INFO)
        logging.info('New Job..Current time is: ' + time.strftime("%c"))

        # read from configuration file
        config = configparser.ConfigParser()
        config.read('Config')

        # log related
        logfilePath = config.get('SourceLocation', 'logdirectoryPath')
        logsourceTableNames = config.get('SourceDatabase', 'logtablenames')

        print('log table names')
        print(logsourceTableNames)
        logging.info('log table names')
        logging.info(logsourceTableNames)

        # content related
        contentfilePath = config.get('SourceLocation', 'contentdirectorypath')
        contentsourceTableNames = config.get('SourceDatabase', 'contentnames')

        print('content table names')
        print(contentfilePath)
        logging.info('content table names')
        logging.info(contentfilePath)

        sinkDbConnectionString = 'mysql+pymysql://root:' + config.get('ConnectionString',
                                                                      'sinkDbConnectionString')
        extension = config.get('SourceLocation', 'extension')

        # load content data
        self.LoadSourceToStaging(contentfilePath,sinkDbConnectionString,contentsourceTableNames,extension)

        print('Successfully fetched all the content data!')
        logging.info('Successfully fetched all the data!')

        # load log data
        self.LoadSourceToStaging(logfilePath,sinkDbConnectionString,logsourceTableNames,extension)

        print('Successfully fetched all the log data!')
        logging.info('Successfully fetched all the log data!')

    def LoadSourceToStaging(self, filePath,sinkDbConnectionString,sourceTableNames,extension):
        try:

            dbFiles = self.fetchFilesFromDirectory(filePath, extension)
            sourceTableNameList = sourceTableNames.split(",")

            # validate data fetched from configuration file
            if (not filePath):
                raise ValueError('Source File path is empty!')
            elif (not sinkDbConnectionString):
                raise ValueError('Sink DB connection string is empty!')
            elif (not sourceTableNames):
                raise ValueError('Source Table Names is empty!')
            elif (not dbFiles or len(dbFiles) == 0):
                raise ValueError('No Db files present!')

            # perform transfer of data from source db to sink db
            for sourceTableName in sourceTableNameList:
                obj = Fetcher()
                isCleaned = 0

                for dbfile in dbFiles:

                    dbfile=filePath+dbfile
                    sourcedbconnectionstring = 'sqlite:///' + dbfile

                    if (isCleaned == 0):
                        obj.cleanSink(sourcedbconnectionstring, sourceTableName, sinkDbConnectionString)
                        isCleaned = 1

                    obj.transferSourceToSink(sourcedbconnectionstring, sourceTableName, sinkDbConnectionString)

        except Exception as e:
            logging.basicConfig(filename='Fetcher.log', level=logging.ERROR)
            logging.error('There is an exception in the code FetcherPlumber!')
            logging.error(e)
            logging.error(traceback.format_exc())
            raise

    # fetch all sqlite files from the directory
    def fetchFilesFromDirectory(self, directoryPath, extension):
        f = []
        for (dirpath, dirnames, filenames) in walk(directoryPath):
            for file in filenames:
                if file.endswith(extension):
                    f.append(file)

        return f
