from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table
from sqlalchemy.sql import func
from sqlalchemy.sql import select
import uuid
import json
import logging
import traceback
import time

class Transformer(object):
	"""Perform the ETL job"""

	def __init__(self, staging_address, nalanda_address):
		super(Transformer, self).__init__()
		self.staging_engine = create_engine(staging_address)
		staging_metadata = MetaData(bind = self.staging_engine)
		self.Content_Summary_Log = Table('logger_contentsummarylog',staging_metadata,autoload=True,autoload_with=self.staging_engine)
		self.Mastery_Log = Table('logger_masterylog',staging_metadata,autoload=True,autoload_with=self.staging_engine)
		self.Attempt_Log = Table('logger_attemptlog',staging_metadata,autoload=True,autoload_with=self.staging_engine)
		self.Facility_User = Table('kolibriauth_facilityuser',staging_metadata,autoload=True,autoload_with=self.staging_engine)
		self.Collection = Table('kolibriauth_collection',staging_metadata,autoload=True,autoload_with=self.staging_engine)
		self.Membership = Table('kolibriauth_membership',staging_metadata,autoload=True,autoload_with=self.staging_engine)
		self.Content_Node = Table('content_contentnode',staging_metadata,autoload=True,autoload_with=self.staging_engine)
		self.Assessment = Table('content_assessmentmetadata',staging_metadata,autoload=True,autoload_with=self.staging_engine)
		self.staging_session = Session(self.staging_engine)
		Base = automap_base()
		engine = create_engine(nalanda_address)
		Base.prepare(engine,reflect=True)
		self.User_Info_Student = Base.classes.nalanda_userinfostudent
		self.User_Info_Class = Base.classes.nalanda_userinfoclass
		self.User_Info_School = Base.classes.nalanda_userinfoschool
		self.Mastery_Level_Student = Base.classes.nalanda_masterylevelstudent
		self.Mastery_Level_Class = Base.classes.nalanda_masterylevelclass
		self.Mastery_Level_School = Base.classes.nalanda_masterylevelschool
		self.Content = Base.classes.nalanda_content
		self.nalanda_session = Session(engine)

	def sync_student_info(self):
		try:
			result_set = self.staging_session\
							.query(self.Facility_User.c.id,self.Facility_User.c.username,self.Membership.c.collection_id)\
							.join(self.Membership, self.Membership.c.user_id==self.Facility_User.c.id).all()
			for record in result_set:
				_user_id = record[0]
				user_id = self.uuid2int(_user_id)
				_collection_id = record[2]
				collection_id = self.uuid2int(_collection_id)
				username = record[1]
				old_record = self.nalanda_session.query(self.User_Info_Student)\
								.filter(self.User_Info_Student.student_id==user_id).first()
				if not old_record:
					nalanda_record = self.User_Info_Student(student_id=user_id,student_name=username,parent=collection_id)
					self.nalanda_session.add(nalanda_record)
				else:
					self.nalanda_session.query(self.User_Info_Student)\
								.filter(self.User_Info_Student.student_id==user_id)\
								.update({"parent":collection_id})
			self.nalanda_session.commit()
			logging.basicConfig(filename='Fetcher.log', level=logging.INFO)
			logging.info('The synchronization of student information is completed at' + time.strftime("%c"))
		except Exception as e:
			logging.basicConfig(filename='Fetcher.log', level=logging.ERROR)
			logging.error('There is an exception in the Transformer!')
			logging.error(e)
			logging.error(traceback.format_exc())
			raise

	def sync_class_info(self):
		try:
			student_count = self.staging_session\
								.query(func.count(self.Facility_User.c.id),self.Membership.c.collection_id)\
								.join(self.Membership, self.Membership.c.user_id==self.Facility_User.c.id)\
								.group_by(self.Membership.c.collection_id).subquery()
			result_set = self.staging_session\
							.query(self.Collection.c.id,self.Collection.c.name,self.Collection.c.parent_id,student_count)\
							.join(student_count, student_count.c.collection_id==self.Collection.c.id).all()
			for record in result_set:
				_class_id = record[0]
				class_id = self.uuid2int(_class_id)
				_school_id = record[2]
				school_id = self.uuid2int(_school_id)
				class_name = record[1]
				total = record[3]
				old_record = self.nalanda_session.query(self.User_Info_Class)\
								.filter(self.User_Info_Class.class_id==class_id).first()
				if not old_record:
					nalanda_record = self.User_Info_Class(class_id=class_id,class_name=class_name,parent=school_id,total_students=total)
					self.nalanda_session.add(nalanda_record)
				else:
					self.nalanda_session.query(self.User_Info_Class)\
								.filter(self.User_Info_Class.class_id==class_id)\
								.update({"total_students":total})
			self.nalanda_session.commit()
			logging.basicConfig(filename='Fetcher.log', level=logging.INFO)
			logging.info('The synchronization of class information is completed at' + time.strftime("%c"))
		except Exception as e:
			logging.basicConfig(filename='Fetcher.log', level=logging.ERROR)
			logging.error('There is an exception in the Transformer!')
			logging.error(e)
			logging.error(traceback.format_exc())
			raise

	def sync_school_info(self):
		try:
			result_set = self.staging_session\
							.query(self.Collection.c.id,self.Collection.c.name,func.count(self.Facility_User.c.id))\
							.join(self.Facility_User, self.Collection.c.id==self.Facility_User.c.facility_id)\
							.group_by(self.Facility_User.c.facility_id).all()
			for record in result_set:
				_school_id = record[0]
				school_id = self.uuid2int(_school_id)
				school_name = record[1]
				total = record[2]
				old_record = self.nalanda_session.query(self.User_Info_School)\
								.filter(self.User_Info_School.school_id==school_id).first()
				if not old_record:
					nalanda_record = self.User_Info_School(school_id=school_id,school_name=school_name,total_students=total)
					self.nalanda_session.add(nalanda_record)
				else:
					self.nalanda_session.query(self.User_Info_School)\
								.filter(self.User_Info_School.school_id==school_id)\
								.update({'total_students':total})
			self.nalanda_session.commit()
			logging.basicConfig(filename='Fetcher.log', level=logging.INFO)
			logging.info('The synchronization of school information is completed at' + time.strftime("%c"))
		except Exception as e:
			logging.basicConfig(filename='Fetcher.log', level=logging.ERROR)
			logging.error('There is an exception in the Transformer!')
			logging.error(e)
			logging.error(traceback.format_exc())
			raise

	def sync_content(self):
		try:
			root_set = self.staging_session\
							.query(self.Content_Node.c.id,self.Content_Node.c.title,self.Content_Node.c.kind,self.Content_Node.c.content_id)\
							.filter(self.Content_Node.c.level==0)\
							.all()
			res = {}
			res['id'] = ''
			res['content_id'] = ''
			res['name'] = ''
			res['children'] = []
			total = -1
			for root in root_set:
				dic = self.dfs_content_reader(root,root[0])
				res['children'].append(dic)
			json_obj = json.dumps(res, ensure_ascii=False)
			old_record = self.nalanda_session.query(self.Content.topic_id)\
							.filter(self.Content.topic_id=='').first()
			if not old_record:
				nalanda_record = self.Content(topic_id='',content_id='',topic_name='',channel_id='',total_questions=-1,sub_topics=json_obj)
				self.nalanda_session.add(nalanda_record)
			else:
				self.nalanda_session.query(self.Content)\
							.filter(self.Content.topic_id=='')\
							.update({'sub_topics':json_obj})
			self.nalanda_session.commit()
			logging.basicConfig(filename='Fetcher.log', level=logging.INFO)
			logging.info('The synchronization of content information is completed at' + time.strftime("%c"))
		except Exception as e:
			logging.basicConfig(filename='Fetcher.log', level=logging.ERROR)
			logging.error('There is an exception in the Transformer!')
			logging.error(e)
			logging.error(traceback.format_exc())
			raise
		
	def dfs_content_reader(self, root, channel_id):
		try:
			if root[2] != 'topic':
				exercise = self.staging_session\
								.query(self.Assessment.c.number_of_assessments)\
								.filter(self.Assessment.c.contentnode_id==root[0]).first()
				res = {}
				if exercise:
					res['total'] = exercise[0]
				else:
					res['total'] = 0
				return res
			else:
				sub_level = self.staging_session\
								.query(self.Content_Node.c.id,self.Content_Node.c.title,self.Content_Node.c.kind,self.Content_Node.c.content_id)\
								.filter(self.Content_Node.c.parent_id==root[0]).all()
				res = {}
				res['id'] = root[0]
				res['channel_id'] = channel_id
				res['content_id'] = root[3]
				res['name'] = root[1]
				res['children'] = []
				total = 0
				for node in sub_level:
					node_res = self.dfs_content_reader(node,channel_id)
					total += node_res['total']
					if 'id' in node_res:
						res['children'].append(node_res)
				res['total'] = total
				json_obj = json.dumps(res, ensure_ascii=False)
				old_record = self.nalanda_session.query(self.Content).filter(self.Content.topic_id==res['id']).first()
				if not old_record:
					nalanda_record = self.Content(topic_id=res['id'],content_id=res['content_id'],channel_id=res['channel_id'],
													topic_name=res['name'],total_questions=res['total'],sub_topics=json_obj)
					self.nalanda_session.add(nalanda_record)
				else:
					self.nalanda_session.query(self.Content)\
								.filter(self.Content.topic_id==res['id'])\
								.update({'content_id':res['content_id'],'channel_id':res['channel_id'],'topic_name':res['name'],\
									'total_questions':res['total'],'sub_topics':json_obj})
				self.nalanda_session.commit()
				return res
		except Exception as e:
			logging.basicConfig(filename='Fetcher.log', level=logging.ERROR)
			logging.error('There is an exception in the Transformer!')
			logging.error(e)
			logging.error(traceback.format_exc())
			raise

	def completed_questions_aggregation_student(self, start_date):
		try:
			select_attempt_log = self.staging_session\
								.query(self.Attempt_Log.c.user_id,func.date(self.Attempt_Log.c.completion_timestamp).label("date"),\
									self.Attempt_Log.c.masterylog_id)\
								.filter(self.Attempt_Log.c.completion_timestamp >= start_date).filter(self.Attempt_Log.c.complete == True)\
								.subquery()
			join_mastery_log = self.staging_session.query(select_attempt_log,self.Mastery_Log.c.summarylog_id)\
								.join(self.Mastery_Log, self.Mastery_Log.c.id==select_attempt_log.c.masterylog_id).subquery()
			result_set = self.staging_session.query(join_mastery_log.c.user_id,self.Content_Summary_Log.c.content_id,join_mastery_log.c.date,\
							self.Content_Summary_Log.c.channel_id,func.count(join_mastery_log.c.user_id))\
						.join(self.Content_Summary_Log, self.Content_Summary_Log.c.id==join_mastery_log.c.summarylog_id)\
						.group_by(join_mastery_log.c.date,join_mastery_log.c.user_id,join_mastery_log.c.summarylog_id)\
						.all()		
			for record in result_set:
				_student_id = record[0]
				student_id = self.uuid2int(_student_id)
				content_id = record[1]
				channel_id = record[3]
				date = record[2]
				completed_questions = record[4]
				old_record = self.nalanda_session.query(self.Mastery_Level_Student).filter(self.Mastery_Level_Student.student_id_id==student_id\
					,self.Mastery_Level_Student.content_id==content_id,self.Mastery_Level_Student.channel_id==channel_id,self.Mastery_Level_Student.date==date)\
					.first()
				if not old_record:
					nalanda_record = self.Mastery_Level_Student(id=str(uuid.uuid4()),student_id_id=student_id,content_id=content_id,\
											channel_id=channel_id,date=date,completed_questions=completed_questions)
					self.nalanda_session.add(nalanda_record)
				else:
					self.nalanda_session.query(self.Mastery_Level_Student)\
								.filter(self.Mastery_Level_Student.student_id_id==student_id,self.Mastery_Level_Student.content_id==content_id,\
									self.Mastery_Level_Student.channel_id==channel_id,self.Mastery_Level_Student.date==date)\
								.update({'completed_questions':completed_questions})
			self.nalanda_session.commit()
			logging.basicConfig(filename='Fetcher.log', level=logging.INFO)
			logging.info('The synchronization of student completed questions is completed at' + time.strftime("%c"))
		except Exception as e:
			logging.basicConfig(filename='Fetcher.log', level=logging.ERROR)
			logging.error('There is an exception in the Transformer!')
			logging.error(e)
			logging.error(traceback.format_exc())
			raise

	def correct_questions_aggregation_student(self, start_date):
		try:
			select_attempt_log = self.staging_session\
								.query(self.Attempt_Log.c.user_id,func.date(self.Attempt_Log.c.completion_timestamp).label("date"),\
									self.Attempt_Log.c.masterylog_id)\
								.filter(self.Attempt_Log.c.completion_timestamp >= start_date).filter(self.Attempt_Log.c.correct == 1)\
								.subquery()
			join_mastery_log = self.staging_session.query(select_attempt_log,self.Mastery_Log.c.summarylog_id)\
								.join(self.Mastery_Log, self.Mastery_Log.c.id==select_attempt_log.c.masterylog_id).subquery()
			result_set = self.staging_session.query(join_mastery_log.c.user_id,self.Content_Summary_Log.c.content_id,join_mastery_log.c.date,\
							self.Content_Summary_Log.c.channel_id,func.count(join_mastery_log.c.user_id))\
						.join(self.Content_Summary_Log, self.Content_Summary_Log.c.id==join_mastery_log.c.summarylog_id)\
						.group_by(join_mastery_log.c.date,join_mastery_log.c.user_id,join_mastery_log.c.summarylog_id)\
						.all()		
			for record in result_set:
				_student_id = record[0]
				student_id = self.uuid2int(_student_id)
				content_id = record[1]
				channel_id = record[3]
				date = record[2]
				correct_questions = record[4]
				old_record = self.nalanda_session.query(self.Mastery_Level_Student).filter(self.Mastery_Level_Student.student_id_id==student_id\
					,self.Mastery_Level_Student.content_id==content_id,self.Mastery_Level_Student.channel_id==channel_id,self.Mastery_Level_Student.date==date)\
					.first()
				if not old_record:
					nalanda_record = self.Mastery_Level_Student(id=str(uuid.uuid4()),student_id_id=student_id,content_id=content_id,\
											channel_id=channel_id,date=date,correct_questions=correct_questions)
					self.nalanda_session.add(nalanda_record)
				else:
					self.nalanda_session.query(self.Mastery_Level_Student)\
								.filter(self.Mastery_Level_Student.student_id_id==student_id,self.Mastery_Level_Student.content_id==content_id,\
									self.Mastery_Level_Student.channel_id==channel_id,self.Mastery_Level_Student.date==date)\
								.update({'correct_questions':correct_questions})
			self.nalanda_session.commit()
			logging.basicConfig(filename='Fetcher.log', level=logging.INFO)
			logging.info('The synchronization of student correct questions is completed at' + time.strftime("%c"))
		except Exception as e:
			logging.basicConfig(filename='Fetcher.log', level=logging.ERROR)
			logging.error('There is an exception in the Transformer!')
			logging.error(e)
			logging.error(traceback.format_exc())
			raise

	def attempted_questions_aggregation_student(self, start_date):
		try:
			select_attempt_log = self.staging_session\
								.query(self.Attempt_Log.c.user_id,func.date(self.Attempt_Log.c.start_timestamp).label("date"),\
									self.Attempt_Log.c.masterylog_id)\
								.filter(self.Attempt_Log.c.start_timestamp >= start_date)\
								.subquery()
			join_mastery_log = self.staging_session.query(select_attempt_log,self.Mastery_Log.c.summarylog_id)\
								.join(self.Mastery_Log, self.Mastery_Log.c.id==select_attempt_log.c.masterylog_id).subquery()
			result_set = self.staging_session.query(join_mastery_log.c.user_id,self.Content_Summary_Log.c.content_id,join_mastery_log.c.date,\
							self.Content_Summary_Log.c.channel_id,func.count(join_mastery_log.c.user_id))\
						.join(self.Content_Summary_Log, self.Content_Summary_Log.c.id==join_mastery_log.c.summarylog_id)\
						.group_by(join_mastery_log.c.date,join_mastery_log.c.user_id,join_mastery_log.c.summarylog_id)\
						.all()		
			for record in result_set:
				_student_id = record[0]
				student_id = self.uuid2int(_student_id)
				content_id = record[1]
				channel_id = record[3]
				date = record[2]
				attempt_questions = record[4]
				old_record = self.nalanda_session.query(self.Mastery_Level_Student).filter(self.Mastery_Level_Student.student_id_id==student_id\
					,self.Mastery_Level_Student.content_id==content_id,self.Mastery_Level_Student.channel_id==channel_id,self.Mastery_Level_Student.date==date)\
					.first()
				if not old_record:
					nalanda_record = self.Mastery_Level_Student(id=str(uuid.uuid4()),student_id_id=student_id,content_id=content_id,\
											channel_id=channel_id,date=date,attempt_questions=attempt_questions)
					self.nalanda_session.add(nalanda_record)
				else:
					self.nalanda_session.query(self.Mastery_Level_Student)\
								.filter(self.Mastery_Level_Student.student_id_id==student_id,self.Mastery_Level_Student.content_id==content_id,\
									self.Mastery_Level_Student.channel_id==channel_id,self.Mastery_Level_Student.date==date)\
								.update({'attempt_questions':attempt_questions})
			self.nalanda_session.commit()
			logging.basicConfig(filename='Fetcher.log', level=logging.INFO)
			logging.info('The synchronization of student attempted questions is completed at' + time.strftime("%c"))
		except Exception as e:
			logging.basicConfig(filename='Fetcher.log', level=logging.ERROR)
			logging.error('There is an exception in the Transformer!')
			logging.error(e)
			logging.error(traceback.format_exc())
			raise

	def completed_student(self, start_date):
		try:
			result_set = self.staging_session\
						.query(self.Content_Summary_Log.c.user_id,self.Content_Summary_Log.c.content_id,\
							func.date(self.Content_Summary_Log.c.completion_timestamp),self.Content_Summary_Log.c.channel_id) \
						.filter(self.Content_Summary_Log.c.completion_timestamp >= start_date)
			for record in result_set:
				_student_id = record[0]
				student_id = self.uuid2int(_student_id)
				content_id = record[1]
				channel_id = record[3]
				date = record[2]
				old_record = self.nalanda_session.query(self.Mastery_Level_Student).filter(self.Mastery_Level_Student.student_id_id==student_id\
					,self.Mastery_Level_Student.content_id==content_id,self.Mastery_Level_Student.channel_id==channel_id,self.Mastery_Level_Student.date==date)\
					.first()
				if not old_record:
					nalanda_record = self.Mastery_Level_Student(id=str(uuid.uuid4()),student_id_id=student_id,content_id=content_id,\
											channel_id=channel_id,date=date,completed=True)
					self.nalanda_session.add(nalanda_record)
				else:
					self.nalanda_session.query(self.Mastery_Level_Student)\
								.filter(self.Mastery_Level_Student.student_id_id==student_id,self.Mastery_Level_Student.content_id==content_id,\
									self.Mastery_Level_Student.channel_id==channel_id,self.Mastery_Level_Student.date==date)\
								.update({'completed':True})
			self.nalanda_session.commit()
			logging.basicConfig(filename='Fetcher.log', level=logging.INFO)
			logging.info('The synchronization of topic completion status is completed at' + time.strftime("%c"))
		except Exception as e:
			logging.basicConfig(filename='Fetcher.log', level=logging.ERROR)
			logging.error('There is an exception in the Transformer!')
			logging.error(e)
			logging.error(traceback.format_exc())
			raise

	def mastery_level_aggregation_class(self, start_date):
		try:
			result_set = self.nalanda_session\
							.query(self.Mastery_Level_Student.date,self.Mastery_Level_Student.content_id,self.Mastery_Level_Student.channel_id,\
								func.sum(self.Mastery_Level_Student.completed_questions),func.sum(self.Mastery_Level_Student.correct_questions),\
								func.sum(self.Mastery_Level_Student.attempt_questions),func.sum(self.Mastery_Level_Student.completed),\
								self.User_Info_Student.parent)\
							.filter(self.Mastery_Level_Student.date >= start_date)\
							.join(self.User_Info_Student,self.Mastery_Level_Student.student_id_id==self.User_Info_Student.student_id)\
							.group_by(self.Mastery_Level_Student.date,self.Mastery_Level_Student.content_id,self.Mastery_Level_Student.channel_id,
								self.User_Info_Student.parent).all()
			for record in result_set:
				date = record[0]
				content_id = record[1]
				channel_id = record[2]
				completed_questions = record[3]
				correct_questions = record[4]
				attempt_questions = record[5]
				completed_topic = record[6]
				class_id = record[7]
				old_record = self.nalanda_session.query(self.Mastery_Level_Class)\
								.filter(self.Mastery_Level_Class.class_id_id==class_id,self.Mastery_Level_Class.content_id==content_id,\
									self.Mastery_Level_Class.channel_id==channel_id,self.Mastery_Level_Class.date==date).first()
				if not old_record:
					nalanda_record = self.Mastery_Level_Class(id=str(uuid.uuid4()),class_id_id=class_id,content_id=content_id,\
										channel_id=channel_id,date=date,completed_questions=completed_questions,correct_questions=correct_questions,\
										attempt_questions=attempt_questions,students_completed=completed_topic)
					self.nalanda_session.add(nalanda_record)
				else:
					self.nalanda_session.query(self.Mastery_Level_Class)\
									.filter(self.Mastery_Level_Class.class_id_id==class_id,self.Mastery_Level_Class.content_id==content_id,\
									self.Mastery_Level_Class.channel_id==channel_id,self.Mastery_Level_Class.date==date)\
									.update({'completed_questions':completed_questions,'correct_questions':correct_questions,\
										'attempt_questions':attempt_questions,'students_completed':completed_topic})
			self.nalanda_session.commit()
			logging.basicConfig(filename='Fetcher.log', level=logging.INFO)
			logging.info('The synchronization of class progress data is completed at' + time.strftime("%c"))
		except Exception as e:
			logging.basicConfig(filename='Fetcher.log', level=logging.ERROR)
			logging.error('There is an exception in the Transformer!')
			logging.error(e)
			logging.error(traceback.format_exc())
			raise

	def mastery_level_aggregation_school(self, start_date):
		try:
			result_set = self.nalanda_session\
							.query(self.Mastery_Level_Class.date,self.Mastery_Level_Class.content_id,self.Mastery_Level_Class.channel_id,\
								func.sum(self.Mastery_Level_Class.completed_questions),func.sum(self.Mastery_Level_Class.correct_questions),\
								func.sum(self.Mastery_Level_Class.attempt_questions),func.sum(self.Mastery_Level_Class.students_completed),\
								self.User_Info_Class.parent)\
							.filter(self.Mastery_Level_Class.date >= start_date)\
							.join(self.User_Info_Class,self.Mastery_Level_Class.class_id_id==self.User_Info_Class.class_id)\
							.group_by(self.Mastery_Level_Class.date,self.Mastery_Level_Class.content_id,self.Mastery_Level_Class.channel_id,
								self.User_Info_Class.parent).all()
			for record in result_set:
				date = record[0]
				content_id = record[1]
				channel_id = record[2]
				completed_questions = record[3]
				correct_questions = record[4]
				attempt_questions = record[5]
				completed_topic = record[6]
				school_id = record[7]
				old_record = self.nalanda_session.query(self.Mastery_Level_School)\
								.filter(self.Mastery_Level_School.school_id_id==school_id,self.Mastery_Level_School.content_id==content_id,\
									self.Mastery_Level_School.channel_id==channel_id,self.Mastery_Level_School.date==date).first()
				if not old_record:
					nalanda_record = self.Mastery_Level_School(id=str(uuid.uuid4()),school_id_id=school_id,content_id=content_id,\
										channel_id=channel_id,date=date,completed_questions=completed_questions,correct_questions=correct_questions,\
										attempt_questions=attempt_questions,students_completed=completed_topic)
					self.nalanda_session.add(nalanda_record)
				else:
					self.nalanda_session.query(self.Mastery_Level_School)\
									.filter(self.Mastery_Level_School.school_id_id==school_id,self.Mastery_Level_School.content_id==content_id,\
									self.Mastery_Level_School.channel_id==channel_id,self.Mastery_Level_School.date==date)\
									.update({'completed_questions':completed_questions,'correct_questions':correct_questions,\
										'attempt_questions':attempt_questions,'students_completed':completed_topic})
			self.nalanda_session.commit()
			logging.basicConfig(filename='Fetcher.log', level=logging.INFO)
			logging.info('The synchronization of school progress data is completed at' + time.strftime("%c"))
		except Exception as e:
			logging.basicConfig(filename='Fetcher.log', level=logging.ERROR)
			logging.error('There is an exception in the Transformer!')
			logging.error(e)
			logging.error(traceback.format_exc())
			raise

	def clear_resource(self):
		self.nalanda_session.close()
		self.staging_session.close()

	def uuid2int(self, raw):
		return uuid.UUID(raw).int >> 65
		
