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
drop table if exists `mastery_level_student`;
create table `mastery_level_student` (
	`id` varchar(64) not null primary key,
	`student_id` bigint not null,
	`topic_id` char(32) not null,
	`channel_id` char(32) not null,
	`date` datetime,
	`completed_questions` int default 0,
	`correct_questions` int default 0,
	`attempt_questions` int default 0,
	`completed_topic` boolean default false
);
drop table if exists `mastery_level_class`;
create table `mastery_level_class` (
	`id` varchar(64) not null primary key,
	`class_id` bigint not null,
	`topic_id` char(32) not null,
	`channel_id` char(32) not null,
	`date` datetime,
	`completed_questions` int default 0,
	`correct_questions` int default 0,
	`attempt_questions` int default 0,
	`completed_topic` int default 0
);
drop table if exists `mastery_level_school`;
create table `mastery_level_school` (
	`id` varchar(64) not null primary key,
	`school_id` bigint not null,
	`topic_id` char(32) not null,
	`channel_id` char(32) not null,
	`date` datetime,
	`completed_questions` int default 0,
	`correct_questions` int default 0,
	`attempt_questions` int default 0,
	`completed_topic` int default 0
);
