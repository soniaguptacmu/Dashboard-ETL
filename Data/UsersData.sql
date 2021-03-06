INSERT INTO kolibriauth_deviceowner VALUES('pbkdf2_sha256$24000$deSBcClSbQlU$6uNWFfLsnelugGfE3/tS8Inyry3z28TmBIXsj7olkQM=','2017-06-17 23:16:53.558925','admin','','2017-06-17 21:39:20.768218','f4852a32869d4350a3b59a79e3af89c0');
CREATE TABLE kolibriauth_facilitydataset (id char(32) NOT NULL PRIMARY KEY, _morango_dirty_bit bool NOT NULL, _morango_source_id varchar(96) NOT NULL, _morango_partition varchar(128) NOT NULL, description text NOT NULL, location varchar(200) NOT NULL, learner_can_edit_username bool NOT NULL, learner_can_edit_name bool NOT NULL, learner_can_edit_password bool NOT NULL, learner_can_sign_up bool NOT NULL, learner_can_delete_account bool NOT NULL);
INSERT INTO kolibriauth_facilitydataset VALUES('40ab2935082777580179b68d26be0e70',1,'40ab2935082777580179b68d26be0e70','40ab2935082777580179b68d26be0e70:crossuser','','',1,1,1,1,1);
CREATE TABLE kolibriauth_collection (id char(32) NOT NULL PRIMARY KEY, _morango_dirty_bit bool NOT NULL, _morango_source_id varchar(96) NOT NULL, 
	_morango_partition varchar(128) NOT NULL, name varchar(100) NOT NULL, kind varchar(20) NOT NULL, lft integer unsigned NOT NULL, rght integer unsigned NOT NULL,
	 tree_id integer unsigned NOT NULL, level integer unsigned NOT NULL, 
	 dataset_id char(32) NOT NULL REFERENCES kolibriauth_facilitydataset (id), 
	 parent_id char(32) NULL REFERENCES kolibriauth_collection (id));
INSERT INTO kolibriauth_collection VALUES('3cc97515ad8d53031c5542057717aad1',1,'475fec4a0b9144f093a16e96d4936382','40ab2935082777580179b68d26be0e70:crossuser','nalanda','facility',1,8,1,0,'40ab2935082777580179b68d26be0e70',NULL);
INSERT INTO kolibriauth_collection VALUES('2c22e7bf8bd31af17cee0f04b9136561',1,'e10b2820f5314c9794f0e1e5b2ae4b8c','40ab2935082777580179b68d26be0e70:crossuser','class 1','classroom',2,3,1,1,'40ab2935082777580179b68d26be0e70','3cc97515ad8d53031c5542057717aad1');
INSERT INTO kolibriauth_collection VALUES('4489cd93a786995f3dcee8cd09f4162b',1,'fdd52083651a4d2f962aedf04fca7550','40ab2935082777580179b68d26be0e70:crossuser','class 2','classroom',4,5,1,1,'40ab2935082777580179b68d26be0e70','3cc97515ad8d53031c5542057717aad1');
INSERT INTO kolibriauth_collection VALUES('67c522786d2fbbe0c4679b1b1783e2f9',1,'f650ff568f9e4432825ad4fc2a0c79ad','40ab2935082777580179b68d26be0e70:crossuser','class 3','classroom',6,7,1,1,'40ab2935082777580179b68d26be0e70','3cc97515ad8d53031c5542057717aad1');
CREATE TABLE kolibriauth_role (id char(32) NOT NULL PRIMARY KEY, _morango_dirty_bit bool NOT NULL, _morango_source_id varchar(96) NOT NULL, 
	_morango_partition varchar(128) NOT NULL, 
	kind varchar(20) NOT NULL, 
	collection_id char(32) NOT NULL REFERENCES kolibriauth_collection (id), 
	dataset_id char(32) NOT NULL REFERENCES kolibriauth_facilitydataset (id), 
	user_id char(32) NOT NULL REFERENCES kolibriauth_facilityuser (id));
