import transformer
def transformer_plumber():
        start_date = "2017-07-10 00:00:00"
        test = transformer.Transformer("mysql+mysqlconnector://root:@localhost/stagingtest","mysql+mysqlconnector://root:@localhost/nalandatest")
        test.sync_student_info();
        test.sync_class_info();
        test.sync_school_info();
        test.sync_content()
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