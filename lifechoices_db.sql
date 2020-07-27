-- MySQL dump 10.13  Distrib 8.0.19, for Win64 (x86_64)
--
-- Host: localhost    Database: lifechoices_db
-- ------------------------------------------------------
-- Server version	8.0.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `administrators_tbl`
--

DROP TABLE IF EXISTS `administrators_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `administrators_tbl` (
  `admin_id` int unsigned NOT NULL AUTO_INCREMENT,
  `admin_username` int(6) unsigned zerofill NOT NULL,
  `admin_privileges` varchar(45) NOT NULL DEFAULT 'None',
  PRIMARY KEY (`admin_id`),
  UNIQUE KEY `admin_username_UNIQUE` (`admin_username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administrators_tbl`
--

LOCK TABLES `administrators_tbl` WRITE;
/*!40000 ALTER TABLE `administrators_tbl` DISABLE KEYS */;
INSERT INTO `administrators_tbl` VALUES (1,000002,'None'),(2,005675,'None'),(3,089567,'None'),(4,000665,'None');
/*!40000 ALTER TABLE `administrators_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `timelogs_tbl`
--

DROP TABLE IF EXISTS `timelogs_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `timelogs_tbl` (
  `timelogs_id` int NOT NULL AUTO_INCREMENT,
  `timeIn` varchar(8) NOT NULL,
  `username` int(6) unsigned zerofill NOT NULL,
  `day` varchar(10) NOT NULL,
  PRIMARY KEY (`timelogs_id`),
  KEY `username_idx` (`username`),
  CONSTRAINT `username` FOREIGN KEY (`username`) REFERENCES `users_tbl` (`username`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `timelogs_tbl`
--

LOCK TABLES `timelogs_tbl` WRITE;
/*!40000 ALTER TABLE `timelogs_tbl` DISABLE KEYS */;
/*!40000 ALTER TABLE `timelogs_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `timelogsout_tbl`
--

DROP TABLE IF EXISTS `timelogsout_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `timelogsout_tbl` (
  `timelogsOut_id` int NOT NULL AUTO_INCREMENT,
  `timeOut` varchar(8) NOT NULL,
  `timelogs_id` int NOT NULL,
  PRIMARY KEY (`timelogsOut_id`),
  KEY `timelogs_id_idx` (`timelogs_id`),
  CONSTRAINT `timelogs_id` FOREIGN KEY (`timelogs_id`) REFERENCES `timelogs_tbl` (`timelogs_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `timelogsout_tbl`
--

LOCK TABLES `timelogsout_tbl` WRITE;
/*!40000 ALTER TABLE `timelogsout_tbl` DISABLE KEYS */;
/*!40000 ALTER TABLE `timelogsout_tbl` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_tbl`
--

DROP TABLE IF EXISTS `users_tbl`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_tbl` (
  `users_ID` int NOT NULL AUTO_INCREMENT,
  `username` int(6) unsigned zerofill NOT NULL,
  `fname` varchar(20) NOT NULL,
  `fsurname` varchar(20) NOT NULL,
  `date_of_birth` date NOT NULL,
  `address` varchar(45) NOT NULL,
  `role` varchar(10) NOT NULL,
  `access` varchar(20) NOT NULL,
  `holidays` int DEFAULT '0',
  `password` varchar(12) NOT NULL DEFAULT 'password',
  PRIMARY KEY (`users_ID`),
  UNIQUE KEY `username_id_UNIQUE` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5173 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_tbl`
--

LOCK TABLES `users_tbl` WRITE;
/*!40000 ALTER TABLE `users_tbl` DISABLE KEYS */;
INSERT INTO `users_tbl` VALUES (1,000001,'Aaqiel','Behardien','2000-01-22','48 Derby Road Lansdowne','Student','Admin',0,'1234'),(2,000002,'Joshua','Cornelias','1998-04-15','69 Raglan Avenue Crawford','Employee','Admin',2,'1234'),(6,345678,'Haley','Fosch','2020-12-03','21 Ottery Road Ottery','Student','None',2,'1234'),(8,000008,'shade','Dark','2019-02-21','17 Brockhurst Road Keynwyn','Lecturer','None',4,'1234'),(10,000009,'Rufus','Mayhem','2000-01-22','69 Fairview Street Fairways','Student','None',0,'1234');
/*!40000 ALTER TABLE `users_tbl` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-13 17:41:55
