<<<<<<< HEAD
import transformer
def transformer_plumber():
        start_date = "2017-07-01 00:00:00"
        test = transformer.Transformer("mysql+mysqlconnector://root:@localhost/staging","mysql+mysqlconnector://root:@localhost/nalanda1")
        test.sync_student_info();
        test.sync_class_info();
        test.sync_school_info();
        #test.sync_content()
        test.clear_log(start_date)
        test.completed_questions_aggregation_student(start_date)
        test.correct_questions_aggregation_student(start_date)
        test.attempted_questions_aggregation_student(start_date)
        test.completed_student(start_date)
        test.mastery_level_aggregation_class(start_date)
        test.mastery_level_aggregation_school(start_date)
        test.clear_resource()

if __name__ == "__main__":
        transformer_plumber()
=======
import transformer
def transformer_plumber():
	start_date = "2017-06-23 00:00:00"
	test = transformer.Transformer("mysql+mysqlconnector://root:password@localhost/staging","mysql+mysqlconnector://root:password@localhost/nalanda")
	test.sync_student_info();
	test.sync_class_info();
	test.sync_school_info();
	test.sync_content();
	test.completed_questions_aggregation_student(start_date)
	test.correct_questions_aggregation_student(start_date)
	test.attempted_questions_aggregation_student(start_date)
	test.completed_student(start_date)
	test.mastery_level_aggregation_class(start_date)
	test.mastery_level_aggregation_school(start_date)
	test.clear_resource()

if __name__ == "__main__":
	transformer_plumber()
>>>>>>> 9fb6355d3dbc13bfa56681355919fcc9cea0d2db