INSERT INTO kolibriauth_role VALUES('fb0938d6de6ac507a0d16256790a445f',1,'3cc97515ad8d53031c5542057717aad1:coach','40ab2935082777580179b68d26be0e70:userspecific:52ec8cc8b8e5c303718f61c014aa7011','coach','3cc97515ad8d53031c5542057717aad1','40ab2935082777580179b68d26be0e70','52ec8cc8b8e5c303718f61c014aa7011');
INSERT INTO kolibriauth_role VALUES('3cb1456fe5387555caa1a71e858401ac',1,'3cc97515ad8d53031c5542057717aad1:coach','40ab2935082777580179b68d26be0e70:userspecific:fe30e10cbaa58662740710fb1b42f94f','coach','3cc97515ad8d53031c5542057717aad1','40ab2935082777580179b68d26be0e70','fe30e10cbaa58662740710fb1b42f94f');
CREATE TABLE kolibriauth_membership (id char(32) NOT NULL PRIMARY KEY, _morango_dirty_bit bool NOT NULL, _morango_source_id varchar(96) NOT NULL, 
	_morango_partition varchar(128) NOT NULL, 
	collection_id char(32) NOT NULL REFERENCES kolibriauth_collection (id), 
	dataset_id char(32) NOT NULL REFERENCES kolibriauth_facilitydataset (id),
	 user_id char(32) NOT NULL REFERENCES kolibriauth_facilityuser (id));
