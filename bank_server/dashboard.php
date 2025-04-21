<?php
session_start();
require 'db.php';

if (!isset($_SESSION['username'])) {
    header("Location: index.php");
    exit();
}

$user = $_SESSION['username'];
$result = $conn->query("SELECT balance FROM users WHERE username='$user'");
$row = $result->fetch_assoc();
echo "<h1>Welcome $user</h1>";
echo "<p>Balance: $" . $row['balance'] . "</p>";
?>

<a href="transfer.php">Transfer Funds</a> | <a href="logout.php">Logout</a>
