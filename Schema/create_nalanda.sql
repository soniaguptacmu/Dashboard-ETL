drop database if exists nalanda;
create database nalanda;
use nalanda;

drop table if exists `user_info_school`;
create table `user_info_school` (
	`school_id` bigint not null primary key,
	`school_name` varchar(140),
	`total_students` int
);
drop table if exists `user_info_class`;
create table `user_info_class` (
	`class_id` bigint not null primary key,
	`class_name` varchar(140),
	`total_students` int,
	`parent` bigint not null references user_info_school(school_id)
);
drop table if exists `user_info_student`;
create table `user_info_student` (
	`student_id` bigint not null primary key,
	`student_name` varchar(140),
	`parent` bigint not null references user_info_class(class_id)
);
drop table if exists `content`;
create table `content` (
	`topic_id` char(32) not null primary key,
	`topic_name` varchar(140),
	`total_questions` int default 0,
	`sub_topics` mediumtext default null
);