INSERT INTO kolibriauth_membership VALUES('a493f7096557673defb383a5e513c151',1,'2c22e7bf8bd31af17cee0f04b9136561','40ab2935082777580179b68d26be0e70:userspecific:5356dae9e08762547f4fe910cf6c1553','2c22e7bf8bd31af17cee0f04b9136561','40ab2935082777580179b68d26be0e70','5356dae9e08762547f4fe910cf6c1553');
INSERT INTO kolibriauth_membership VALUES('72c44e1271034fe3cc2c6fc32b16e4fe',1,'2c22e7bf8bd31af17cee0f04b9136561','40ab2935082777580179b68d26be0e70:userspecific:e8964f7dae2fa4ad566b85dfc4c61cce','2c22e7bf8bd31af17cee0f04b9136561','40ab2935082777580179b68d26be0e70','e8964f7dae2fa4ad566b85dfc4c61cce');
INSERT INTO kolibriauth_membership VALUES('9545037bdbe8dd3b29eae83f2fe59240',1,'67c522786d2fbbe0c4679b1b1783e2f9','40ab2935082777580179b68d26be0e70:userspecific:37104f79cf8173fe0708f4ded8ff7e5d','67c522786d2fbbe0c4679b1b1783e2f9','40ab2935082777580179b68d26be0e70','37104f79cf8173fe0708f4ded8ff7e5d');
INSERT INTO kolibriauth_membership VALUES('76bf91bf922723ba15f281dc6cf6ab5e',1,'67c522786d2fbbe0c4679b1b1783e2f9','40ab2935082777580179b68d26be0e70:userspecific:d8bc5a1302a7e1a4fa0b7a7285b6735d','67c522786d2fbbe0c4679b1b1783e2f9','40ab2935082777580179b68d26be0e70','d8bc5a1302a7e1a4fa0b7a7285b6735d');
INSERT INTO kolibriauth_membership VALUES('fe34d891b6bcee9ec01912d0330dffb4',1,'67c522786d2fbbe0c4679b1b1783e2f9','40ab2935082777580179b68d26be0e70:userspecific:112063d4b09f30989f7476ca732891a7','67c522786d2fbbe0c4679b1b1783e2f9','40ab2935082777580179b68d26be0e70','112063d4b09f30989f7476ca732891a7');
INSERT INTO kolibriauth_membership VALUES('ca1a173d6a365f6bf50069e6824bdaf6',1,'4489cd93a786995f3dcee8cd09f4162b','40ab2935082777580179b68d26be0e70:userspecific:91bdbbda05c5f4016f8eab7c5db7a748','4489cd93a786995f3dcee8cd09f4162b','40ab2935082777580179b68d26be0e70','91bdbbda05c5f4016f8eab7c5db7a748');
INSERT INTO kolibriauth_membership VALUES('dfff45938e9c45215d8106ff3301d963',1,'4489cd93a786995f3dcee8cd09f4162b','40ab2935082777580179b68d26be0e70:userspecific:21a725fc51adbf65ffae21ae6155697b','4489cd93a786995f3dcee8cd09f4162b','40ab2935082777580179b68d26be0e70','21a725fc51adbf65ffae21ae6155697b');
INSERT INTO kolibriauth_membership VALUES('74c014f4add0c8bc3c5bf3d5c0d77b81',1,'4489cd93a786995f3dcee8cd09f4162b','40ab2935082777580179b68d26be0e70:userspecific:97668b274966ebd1a46714fa8be2bc3a','4489cd93a786995f3dcee8cd09f4162b','40ab2935082777580179b68d26be0e70','97668b274966ebd1a46714fa8be2bc3a');
INSERT INTO kolibriauth_membership VALUES('d85c9b5a5058ab1d46c7adfbe8c82312',1,'4489cd93a786995f3dcee8cd09f4162b','40ab2935082777580179b68d26be0e70:userspecific:d1b28655a73b0c516f4e6c81814891e2','4489cd93a786995f3dcee8cd09f4162b','40ab2935082777580179b68d26be0e70','d1b28655a73b0c516f4e6c81814891e2');
INSERT INTO kolibriauth_membership VALUES('014ed8630f31e5b209e1ac8026759869',1,'2c22e7bf8bd31af17cee0f04b9136561','40ab2935082777580179b68d26be0e70:userspecific:7a0ee8cd38d35f57f4c7b83cddf1b6fb','2c22e7bf8bd31af17cee0f04b9136561','40ab2935082777580179b68d26be0e70','7a0ee8cd38d35f57f4c7b83cddf1b6fb');
INSERT INTO kolibriauth_membership VALUES('616b684af9a09aa2494f2c7ab06a2c28',1,'2c22e7bf8bd31af17cee0f04b9136561','40ab2935082777580179b68d26be0e70:userspecific:596e92e8c802c70818a2ec6e6a84eb79','2c22e7bf8bd31af17cee0f04b9136561','40ab2935082777580179b68d26be0e70','596e92e8c802c70818a2ec6e6a84eb79');
INSERT INTO kolibriauth_membership VALUES('e2668acca9949644c80060fb6abc6565',1,'2c22e7bf8bd31af17cee0f04b9136561','40ab2935082777580179b68d26be0e70:userspecific:52ec8cc8b8e5c303718f61c014aa7011','2c22e7bf8bd31af17cee0f04b9136561','40ab2935082777580179b68d26be0e70','52ec8cc8b8e5c303718f61c014aa7011');
INSERT INTO kolibriauth_membership VALUES('416dbed6b133eb0a4eaf749c946141a8',1,'4489cd93a786995f3dcee8cd09f4162b','40ab2935082777580179b68d26be0e70:userspecific:fe30e10cbaa58662740710fb1b42f94f','4489cd93a786995f3dcee8cd09f4162b','40ab2935082777580179b68d26be0e70','fe30e10cbaa58662740710fb1b42f94f');
INSERT INTO kolibriauth_membership VALUES('a96bc423a7117786a66a701494bc5134',1,'67c522786d2fbbe0c4679b1b1783e2f9','40ab2935082777580179b68d26be0e70:userspecific:fe30e10cbaa58662740710fb1b42f94f','67c522786d2fbbe0c4679b1b1783e2f9','40ab2935082777580179b68d26be0e70','fe30e10cbaa58662740710fb1b42f94f');
CREATE TABLE kolibriauth_facilityuser (password varchar(128) NOT NULL, last_login datetime NULL, id char(32) NOT NULL PRIMARY KEY, 
	_morango_dirty_bit bool NOT NULL, _morango_source_id varchar(96) NOT NULL, _morango_partition varchar(128) NOT NULL,
	 username varchar(30) NOT NULL, full_name varchar(120) NOT NULL, date_joined datetime NOT NULL, 
	 dataset_id char(32) NOT NULL REFERENCES kolibriauth_facilitydataset (id), 
	 facility_id char(32) NOT NULL REFERENCES kolibriauth_collection (id));
