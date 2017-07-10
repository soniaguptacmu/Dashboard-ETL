import unittest
import os
import sys
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table
from sqlalchemy import select, func, Integer, Table, Column, MetaData
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Fetcher import Fetcher

class test_Fetcher(unittest.TestCase):

    sinkDbConnectionString = 'mysql+pymysql://root:password@localhost/hell?charset=utf8'

    def test_transferSourceToSink(self):

        try:
            sourcedbconnectionstring='sqlite:///../../ContentData/eb99f209f9c34ba192f6e695aeb37e4f.sqlite3'

            sourceTableName='Content_contentnode'
            fetchObj=Fetcher()
            fetchObj.transferSourceToSink(sourcedbconnectionstring, sourceTableName, self.sinkDbConnectionString)
            self.assertTrue(True)
        except Exception as e:
            print(e)
            self.assertFalse(True,'There was an exception while loading from source to sink')

    def test_transferSourceToSink_actualData(self):

        try:
            sourcedbconnectionstring = 'sqlite:///../../ContentData/eb99f209f9c34ba192f6e695aeb37e4f.sqlite3'

            sourceTableName = 'Content_contentnode'

            fetchObj = Fetcher()
            fetchObj.transferSourceToSink(sourcedbconnectionstring, sourceTableName, self.sinkDbConnectionString)
            staging_engine = create_engine(self.sinkDbConnectionString)
            staging_metadata = MetaData(bind=staging_engine)
            Content_Node = Table('content_contentnode', staging_metadata, autoload=True,
                                      autoload_with=staging_engine)
            session=Session(staging_engine)
            self.assertTrue(session.query(Content_Node).count()>0)

        except Exception as e:
            print(e)
            self.assertFalse(True, 'There was an exception while loading from source to sink')

    def test_cleansink(self):
        try:
            sourcedbconnectionstring ='sqlite:///../../ContentData/eb99f209f9c34ba192f6e695aeb37e4f.sqlite3'

            sourceTableName = 'Content_contentnode'

            fetchObj = Fetcher()
            fetchObj.cleansink(sourcedbconnectionstring, sourceTableName, self.sinkDbConnectionString)
            self.assertTrue(True)
        except Exception as e:
            print(e)
            self.assertFalse(True,'There was an exception while cleaning the sink')

if __name__ == '__main__':
    unittest.main()