-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 02, 2024 at 07:55 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ev`
--

-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE `transactions` (
  `vehicleId` varchar(36) NOT NULL,
  `paymentId` varchar(36) NOT NULL,
  `lastBatterySwitch` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transactions`
--

INSERT INTO `transactions` (`vehicleId`, `paymentId`, `lastBatterySwitch`) VALUES
('e78d8e36-83f0-432e-9525-3edc68eeb144', '04354d8f-8b81-4659-8406-76286bfa88cf', '2024-04-02 16:42:40'),
('0c6c303f-242c-4143-82d4-377657030834', '7b6f6b30-c305-4f30-b416-c765164fab62', '2024-04-02 17:29:50'),
('9e580531-0447-4add-9fdd-a22360cf4a1a', '8f61b4f3-8fc8-4db3-a976-b0e553908b07', '2024-04-02 17:42:27');

-- --------------------------------------------------------

--
-- Table structure for table `vehicleinfo`
--

CREATE TABLE `vehicleinfo` (
  `vehicleId` varchar(36) NOT NULL,
  `vehicleName` varchar(20) NOT NULL,
  `ownerName` varchar(20) NOT NULL,
  `purchaseDate` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vehicleinfo`
--

INSERT INTO `vehicleinfo` (`vehicleId`, `vehicleName`, `ownerName`, `purchaseDate`) VALUES
('0c6c303f-242c-4143-82d4-377657030834', 'IN-78', 'Selina Williams', '2024-04-02 12:50:15'),
('490aab1e-e60d-46e6-be22-6a39854dc5f1', 'TY-30', 'Chloe Evrret', '2024-04-02 12:07:11'),
('9e580531-0447-4add-9fdd-a22360cf4a1a', 'WB-9892', 'Bruce Wayne', '2024-04-02 13:18:39'),
('ba89bb05-47bd-4578-895d-c609d58e83f5', 'RTUY-62', 'Charles Brown', '2024-04-02 12:50:35'),
('d62a6348-26c1-4bff-93ee-9bef799c5ef3', 'yui-92', 'Bruce Wayne', '2024-04-02 17:40:07'),
('d8862aed-18e0-460f-b5b1-cc379020be4d', 'XC-300', 'Karl Bennet', '2024-04-02 10:57:01'),
('dc8391fb-efa0-4b5f-ae49-3e27dcd269ad', 'XZ-37', 'Mitchell Johnson', '2024-04-02 13:27:04'),
('e16b2df2-76c9-4ea0-9062-153e5c014542', 'TY-1901', 'Mary Jones', '2024-04-02 12:51:03'),
('e78d8e36-83f0-432e-9525-3edc68eeb144', 'TY-23', 'Petr Johnson', '2024-04-02 12:47:38'),
('eb007a82-be56-4576-ad29-c999b6750794', 'OPY-45', 'Cater Smith', '2024-04-02 12:45:20');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`paymentId`);

--
-- Indexes for table `vehicleinfo`
--
ALTER TABLE `vehicleinfo`
  ADD PRIMARY KEY (`vehicleId`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