INSERT INTO kolibriauth_facilityuser VALUES('pbkdf2_sha256$24000$XVmuUU4nJYIS$1UH1t9hW7V9MeTz5Xi7fRt5717WAW1B1+ITbZeR/ULE=',NULL,
	'5356dae9e08762547f4fe910cf6c1553',1,'23da47368e014b1fbe7dc349d5da46b3','40ab2935082777580179b68d26be0e70:userspecific:5356dae9e08762547f4fe910cf6c1553','minghan','minghan','2017-06-17 21:41:45.964586','40ab2935082777580179b68d26be0e70','3cc97515ad8d53031c5542057717aad1');
INSERT INTO kolibriauth_facilityuser VALUES('pbkdf2_sha256$24000$MNfmUpTCFxfU$K4LIxuvnB63IIblRwb3Y3DYD0VetsBW+LSPyVIvxMm8=','2017-06-17 23:17:38.799766',
	'37104f79cf8173fe0708f4ded8ff7e5d',1,'66bb46d170b04d5fbb27e2f326280fcd','40ab2935082777580179b68d26be0e70:userspecific:37104f79cf8173fe0708f4ded8ff7e5d','sonia','sonia','2017-06-17 21:41:55.031326','40ab2935082777580179b68d26be0e70','3cc97515ad8d53031c5542057717aad1');
INSERT INTO kolibriauth_facilityuser VALUES('pbkdf2_sha256$24000$27zabvxWVDRe$PK9VWaEQBTPXQZ5Ez2rMTWl6m/H/1NSL6RxPKIfs8MU=',NULL,
	'e8964f7dae2fa4ad566b85dfc4c61cce',1,'beadea8fc1bb4882847b0e1dfd0f7b20','40ab2935082777580179b68d26be0e70:userspecific:e8964f7dae2fa4ad566b85dfc4c61cce','renfei','renfei','2017-06-17 21:42:06.113487','40ab2935082777580179b68d26be0e70','3cc97515ad8d53031c5542057717aad1');
INSERT INTO kolibriauth_facilityuser VALUES('pbkdf2_sha256$24000$DKPWICnFRC9O$SiKfa9JHai6Ozux4M+mV+6Z5Cu0aF/bbn9BjE7DnLhU=',NULL,
	'97668b274966ebd1a46714fa8be2bc3a',1,'2de81f5a304d4aec95c434f8c5090428','40ab2935082777580179b68d26be0e70:userspecific:97668b274966ebd1a46714fa8be2bc3a','kunal','kunal','2017-06-17 23:12:06.334917','40ab2935082777580179b68d26be0e70','3cc97515ad8d53031c5542057717aad1');
INSERT INTO kolibriauth_facilityuser VALUES('pbkdf2_sha256$24000$MdgkAhRG7xM3$0nwhYS5eAR9qMoizO9Vfj9ht4F1dc7Y+0qYeDgaN8X0=',NULL,
	'112063d4b09f30989f7476ca732891a7',1,'8b2590142f014742a2e5b551559d621a','40ab2935082777580179b68d26be0e70:userspecific:112063d4b09f30989f7476ca732891a7','tapan','tapan','2017-06-17 23:12:16.952007','40ab2935082777580179b68d26be0e70','3cc97515ad8d53031c5542057717aad1');
INSERT INTO kolibriauth_facilityuser VALUES('pbkdf2_sha256$24000$5j38bLcjsu9f$Rr4PIpwrLwYXKyjfO3SN66MrybZvsnCrOZRkmFtUG1o=',NULL,
	'21a725fc51adbf65ffae21ae6155697b',1,'54bbbb6930e243e8b420c9343c972e73','40ab2935082777580179b68d26be0e70:userspecific:21a725fc51adbf65ffae21ae6155697b','shakti','shakti','2017-06-17 23:12:29.730077','40ab2935082777580179b68d26be0e70','3cc97515ad8d53031c5542057717aad1');
INSERT INTO kolibriauth_facilityuser VALUES('pbkdf2_sha256$24000$RVyUcsd9HwuC$xMsiSEN24B4d+utc9ifDtSXcvgK6uwmlJX3T9NOHzVo=',NULL,
	'91bdbbda05c5f4016f8eab7c5db7a748',1,'da52acb0e5304c0fbcc83342517065d3','40ab2935082777580179b68d26be0e70:userspecific:91bdbbda05c5f4016f8eab7c5db7a748','linda','linda','2017-06-17 23:12:41.372484','40ab2935082777580179b68d26be0e70','3cc97515ad8d53031c5542057717aad1');
