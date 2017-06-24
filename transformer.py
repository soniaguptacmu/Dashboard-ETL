from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table
from sqlalchemy.sql import func
from sqlalchemy.sql import select
import uuid
import json

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
		#self.Mastery_Level_Student = Table('exercise_completion_student',nalanda_metadata,autoload=True,autoload_with=self.nalanda_engine)
		#self.Mastery_Level_Class = Table('exercise_completion_student',nalanda_metadata,autoload=True,autoload_with=self.nalanda_engine)
		#self.Mastery_Level_School = Table('exercise_completion_student',nalanda_metadata,autoload=True,autoload_with=self.nalanda_engine)
		Base = automap_base()
		engine = create_engine(nalanda_address)
		Base.prepare(engine,reflect=True)
		self.User_Info_Student = Base.classes.user_info_student
		self.User_Info_Class = Base.classes.user_info_class
		self.User_Info_School = Base.classes.user_info_school
		self.Content = Base.classes.content
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
		except:
			pass

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
		except:
			pass

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
		except:
			pass

	def sync_content(self):
		try:
			root_set = self.staging_session\
							.query(self.Content_Node.c.id,self.Content_Node.c.title,self.Content_Node.c.kind)\
							.filter(self.Content_Node.c.level==0)\
							.all()
			res = {}
			res['id'] = ''
			res['name'] = ''
			res['children'] = []
			total = -1
			for root in root_set:
				dic = self.dfs_content_reader(root)
				res['children'].append(dic)
			json_obj = json.dumps(res, ensure_ascii=False)
			old_record = self.nalanda_session.query(self.Content.topic_id)\
							.filter(self.Content.topic_id=='').first()
			if not old_record:
				nalanda_record = self.Content(topic_id='',topic_name='',total_questions=-1,sub_topics=json_obj)
				self.nalanda_session.add(nalanda_record)
			else:
				self.nalanda_session.query(self.Content)\
							.filter(self.Content.topic_id=='')\
							.update({'sub_topics':json_obj})
			self.nalanda_session.commit()
		except:
			pass
		
	def dfs_content_reader(self, root):
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
								.query(self.Content_Node.c.id,self.Content_Node.c.title,self.Content_Node.c.kind)\
								.filter(self.Content_Node.c.parent_id==root[0]).all()
				res = {}
				res['id'] = root[0]
				res['name'] = root[1]
				res['children'] = []
				total = 0
				for node in sub_level:
					node_res = self.dfs_content_reader(node)
					total += node_res['total']
					if 'id' in node_res:
						res['children'].append(node_res)
				res['total'] = total
				json_obj = json.dumps(res, ensure_ascii=False)
				old_record = self.nalanda_session.query(self.Content).filter(self.Content.topic_id==res['id']).first()
				if not old_record:
					nalanda_record = self.Content(topic_id=res['id'],topic_name=res['name'],total_questions=res['total'],sub_topics=json_obj)
					self.nalanda_session.add(nalanda_record)
				else:
					self.nalanda_session.query(self.Content)\
								.filter(self.Content.topic_id==res['id'])\
								.update({'topic_name':res['name'],'total_questions':res['total'],'sub_topics':json_obj})
				self.nalanda_session.commit()
				return res
			except:
				pass

	def completed_questions_aggregation_student(self, start_date):
		select_attempt_log = self.staging_session\
							.query(self.Attempt_Log.c.user_id, func.count(self.Attempt_Log.c.user_id),\
								func.date(self.Attempt_Log.c.completion_timestamp), self.Attempt_Log.c.masterylog_id)\
							.filter(self.Attempt_Log.c.completion_timestamp >= start_date).filter(self.Attempt_Log.c.complete == True)\
							.group_by(func.date(self.Attempt_Log.c.completion_timestamp),self.Attempt_Log.c.user_id, self.Attempt_Log.c.masterylog_id)\
							.subquery()
		join_mastery_log = self.staging_session.query(select_attempt_log,self.Mastery_Log.c.summarylog_id)\
							.join(self.Mastery_Log, self.Mastery_Log.c.id==select_attempt_log.c.masterylog_id).subquery()
		result_set = self.staging_session.query(join_mastery_log)\
					.join(self.Content_Summary_Log, self.Content_Summary_Log.c.id==join_mastery_log.c.summarylog_id)
		for u in result_set:
			print(u)

	def corrected_questions_aggregation_student(self, start_date):
		select_attempt_log = self.staging_session\
							.query(self.Attempt_Log.c.user_id, func.count(self.Attempt_Log.c.user_id),\
								func.date(self.Attempt_Log.c.completion_timestamp), self.Attempt_Log.c.masterylog_id)\
							.filter(self.Attempt_Log.c.completion_timestamp >= start_date).filter(self.Attempt_Log.c.correct == 1.0)\
							.group_by(func.date(self.Attempt_Log.c.completion_timestamp),self.Attempt_Log.c.user_id, self.Attempt_Log.c.masterylog_id)\
							.subquery()
		join_mastery_log = self.staging_session.query(select_attempt_log,self.Mastery_Log.c.summarylog_id)\
							.join(self.Mastery_Log, self.Mastery_Log.c.id==select_attempt_log.c.masterylog_id).subquery()
		result_set = self.staging_session.query(join_mastery_log)\
					.join(self.Content_Summary_Log, self.Content_Summary_Log.c.id==join_mastery_log.c.summarylog_id)
		for u in result_set:
			print(u)

	def attempted_questions_aggregation_student(self, start_date):
		select_attempt_log = self.staging_session\
							.query(self.Attempt_Log.c.user_id, func.count(self.Attempt_Log.c.user_id),\
								func.date(self.Attempt_Log.c.completion_timestamp), self.Attempt_Log.c.masterylog_id)\
							.filter(self.Attempt_Log.c.completion_timestamp >= start_date)\
							.group_by(func.date(self.Attempt_Log.c.completion_timestamp),self.Attempt_Log.c.user_id, self.Attempt_Log.c.masterylog_id)\
							.subquery()
		join_mastery_log = self.staging_session.query(select_attempt_log,self.Mastery_Log.c.summarylog_id)\
							.join(self.Mastery_Log, self.Mastery_Log.c.id==select_attempt_log.c.masterylog_id).subquery()
		result_set = self.staging_session.query(join_mastery_log)\
					.join(self.Content_Summary_Log, self.Content_Summary_Log.c.id==join_mastery_log.c.summarylog_id)
		for u in result_set:
			print(u)


	def completed_student(self, start_date):
		result_set = self.staging_session.query(self.Content_Summary_Log.c.user_id,self.Content_Summary_Log.c.content_id) \
			.filter(self.Content_Summary_Log.c.completion_timestamp >= start_date)
		for record in result_set:
			record_dict = record.__dict__
			_user_id = record_dict['user_id']
			user_id = uuid2int(_user_id)
			_content_id = record_dict['content_id']
			content_id = uuid2int(_content_id)
			nalanda_record = Mastery_Level_Student(student_id=user_id, topic_id=content_id,\
				date=record_dict['completion_timestamp'], completed=True)
			self.nalanda_session.add(nalanda_record)

	def completed_questions_aggregation_class(self, start_date):
		pass

	def corrected_questions_aggregation_class(self, start_date):
		pass

	def attempted_questions_aggregation_class(self, start_date):
		pass

	def completed_students(self, start_date):
		pass

	def completed_questions_aggregation_school(self, start_date):
		pass

	def corrected_questions_aggregation_school(self, start_date):
		pass

	def attempted_questions_aggregation_school(self, start_date):
		pass

	def completed_students(self,start_date):
		pass

	def clear_resource(self):
		pass

	def uuid2int(self, raw):
		return uuid.UUID(raw).int >> 65
		
