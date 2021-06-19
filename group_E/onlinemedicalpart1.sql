/*!40101 SET NAMES utf8 */;
/*!40014 SET FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/ onlinemedicalpart1 /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE onlinemedicalpart1;

DROP TABLE IF EXISTS userinfo;
CREATE TABLE `userinfo` (
  `uid` varchar(33) NOT NULL,
  `password` varchar(50) NOT NULL,
  `nickname` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `address` varchar(50) NOT NULL,
  `phoneNumber` varchar(20) NOT NULL,
  `emailAddr` varchar(30) NOT NULL,
  `utype` int NOT NULL,
  PRIMARY KEY (`uid`)
);
INSERT INTO userinfo(uid,password,nickname,name,address,phoneNumber,emailAddr,utype) VALUES('33012219870101291X','987654321','test2','管理员','杭州西湖区','86-18893333532','3200101988@zju.edu.cn',1),('33012219970101291X','123456789','test1','用户一号','浙大紫金港','86-18895719532','3200101988@zju.edu.cn',0);