-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: mydb
-- ------------------------------------------------------
-- Server version	8.0.36

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
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `id` int NOT NULL,
  `fname` varchar(45) NOT NULL,
  `Lastname` varchar(45) NOT NULL,
  `contact` varchar(45) NOT NULL,
  `Location` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (1,'test 1 fname','test 1 Lastname','test 1 contact','test 1 Location'),(2,'test 2 fname','test 2 Lastname','test 2 contact','test 2 Location'),(3,'test 3 fname','test 3 Lastname','test 3 contact','test 3 Location'),(4,'test 4 fname','test 4 Lastname','test 4 contact','test 4 Location'),(5,'test 5 fname','test 5 Lastname','test 5 contact','test 5 Location'),(6,'test 6 fname','test 6 Lastname','test 6 contact','test 6 Location'),(7,'test 7 fname','test 7 Lastname','test 7 contact','test 7 Location'),(8,'test 8 fname','test 8 Lastname','test 8 contact','test 8 Location'),(9,'test 9 fname','test 9 Lastname','test 9 contact','test 9 Location'),(10,'test 10 fname','test 10 Lastname','test 10 contact','test 10 Location'),(11,'test 11 fname','test 11 Lastname','test 11 contact','test 11 Location'),(12,'test 12 fname','test 12 Lastname','test 12 contact','test 12 Location'),(13,'test 13 fname','test 13 Lastname','test 13 contact','test 13 Location'),(14,'test 14 fname','test 14 Lastname','test 14 contact','test 14 Location'),(15,'test 15 fname','test 15 Lastname','test 15 contact','test 15 Location'),(16,'test 16 fname','test 16 Lastname','test 16 contact','test 16 Location'),(17,'test 17 fname','test 17 Lastname','test 17 contact','test 17 Location'),(18,'test 18 fname','test 18 Lastname','test 18 contact','test 18 Location'),(19,'test 19 fname','test 19 Lastname','test 19 contact','test 19 Location'),(20,'test 20 fname','test 20 Lastname','test 20 contact','test 20 Location'),(21,'test 21 fname','test 21 Lastname','test 21 contact','test 21 Location'),(22,'test 22 fname','test 22 Lastname','test 22 contact','test 22 Location'),(23,'test 23 fname','test 23 Lastname','test 23 contact','test 23 Location'),(24,'test 24 fname','test 24 Lastname','test 24 contact','test 24 Location'),(25,'test 25 fname','test 25 Lastname','test 25 contact','test 25 Location');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `experiences`
--

DROP TABLE IF EXISTS `experiences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `experiences` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` varchar(45) NOT NULL,
  `product_id` int NOT NULL,
  `customer_id` int NOT NULL,
  `experience` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `experiences`
--

