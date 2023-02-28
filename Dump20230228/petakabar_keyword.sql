-- MySQL dump 10.13  Distrib 8.0.31, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: petakabar
-- ------------------------------------------------------
-- Server version	8.0.31

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `keyword`
--

DROP TABLE IF EXISTS `keyword`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `keyword` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `nama_keyword` varchar(45) NOT NULL,
  `source` varchar(45) NOT NULL,
  `topik_id` int NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `topik_id_idx` (`topik_id`),
  CONSTRAINT `topik_id` FOREIGN KEY (`topik_id`) REFERENCES `topik` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=289 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `keyword`
--

LOCK TABLES `keyword` WRITE;
/*!40000 ALTER TABLE `keyword` DISABLE KEYS */;
INSERT INTO `keyword` VALUES (1,'tabrakan','kompas',3),(2,'kecelakaan','kompas',3),(3,'tertabrak','kompas',3),(4,'kapal tenggelam','kompas',3),(5,'kapal terbalik','kompas',3),(6,'pesawat jatuh','kompas',3),(7,'tabrakan','tribun',3),(8,'kecelakaan','tribun',3),(9,'tertabrak','tribun',3),(10,'tabrakan','tempo',3),(11,'kecelakaan','tempo',3),(12,'tertabrak','tempo',3),(13,'kapal tenggelam','tempo',3),(14,'kapal terbalik','tempo',3),(15,'pesawat jatuh','tempo',3),(16,'tabrakan','detik',3),(17,'kecelakaan','detik',3),(18,'tertabrak','detik',3),(19,'kapal tenggelam','detik',3),(20,'kapal terbalik','detik',3),(21,'pesawat jatuh','detik',3),(23,'ekonomi','detik',2),(24,'ekonomi ri','detik',2),(25,'ekonomi desa','detik',2),(26,'umkm','detik',2),(27,'krisis ekonomi','detik',2),(28,'pertumbuhan ekonomi','detik',2),(29,'ekspor','detik',2),(30,'impor','detik',2),(31,'ekspor impor','detik',2),(32,'neraca dagang','detik',2),(33,'neraca perdagangan','detik',2),(34,'ekonomi','kompas',2),(35,'ekonomi desa','kompas',2),(36,'umkm','kompas',2),(37,'krisis ekonomi','kompas',2),(38,'pertumbuhan ekonomi','kompas',2),(39,'ekspor','kompas',2),(40,'impor','kompas',2),(41,'ekspor impor','kompas',2),(42,'neraca dagang','kompas',2),(43,'neraca perdagangan','kompas',2),(44,'ekonomi','tempo',2),(45,'ekonomi desa','tempo',2),(46,'umkm','tempo',2),(47,'krisis ekonomi','tempo',2),(48,'pertumbuhan ekonomi','tempo',2),(49,'ekspor','tempo',2),(50,'impor','tempo',2),(51,'ekspor impor','tempo',2),(52,'neraca dagang','tempo',2),(53,'neraca perdagangan','tempo',2),(54,'ekonomi','tribun',2),(55,'umkm','tribun',2),(56,'ekspor','tribun',2),(57,'impor','tribun',2),(58,'ekonomi ri','kompas',2),(59,'ekonomi ri','tempo',2),(60,'sepak bola','detik',6),(61,'bulutangkis','detik',6),(62,'basket','detik',6),(63,'futsal','detik',6),(64,'sepak bola','kompas',6),(65,'bulutangkis','kompas',6),(66,'basket','kompas',6),(67,'futsal','kompas',6),(68,'sepakbola','tempo',6),(69,'bulutangkis','tempo',6),(70,'basket','tempo',6),(71,'futsal','tempo',6),(72,'bulutangkis','tribun',6),(73,'basket','tribun',6),(74,'futsal','tribun',6),(80,'angin kencang','detik',1),(81,'puting beliung','detik',1),(82,'pergerakan tanah','detik',1),(83,'erosi','detik',1),(84,'abrasi','detik',1),(85,'tanah longsor','kompas',1),(86,'gempa bumi','kompas',1),(87,'kebakaran','kompas',1),(88,'banjir','kompas',1),(89,'kekeringan','kompas',1),(90,'angin kencang','kompas',1),(91,'puting beliung','kompas',1),(92,'pergerakan tanah','kompas',1),(93,'erosi','kompas',1),(94,'abrasi','kompas',1),(95,'tanah longsor','tempo',1),(96,'gempa bumi','tempo',1),(97,'kebakaran','tempo',1),(98,'banjir','tempo',1),(99,'kekeringan','tempo',1),(100,'angin kencang','tempo',1),(101,'puting beliung','tempo',1),(102,'pergerakan tanah','tempo',1),(103,'erosi','tempo',1),(104,'abrasi','tempo',1),(105,'longsor','tribun',1),(106,'gempa','tribun',1),(107,'kebakaran','tribun',1),(108,'banjir','tribun',1),(109,'kekeringan','tribun',1),(110,'erosi','tribun',1),(111,'abrasi','tribun',1),(132,'pembunuhan','detik',5),(133,'pencurian','detik',5),(134,'pemerkosaan','detik',5),(135,'perampokan','detik',5),(136,'curanmor','detik',5),(137,'pembunuhan','kompas',5),(138,'pencurian','kompas',5),(139,'pemerkosaan','kompas',5),(140,'perampokan','kompas',5),(141,'curanmor','kompas',5),(142,'pembunuhan','tempo',5),(143,'pencurian','tempo',5),(144,'pemerkosaan','tempo',5),(145,'perampokan','tempo',5),(146,'curanmor','tempo',5),(147,'pembunuhan','tribun',5),(148,'pencurian','tribun',5),(149,'pemerkosaan','tribun',5),(150,'perampokan','tribun',5),(151,'curanmor','tribun',5),(153,'kesehatan','detik',4),(154,'gizi','detik',4),(155,'infeksi','detik',4),(156,'radang','detik',4),(157,'medis','detik',4),(158,'bakteri','detik',4),(159,'paru','detik',4),(160,'hati','detik',4),(161,'ginjal','detik',4),(162,'kulit','detik',4),(163,'radang','detik',4),(164,'simtoma','detik',4),(165,'pneumonia','detik',4),(166,'komplikasi','detik',4),(167,'kelainan','detik',4),(168,'polio','detik',4),(169,'penyakit','detik',4),(170,'virus','detik',4),(171,'tuberkulosis','detik',4),(172,'dbd','detik',4),(173,'kolera','detik',4),(174,'diabetes','detik',4),(175,'corona','detik',4),(176,'covid','detik',4),(177,'bells palsy','detik',4),(178,'kanker','detik',4),(179,'malaria','detik',4),(180,'virus zika','detik',4),(181,'cikungunya','detik',4),(182,'stroke','detik',4),(183,'kesehatan','tempo',4),(184,'gizi','tempo',4),(185,'infeksi','tempo',4),(186,'radang','tempo',4),(187,'medis','tempo',4),(188,'bakteri','tempo',4),(189,'paru','tempo',4),(190,'hati','tempo',4),(191,'ginjal','tempo',4),(192,'kulit','tempo',4),(193,'radang','tempo',4),(194,'simtoma','tempo',4),(195,'pneumonia','tempo',4),(196,'komplikasi','tempo',4),(197,'kelainan','tempo',4),(198,'polio','tempo',4),(199,'penyakit','tempo',4),(200,'virus','tempo',4),(201,'tuberkulosis','tempo',4),(202,'dbd','tempo',4),(203,'kolera','tempo',4),(204,'diabetes','tempo',4),(205,'corona','tempo',4),(206,'covid','tempo',4),(207,'bells palsy','tempo',4),(208,'kanker','tempo',4),(209,'malaria','tempo',4),(210,'virus zika','tempo',4),(211,'cikungunya','tempo',4),(212,'stroke','tempo',4),(213,'kesehatan','kompas',4),(214,'gizi','kompas',4),(215,'infeksi','kompas',4),(216,'radang','kompas',4),(217,'medis','kompas',4),(218,'bakteri','kompas',4),(219,'paru','kompas',4),(220,'hati','kompas',4),(221,'ginjal','kompas',4),(222,'kulit','kompas',4),(223,'radang','kompas',4),(224,'simtoma','kompas',4),(225,'pneumonia','kompas',4),(226,'komplikasi','kompas',4),(227,'kelainan','kompas',4),(228,'polio','kompas',4),(229,'penyakit','kompas',4),(230,'virus','kompas',4),(231,'tuberkulosis','kompas',4),(232,'dbd','kompas',4),(233,'kolera','kompas',4),(234,'diabetes','kompas',4),(235,'corona','kompas',4),(236,'covid','kompas',4),(237,'bells palsy','kompas',4),(238,'kanker','kompas',4),(239,'malaria','kompas',4),(240,'virus zika','kompas',4),(241,'cikungunya','kompas',4),(242,'stroke','kompas',4),(243,'kesehatan','tribun',4),(244,'gizi','tribun',4),(245,'infeksi','tribun',4),(246,'radang','tribun',4),(247,'medis','tribun',4),(248,'bakteri','tribun',4),(249,'paru','tribun',4),(250,'hati','tribun',4),(251,'ginjal','tribun',4),(252,'kulit','tribun',4),(253,'radang','tribun',4),(255,'pneumonia','tribun',4),(256,'komplikasi','tribun',4),(257,'kelainan','tribun',4),(258,'polio','tribun',4),(259,'penyakit','tribun',4),(260,'virus','tribun',4),(261,'tuberkulosis','tribun',4),(262,'dbd','tribun',4),(263,'kolera','tribun',4),(264,'diabetes','tribun',4),(265,'corona','tribun',4),(266,'covid','tribun',4),(268,'kanker','tribun',4),(269,'malaria','tribun',4),(270,'cikungunya','tribun',4),(271,'stroke','tribun',4),(275,'sepakbola','tribun',6),(280,'tanah longsor','detik',1),(281,'gempa bumi','detik',1),(282,'kebakaran','detik',1),(283,'banjir','detik',1),(284,'kekeringan','detik',1);
/*!40000 ALTER TABLE `keyword` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-02-28 18:40:47
