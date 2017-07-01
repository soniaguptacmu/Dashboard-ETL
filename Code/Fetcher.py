"""This class fetches data from source sqlite file and dumps into staging db"""
import logging
import traceback
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table
from sqlalchemy import orm

class Fetcher(object):
    """This class fetches data from source sqlite file and dumps into staging db"""

    def cleansink(self, sourcedbconnectionstring, sourceTableName, sinkDbConnectionString):
        """It cleans the staging db"""

        # Fetch data structure from source Table
        sourceDbEngine = create_engine(sourcedbconnectionstring)
        sourceDbEngine.echo = False
        metadata = MetaData(bind=sourceDbEngine)
        EntityTable = Table(sourceTableName, metadata, autoload=True)

        # establish sink connection
        sinkDbEngine = create_engine(sinkDbConnectionString)
        sinkConnection = sinkDbEngine.connect()
        sinkConnection.execute(EntityTable.delete())


    def transferSourceToSink(self, sourcedbconnectionstring, sourceTableName, sinkDbConnectionString):
        """fetches data from source and dump into sink"""

        try:
            # Establish source connection
            sourceDbEngine = create_engine(sourcedbconnectionstring)
            # sourceDbEngine = create_engine(sourcedbconnectionstring)
            sourceDbEngine.echo = False
            metadata = MetaData(bind=sourceDbEngine)

            # Fetch data structure from source table
            EntityTable = Table(sourceTableName, metadata, autoload=True)

            # establish sink connection
            sinkDbEngine = create_engine(sinkDbConnectionString)

            sinkConnection = sinkDbEngine.connect()

            class Entity(object):
                """These are the empty classes that will become our data classes"""
                pass

            # Map data structure of source  table to Entity class
            orm.mapper(Entity, EntityTable)

            # Fetch all data from source table
            Entity = EntityTable.select().execute()

            # Insert data from source db to sink db
            for row in Entity:
                sinkConnection.execute(EntityTable.insert(), row)

        except Exception as e:
            logging.basicConfig(filename='Fetcher.log', level=logging.ERROR)
            logging.error('There is an exception in the code Fetcher!')
            logging.error(e)
            logging.error(traceback.format_exc())
            raise