LOCK TABLES `experiences` WRITE;
/*!40000 ALTER TABLE `experiences` DISABLE KEYS */;
INSERT INTO `experiences` VALUES (1,'test 1 date',1,1,'test 1 experience'),(2,'test 2 date',2,2,'test 2 experience'),(3,'test 3 date',2,2,'test 3 experience'),(4,'test 4 date',4,4,'test 4 experience'),(5,'test 5 date',5,5,'test 5 experience'),(6,'test 6 date',6,6,'test 6 experience'),(7,'test 7 date',7,7,'test 7 experience'),(8,'test 8 date',8,8,'test 8 experience'),(9,'test 9 date',9,9,'test 9 experience'),(10,'test 10 date',10,10,'test 10 experience'),(11,'test 11 date',11,11,'test 11 experience'),(12,'test 12 date',12,12,'test 12 experience'),(13,'test 13 date',13,13,'test 13 experience'),(14,'test 14 date',14,14,'test 14 experience'),(15,'test 15 date',15,15,'test 15 experience'),(16,'test 16 date',16,16,'test 16 experience'),(17,'test 17 date',17,17,'test 17 experience'),(18,'test 18 date',18,18,'test 18 experience'),(19,'test 19 date',19,19,'test 19 experience'),(20,'test 20 date',20,20,'test 20 experience'),(21,'test 21 date',21,21,'test 21 experience'),(22,'test 22 date',22,22,'test 22 experience'),(23,'test 23 date',23,23,'test 23 experience'),(24,'test 24 date',24,24,'test 24 experience'),(25,'test 25 date',25,25,'test 25 experience');
/*!40000 ALTER TABLE `experiences` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `id` int NOT NULL,
  `name` varchar(45) NOT NULL,
  `c_method` varchar(45) NOT NULL,
  `c_type` varchar(45) NOT NULL,
  `pest` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,'test 1 name','test 1 c_method','test 1 c_type','test 1 pest'),(2,'test 2 name','test 2 c_method','test 2 c_type','test 2 pest'),(3,'test 3 name','test 3 c_method','test 3 c_type','test 3 pest'),(4,'test 4 name','test 4 c_method','test 4 c_type','test 4 pest'),(5,'test 5 name','test 5 c_method','test 5 c_type','test 5 pest'),(6,'test 6 name','test 6 c_method','test 6 c_type','test 6 pest'),(7,'test 7 name','test 7 c_method','test 7 c_type','test 7 pest'),(8,'test 8 name','test 8 c_method','test 8 c_type','test 8 pest'),(9,'test 9 name','test 9 c_method','test 9 c_type','test 9 pest'),(10,'test 10 name','test 10 c_method','test 10 c_type','test 10 pest'),(11,'test 11 name','test 11 c_method','test 11 c_type','test 11 pest'),(12,'test 12 name','test 12 c_method','test 12 c_type','test 12 pest'),(13,'test 13 name','test 13 c_method','test 13 c_type','test 13 pest'),(14,'test 14 name','test 14 c_method','test 14 c_type','test 14 pest'),(15,'test 15 name','test 15 c_method','test 15 c_type','test 15 pest'),(16,'test 16 name','test 16 c_method','test 16 c_type','test 16 pest'),(17,'test 17 name','test 17 c_method','test 17 c_type','test 17 pest'),(18,'test 18 name','test 18 c_method','test 18 c_type','test 18 pest'),(19,'test 19 name','test 19 c_method','test 19 c_type','test 19 pest'),(20,'test 20 name','test 20 c_method','test 20 c_type','test 20 pest'),(21,'test 21 name','test 21 c_method','test 21 c_type','test 21 pest'),(22,'test 22 name','test 22 c_method','test 22 c_type','test 22 pest'),(23,'test 23 name','test 23 c_method','test 23 c_type','test 23 pest'),(24,'test 24 name','test 24 c_method','test 24 c_type','test 24 pest'),(25,'test 25 name','test 25 c_method','test 25 c_type','test 25 pest');
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchase`
--

DROP TABLE IF EXISTS `purchase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchase` (
  `id` int NOT NULL,
  `date` varchar(45) NOT NULL,
  `product_id` int NOT NULL,
  `customer_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_purchase_product_idx` (`product_id`),
  KEY `fk_purchase_customer1_idx` (`customer_id`),
  CONSTRAINT `fk_purchase_customer1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`),
  CONSTRAINT `fk_purchase_product` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchase`
--

LOCK TABLES `purchase` WRITE;
/*!40000 ALTER TABLE `purchase` DISABLE KEYS */;
INSERT INTO `purchase` VALUES (1,'test 2 date',2,2),(2,'test 2 date',2,2),(3,'test 3 date',3,3),(4,'test 4 date',4,4),(5,'test 5 date',5,5),(6,'test 6 date',6,6),(7,'test 7 date',7,7),(8,'test 8 date',8,8),(9,'test 9 date',9,9),(10,'test 10 date',10,10),(11,'test 11 date',11,11),(12,'test 12 date',12,12),(13,'test 13 date',13,13),(14,'test 14 date',14,14),(15,'test 15 date',15,15),(16,'test 16 date',16,16),(17,'test 17 date',17,17),(18,'test 18 date',18,18),(19,'test 19 date',19,19),(20,'test 20 date',20,20),(21,'test 21 date',21,21),(22,'test 22 date',22,22),(23,'test 23 date',23,23),(24,'test 24 date',24,24),(25,'test 25 date',25,25);
/*!40000 ALTER TABLE `purchase` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-18 13:44:14
