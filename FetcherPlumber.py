from os import walk
import configparser

from Fetcher import Fetcher


class FetcherPlumber(object):
    # perform extract transform load from source kolibri db to staging db of Nalanda
    def SourceToStagingJob(self):
        try:
            # read from configuration file
            config = configparser.ConfigParser();
            config.read('Config');

            filePath = config.get('SourceLocation', 'directoryPath');
            sinkDbConnectionString = 'mysql+pymysql://root:'+config.get('ConnectionString', 'sinkDbConnectionString');
            sourceTableNames = config.get('SourceDatabase', 'names');
            extension = config.get('SourceLocation', 'extension');

            dbFiles = self.fetchFilesFromFirectory(filePath, extension);
            sourceTableNameList = sourceTableNames.split(",")

            # validate data fetched from configuration file
            if (not filePath):
                raise ValueError('Source File path is empty!');
            elif (not sinkDbConnectionString):
                raise ValueError('Sink DB connection string is empty!');
            elif (not sourceTableNames):
                raise ValueError('Source Table Names is empty!');
            elif (not dbFiles or len(dbFiles) == 0):
                raise ValueError('No Db files present!');

            # perform transfer of data from source db to sink db
            for dbfile in dbFiles:
                sourcedbconnectionstring = 'sqlite:///' + dbfile;
                for sourceTableName in sourceTableNameList:
                    obj = Fetcher();
                    obj.transferSourceToSink(sourcedbconnectionstring, sourceTableName, sinkDbConnectionString);

        except Exception as e:
            print(e);

    # fetch all sqlite files from the directory
    def fetchFilesFromFirectory(self, directoryPath, extension):
        f = []
        for (dirpath, dirnames, filenames) in walk('.'):
            for file in filenames:
                if file.endswith(extension):
                    f.append(file)

        return f;
