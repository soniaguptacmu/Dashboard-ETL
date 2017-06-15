from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table
from sqlalchemy import orm


class Fetcher(object):
    # fetches data from source and dump into sink
    def transferSourceToSink(self, sourceDbConnectionString, sourceTableName, sinkDbConnectionString):

        try:
            # Establish source connection
            sourceDbEngine = create_engine(sourceDbConnectionString)
            sourceDbEngine.echo = False
            metadata = MetaData(bind=sourceDbEngine)

            # Fetch data structure from source table
            EntityTable = Table(sourceTableName, metadata, autoload=True)

            # establish sink connection
            sinkDbEngine = create_engine(sinkDbConnectionString)
            sinkConnection = sinkDbEngine.connect()

            # These are the empty classes that will become our data classes
            class Entity(object):
                pass

            # Map data structure of source source table to Entity class
            orm.mapper(Entity, EntityTable)

            # Fetch all data from source table
            Entity = EntityTable.select().execute();

            # Insert data from source db to sink db
            for row in Entity:
                sinkConnection.execute(EntityTable.insert(), row);

        except Exception as e:
            print(e);
            # todo: log into logfile
