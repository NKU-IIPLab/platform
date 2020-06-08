CREATE DATABASE  IF NOT EXISTS `hop` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */;
USE `hop`;
-- MySQL dump 10.13  Distrib 8.0.11, for Win64 (x86_64)
--
-- Host: localhost    Database: hop
-- ------------------------------------------------------
-- Server version	8.0.11

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'文件处理'),(2,'聚类算法'),(3,'图形化'),(4,'数据处理'),(5,'分类算法'),(6,'模型结果'),(7,'回归算法'),(8,'自定义算法');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `channel`
--

DROP TABLE IF EXISTS `channel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `channel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(45) DEFAULT NULL,
  `channel_name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_UNIQUE` (`token`)
) ENGINE=InnoDB AUTO_INCREMENT=508 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `channel`
--

LOCK TABLES `channel` WRITE;
/*!40000 ALTER TABLE `channel` DISABLE KEYS */;
INSERT INTO `channel` VALUES (507,'1','specific.NseEfZHQ!jvMBkaJZUjin');
/*!40000 ALTER TABLE `channel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `edge`
--

DROP TABLE IF EXISTS `edge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `edge` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `edge_id` varchar(45) DEFAULT NULL,
  `source` varchar(45) DEFAULT NULL,
  `target` varchar(45) DEFAULT NULL,
  `start` json DEFAULT NULL,
  `end` json DEFAULT NULL,
  `start_point_id` varchar(45) DEFAULT NULL,
  `end_point_id` varchar(45) DEFAULT NULL,
  `start_point` json DEFAULT NULL,
  `end_point` json DEFAULT NULL,
  `shape` varchar(45) DEFAULT NULL,
  `type` varchar(45) DEFAULT NULL,
  `source_node_id` int(11) NOT NULL,
  `target_node_id` int(11) NOT NULL,
  `graph_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_source_node_id_idx` (`source_node_id`),
  KEY `fk_target_node_id_idx` (`target_node_id`),
  KEY `fk_edge_graph1_idx` (`graph_id`),
  CONSTRAINT `fk_edge_graph1` FOREIGN KEY (`graph_id`) REFERENCES `graph` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_source_node_id` FOREIGN KEY (`source_node_id`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_target_node_id` FOREIGN KEY (`target_node_id`) REFERENCES `node` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `edge`
--

LOCK TABLES `edge` WRITE;
/*!40000 ALTER TABLE `edge` DISABLE KEYS */;
INSERT INTO `edge` VALUES (1,'edge73','node1','node11','{\"x\": 0, \"y\": 17}','{\"x\": 0, \"y\": -17}','circle5','circle15','{\"x\": 279.53846153846155, \"y\": 160.5}','{\"x\": 168.46153846153845, \"y\": 255.5}','customEdge','edge',1,1,1),(2,'edge166','node1','node6','{\"x\": 0, \"y\": 17}','{\"x\": 0, \"y\": -17}','circle5','circle10','{\"x\": 313.1578947368421, \"y\": 160.5}','{\"x\": 386.8421052631579, \"y\": 258.5}','customEdge','edge',1,1,1),(3,'edge227','node11','node18','{\"x\": 0, \"y\": 17}','{\"x\": 0, \"y\": -17}','circle17','circle22','{\"x\": 170.87581699346404, \"y\": 290.5}','{\"x\": 325.12418300653593, \"y\": 408.5}','customEdge','edge',3,3,1),(4,'edge290','node11','node23','{\"x\": 0, \"y\": 17}','{\"x\": 0, \"y\": -17}','circle17','circle27','{\"x\": 148.56451612903226, \"y\": 290.5}','{\"x\": 152.43548387096774, \"y\": 410.5}','customEdge','edge',3,3,1),(5,'edge55','node1','node6','{\"x\": 0, \"y\": 17}','{\"x\": 0, \"y\": -17}','circle5','circle10','{\"x\": 312.0833333333333, \"y\": 188.5}','{\"x\": 373.9166666666667, \"y\": 237.5}','customEdge','edge',6,6,2),(6,'edge93','node1','node11','{\"x\": 0, \"y\": 17}','{\"x\": 0, \"y\": -17}','circle5','circle15','{\"x\": 272.1195652173913, \"y\": 188.5}','{\"x\": 213.8804347826087, \"y\": 245.5}','customEdge','edge',6,6,2),(7,'edge124','node11','node18','{\"x\": 0, \"y\": 17}','{\"x\": 0, \"y\": -17}','circle17','circle22','{\"x\": 215.6681415929203, \"y\": 280.5}','{\"x\": 303.33185840707966, \"y\": 358.5}','customEdge','edge',8,8,2);
/*!40000 ALTER TABLE `edge` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `file`
--

DROP TABLE IF EXISTS `file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `file` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text,
  `status` varchar(45) DEFAULT NULL,
  `size` varchar(45) DEFAULT NULL,
  `percentage` int(11) DEFAULT NULL,
  `filepath` text,
  `graph_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_file_graph1_idx` (`graph_id`),
  CONSTRAINT `fk_file_graph1` FOREIGN KEY (`graph_id`) REFERENCES `graph` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `file`
--

LOCK TABLES `file` WRITE;
/*!40000 ALTER TABLE `file` DISABLE KEYS */;
INSERT INTO `file` VALUES (1,'iris.csv','success','4702',100,'k-means\\upload\\iris.csv',1),(2,'iris.csv','success','4702',100,'knn\\upload\\iris.csv',2);
/*!40000 ALTER TABLE `file` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `graph`
--

DROP TABLE IF EXISTS `graph`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `graph` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_name` varchar(120) DEFAULT NULL,
  `owner` varchar(120) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `modified_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `graph`
--

LOCK TABLES `graph` WRITE;
/*!40000 ALTER TABLE `graph` DISABLE KEYS */;
INSERT INTO `graph` VALUES (1,'k-means','christ','2020-03-31 01:55:59','2020-03-31 01:58:12'),(2,'knn','christ','2020-03-31 01:59:44','2020-03-31 02:00:15');
/*!40000 ALTER TABLE `graph` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `node`
--

DROP TABLE IF EXISTS `node`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `node` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `node_id` varchar(45) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `type` varchar(45) DEFAULT NULL,
  `description` text,
  `raw_script_name` text,
  `status` varchar(45) DEFAULT NULL,
  `shape` varchar(45) DEFAULT NULL,
  `size` varchar(45) DEFAULT NULL,
  `color` varchar(45) DEFAULT NULL,
  `x` int(11) DEFAULT NULL,
  `y` int(11) DEFAULT NULL,
  `graph_id` int(11) NOT NULL,
  `template_id` int(11) NOT NULL,
  PRIMARY KEY (`id`,`graph_id`,`template_id`),
  KEY `fk_node_graph1_idx` (`graph_id`),
  KEY `fk_node_node_template1_idx` (`template_id`),
  CONSTRAINT `fk_node_graph1` FOREIGN KEY (`graph_id`) REFERENCES `graph` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_node_node_template1` FOREIGN KEY (`template_id`) REFERENCES `node_template` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `node`
--

LOCK TABLES `node` WRITE;
/*!40000 ALTER TABLE `node` DISABLE KEYS */;
INSERT INTO `node` VALUES (1,'node1','选择文件','node',NULL,'select.txt','complete','customNode','[170, 34]','#1890ff',300,143,1,1),(2,'node6','可视化文件','node',NULL,NULL,'init','customNode','[170, 34]','#1890ff',400,276,1,3),(3,'node11','特征选择','node',NULL,'feature.txt','complete','customNode','[170, 34]','#1890ff',148,273,1,5),(4,'node18','Kmeans','node',NULL,'KMeans.txt','complete','customNode','[170, 34]','#1890ff',348,426,1,7),(5,'node23','下载文件','node',NULL,NULL,'init','customNode','[170, 34]','#1890ff',153,428,1,4),(6,'node1','选择文件','node',NULL,'select.txt','complete','customNode','[170, 34]','#1890ff',290,171,2,1),(7,'node6','可视化文件','node',NULL,NULL,'init','customNode','[170, 34]','#1890ff',396,255,2,3),(8,'node11','特征选择','node',NULL,'feature.txt','complete','customNode','[170, 34]','#1890ff',196,263,2,5),(9,'node18','KNeighborsClassifier','node',NULL,'KNeighborsClassifier.txt','complete','customNode','[170, 34]','#1890ff',323,376,2,8);
/*!40000 ALTER TABLE `node` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `node_detail`
--

DROP TABLE IF EXISTS `node_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `node_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(45) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `label` varchar(45) DEFAULT NULL,
  `value` text,
  `node_id` int(11) NOT NULL,
  `graph_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_node_detail_node1_idx` (`node_id`,`graph_id`),
  CONSTRAINT `fk_node_detail_node1` FOREIGN KEY (`node_id`, `graph_id`) REFERENCES `node` (`id`, `graph_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `node_detail`
--

LOCK TABLES `node_detail` WRITE;
/*!40000 ALTER TABLE `node_detail` DISABLE KEYS */;
INSERT INTO `node_detail` VALUES (1,'input','name','名称','{\"value\": \"\\u9009\\u62e9\\u6587\\u4ef6\"}',1,1),(2,'selectFile','selectFile','选择','{\"value\": 1}',1,1),(3,'input','name','名称','{\"value\": \"\\u53ef\\u89c6\\u5316\\u6587\\u4ef6\"}',2,1),(4,'visualization','visualization','','{\"value\": \"\"}',2,1),(5,'input','name','名称','{\"value\": \"\\u7279\\u5f81\\u9009\\u62e9\"}',3,1),(6,'input','feature_line','特征列（如1,2,3）','{\"value\": \"1,2,3,4,5\"}',3,1),(7,'preview','preview','','{\"value\": \"\"}',3,1),(8,'input','name','名称','{\"value\": \"KMeans\"}',4,1),(9,'inputNumber','n_clusters','n_clusters','{\"value\": 8}',4,1),(10,'input','init','init','{\"value\": \"k-means++\"}',4,1),(11,'inputNumber','n_init','n_init','{\"value\": 10}',4,1),(12,'inputNumber','max_iter','max_iter','{\"value\": 300}',4,1),(13,'inputNumber','tol','tol','{\"value\": 0.0001}',4,1),(14,'input','precompute_distances','precompute_distances','{\"value\": \"auto\"}',4,1),(15,'inputNumber','verbose','verbose','{\"value\": 0}',4,1),(16,'input','random_state','random_state','{\"value\": null}',4,1),(17,'checkbox','copy_x','copy_x','{\"value\": true}',4,1),(18,'input','n_jobs','n_jobs','{\"value\": null}',4,1),(19,'input','algorithm','algorithm','{\"value\": \"auto\"}',4,1),(20,'input','name','名称','{\"value\": \"\\u4e0b\\u8f7d\\u6587\\u4ef6\"}',5,1),(21,'download','download','下载','{\"value\": \"\"}',5,1),(22,'input','name','名称','{\"value\": \"\\u9009\\u62e9\\u6587\\u4ef6\"}',6,2),(23,'selectFile','selectFile','选择','{\"value\": 2}',6,2),(24,'input','name','名称','{\"value\": \"\\u53ef\\u89c6\\u5316\\u6587\\u4ef6\"}',7,2),(25,'visualization','visualization','','{\"value\": \"\"}',7,2),(26,'input','name','名称','{\"value\": \"\\u7279\\u5f81\\u9009\\u62e9\"}',8,2),(27,'input','feature_line','特征列（如1,2,3）','{\"value\": \"1,2,3,4,5\"}',8,2),(28,'preview','preview','','{\"value\": \"\"}',8,2),(29,'input','name','名称','{\"value\": \"Knn\"}',9,2),(30,'inputNumber','n_neighbors','n_neighbors','{\"value\": 5}',9,2),(31,'input','weights','weights','{\"value\": \"uniform\"}',9,2),(32,'input','algorithm','algorithm','{\"value\": \"auto\"}',9,2),(33,'inputNumber','leaf_size','leaf_size','{\"value\": 30}',9,2),(34,'inputNumber','p','p','{\"value\": 2}',9,2),(35,'input','metric','metric','{\"value\": \"minkowski\"}',9,2),(36,'input','metric_params','metric_params','{\"value\": null}',9,2),(37,'input','n_jobs','n_jobs','{\"value\": null}',9,2);
/*!40000 ALTER TABLE `node_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `node_template`
--

DROP TABLE IF EXISTS `node_template`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `node_template` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `raw_script_name` text,
  `shape` varchar(45) DEFAULT NULL,
  `size` varchar(45) DEFAULT NULL,
  `color` varchar(45) DEFAULT NULL,
  `node_detail` json DEFAULT NULL,
  `point_detail` json DEFAULT NULL,
  `category_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_node_template_category1_idx` (`category_id`),
  CONSTRAINT `fk_node_template_category1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `node_template`
--

LOCK TABLES `node_template` WRITE;
/*!40000 ALTER TABLE `node_template` DISABLE KEYS */;
INSERT INTO `node_template` VALUES (1,'选择文件','select.txt','customNode','170*34','#1890ff','[{\"name\": \"name\", \"type\": \"input\", \"label\": \"名称\", \"value\": \"选择文件\"}, {\"name\": \"selectFile\", \"type\": \"selectFile\", \"label\": \"选择\", \"value\": \"\"}]','[{\"func\": \"\", \"name\": \"文件\", \"type\": \"output\", \"proportion\": 0.5}]',1),(3,'可视化文件',NULL,'customNode','170*34','#1890ff','[{\"name\": \"name\", \"type\": \"input\", \"label\": \"名称\", \"value\": \"可视化文件\"}, {\"name\": \"visualization\", \"type\": \"visualization\", \"label\": \"\", \"value\": \"\"}]','[{\"func\": \"\", \"name\": \"文件\", \"type\": \"input\", \"proportion\": 0.5}]',3),(4,'下载文件',NULL,'customNode','170*34','#1890ff','[{\"name\": \"name\", \"type\": \"input\", \"label\": \"名称\", \"value\": \"下载文件\"}, {\"name\": \"download\", \"type\": \"download\", \"label\": \"下载\", \"value\": \"\"}]','[{\"func\": \"\", \"name\": \"文件\", \"type\": \"input\", \"proportion\": 0.5}]',3),(5,'特征选择','feature.txt','customNode','170*34','#1890ff','[{\"name\": \"name\", \"type\": \"input\", \"label\": \"名称\", \"value\": \"特征选择\"}, {\"name\": \"feature_line\", \"type\": \"input\", \"label\": \"特征列（如1,2,3）\", \"value\": \"1\"}, {\"name\": \"preview\", \"type\": \"preview\", \"label\": \"\", \"value\": \"\"}]','[{\"func\": \"\", \"name\": \"文件\", \"type\": \"input\", \"proportion\": 0.5}, {\"func\": \"\", \"name\": \"选择列\", \"type\": \"output\", \"proportion\": 0.5}]',4),(6,'SVC','SVC.txt','customNode','170*34','#1890ff','[{\"name\": \"name\", \"type\": \"input\", \"label\": \"名称\", \"value\": \"SVC\"}, {\"name\": \"C\", \"type\": \"inputNumber\", \"label\": \"C\", \"value\": 1}, {\"name\": \"kernel\", \"type\": \"input\", \"label\": \"kernel\", \"value\": \"rbf\"}, {\"name\": \"degree\", \"type\": \"inputNumber\", \"label\": \"degree\", \"value\": 3}, {\"name\": \"gamma\", \"type\": \"input\", \"label\": \"gamma\", \"value\": \"scale\"}, {\"name\": \"coef0\", \"type\": \"inputNumber\", \"label\": \"coef0\", \"value\": 0}, {\"name\": \"shrinking\", \"type\": \"checkbox\", \"label\": \"shrinking\", \"value\": true}, {\"name\": \"probability\", \"type\": \"checkbox\", \"label\": \"probability\", \"value\": false}, {\"name\": \"tol\", \"type\": \"inputNumber\", \"label\": \"tol\", \"value\": 0.001}, {\"name\": \"cache_size\", \"type\": \"inputNumber\", \"label\": \"cache_size\", \"value\": 200}, {\"name\": \"class_weight\", \"type\": \"input\", \"label\": \"class_weight\", \"value\": null}, {\"name\": \"verbose\", \"type\": \"checkbox\", \"label\": \"verbose\", \"value\": false}, {\"name\": \"max_iter\", \"type\": \"inputNumber\", \"label\": \"max_iter\", \"value\": -1}, {\"name\": \"decision_function_shape\", \"type\": \"input\", \"label\": \"decision_function_shape\", \"value\": \"ovr\"}, {\"name\": \"break_ties\", \"type\": \"checkbox\", \"label\": \"break_ties\", \"value\": false}, {\"name\": \"random_state\", \"type\": \"input\", \"label\": \"random_state\", \"value\": null}]','[{\"func\": \"\", \"name\": \"训练数据\", \"type\": \"input\", \"proportion\": 0.5}]',5),(7,'Kmeans','KMeans.txt','customNode','170*34','#1890ff','[{\"name\": \"name\", \"type\": \"input\", \"label\": \"名称\", \"value\": \"KMeans\"}, {\"name\": \"n_clusters\", \"type\": \"inputNumber\", \"label\": \"n_clusters\", \"value\": 8}, {\"name\": \"init\", \"type\": \"input\", \"label\": \"init\", \"value\": \"k-means++\"}, {\"name\": \"n_init\", \"type\": \"inputNumber\", \"label\": \"n_init\", \"value\": 10}, {\"name\": \"max_iter\", \"type\": \"inputNumber\", \"label\": \"max_iter\", \"value\": 300}, {\"name\": \"tol\", \"type\": \"inputNumber\", \"label\": \"tol\", \"value\": 0.0001}, {\"name\": \"precompute_distances\", \"type\": \"input\", \"label\": \"precompute_distances\", \"value\": \"auto\"}, {\"name\": \"verbose\", \"type\": \"inputNumber\", \"label\": \"verbose\", \"value\": 0}, {\"name\": \"random_state\", \"type\": \"input\", \"label\": \"random_state\", \"value\": null}, {\"name\": \"copy_x\", \"type\": \"checkbox\", \"label\": \"copy_x\", \"value\": true}, {\"name\": \"n_jobs\", \"type\": \"input\", \"label\": \"n_jobs\", \"value\": null}, {\"name\": \"algorithm\", \"type\": \"input\", \"label\": \"algorithm\", \"value\": \"auto\"}]','[{\"func\": \"\", \"name\": \"训练数据\", \"type\": \"input\", \"proportion\": 0.5}]',2),(8,'KNeighborsClassifier','KNeighborsClassifier.txt','customNode','170*34','#1890ff','[{\"name\": \"name\", \"type\": \"input\", \"label\": \"名称\", \"value\": \"Knn\"}, {\"name\": \"n_neighbors\", \"type\": \"inputNumber\", \"label\": \"n_neighbors\", \"value\": 5}, {\"name\": \"weights\", \"type\": \"input\", \"label\": \"weights\", \"value\": \"uniform\"}, {\"name\": \"algorithm\", \"type\": \"input\", \"label\": \"algorithm\", \"value\": \"auto\"}, {\"name\": \"leaf_size\", \"type\": \"inputNumber\", \"label\": \"leaf_size\", \"value\": 30}, {\"name\": \"p\", \"type\": \"inputNumber\", \"label\": \"p\", \"value\": 2}, {\"name\": \"metric\", \"type\": \"input\", \"label\": \"metric\", \"value\": \"minkowski\"}, {\"name\": \"metric_params\", \"type\": \"input\", \"label\": \"metric_params\", \"value\": null}, {\"name\": \"n_jobs\", \"type\": \"input\", \"label\": \"n_jobs\", \"value\": null}]','[{\"func\": \"\", \"name\": \"训练数据\", \"type\": \"input\", \"proportion\": 0.5}]',5);
/*!40000 ALTER TABLE `node_template` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `point_detail`
--

DROP TABLE IF EXISTS `point_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `point_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `point_id` varchar(45) DEFAULT NULL,
  `name` text,
  `type` varchar(45) DEFAULT NULL,
  `proportion` float DEFAULT NULL,
  `func` varchar(45) DEFAULT NULL,
  `node_id` int(11) NOT NULL,
  `graph_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_point_detail_node1_idx` (`node_id`,`graph_id`),
  CONSTRAINT `fk_point_detail_node1` FOREIGN KEY (`node_id`, `graph_id`) REFERENCES `node` (`id`, `graph_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `point_detail`
--

LOCK TABLES `point_detail` WRITE;
/*!40000 ALTER TABLE `point_detail` DISABLE KEYS */;
INSERT INTO `point_detail` VALUES (1,'circle5','文件','output',0.5,NULL,1,1),(2,'circle10','文件','input',0.5,NULL,2,1),(3,'circle15','文件','input',0.5,NULL,3,1),(4,'circle17','选择列','output',0.5,NULL,3,1),(5,'circle22','训练数据','input',0.5,NULL,4,1),(6,'circle27','文件','input',0.5,NULL,5,1),(7,'circle5','文件','output',0.5,NULL,6,2),(8,'circle10','文件','input',0.5,NULL,7,2),(9,'circle15','文件','input',0.5,NULL,8,2),(10,'circle17','选择列','output',0.5,NULL,8,2),(11,'circle22','训练数据','input',0.5,NULL,9,2);
/*!40000 ALTER TABLE `point_detail` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-03-31  2:06:58