INSERT INTO kolibriauth_facilityuser VALUES('pbkdf2_sha256$24000$2Yo2bRRZKit5$mIbnS4oweoEbu2GtDP365Jxo7YR599R53F03sg3OjGo=',NULL,
	'd8bc5a1302a7e1a4fa0b7a7285b6735d',1,'059ffb9930954f2c85dfd83536e90969','40ab2935082777580179b68d26be0e70:userspecific:d8bc5a1302a7e1a4fa0b7a7285b6735d','swati','swati','2017-06-17 23:13:06.369526','40ab2935082777580179b68d26be0e70','3cc97515ad8d53031c5542057717aad1');
INSERT INTO kolibriauth_facilityuser VALUES('pbkdf2_sha256$24000$VVbKzoNtc1hA$FR2vGuhR3uC077BXX/Xb97po2cMtz3HgjmhdK1sgQYM=',NULL,
	'596e92e8c802c70818a2ec6e6a84eb79',1,'7f44a67ecdea418a96cb29a177f6197e','40ab2935082777580179b68d26be0e70:userspecific:596e92e8c802c70818a2ec6e6a84eb79','vignesh','vignesh','2017-06-17 23:13:18.655537','40ab2935082777580179b68d26be0e70','3cc97515ad8d53031c5542057717aad1');
INSERT INTO kolibriauth_facilityuser VALUES('pbkdf2_sha256$24000$MeNzsmrRgH2x$rj5+7JqfByQ7Fanyk87r0PKa14Pop/CzgCMoP+FB4TI=',NULL,
	'6d31d1e3b1bd60d419a4fcb547901934',1,'2a633d8dae034673960445efcab56e46','40ab2935082777580179b68d26be0e70:userspecific:6d31d1e3b1bd60d419a4fcb547901934','xiaolei','xiaolei','2017-06-17 23:13:34.842317','40ab2935082777580179b68d26be0e70','3cc97515ad8d53031c5542057717aad1');
INSERT INTO kolibriauth_facilityuser VALUES('pbkdf2_sha256$24000$nJVVqhV6Inl4$TQ+hbDHThs8rIVZ1KojzliQLL3i5jjor/Q+LP9r5HIk=',NULL,
	'7a0ee8cd38d35f57f4c7b83cddf1b6fb',1,'ddc1bc4f593247729ae12a2e328cd04d','40ab2935082777580179b68d26be0e70:userspecific:7a0ee8cd38d35f57f4c7b83cddf1b6fb','sahashwat','shashwat','2017-06-17 23:13:55.014160','40ab2935082777580179b68d26be0e70','3cc97515ad8d53031c5542057717aad1');


INSERT INTO kolibriauth_facilityuser VALUES('pbkdf2_sha256$24000$EM0eAalPzEwM$QIvn3dMIT7m/iAJooBk7BCh+UDfgvJhtJzqvlST4TfM=',NULL,
	'52ec8cc8b8e5c303718f61c014aa7011',1,'d3e7bccecbcd41c0b96281d4b1f3a177','40ab2935082777580179b68d26be0e70:userspecific:52ec8cc8b8e5c303718f61c014aa7011','vivek','vivek','2017-06-17 21:42:20.328281','40ab2935082777580179b68d26be0e70','3cc97515ad8d53031c5542057717aad1');
INSERT INTO kolibriauth_facilityuser VALUES('pbkdf2_sha256$24000$s8Qf2XEe6tfV$HozrerAzsFB2aLvAaMnwb2TWdhBojbawtmQiKEQCUJ4=',NULL,
	'fe30e10cbaa58662740710fb1b42f94f',1,'eb2741d20018455896b9158b0630cc27','40ab2935082777580179b68d26be0e70:userspecific:fe30e10cbaa58662740710fb1b42f94f','vijay','vijay','2017-06-17 21:42:35.393797','40ab2935082777580179b68d26be0e70','3cc97515ad8d53031c5542057717aad1');


