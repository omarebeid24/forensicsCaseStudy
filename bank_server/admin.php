<?php
session_start();
require 'db.php';

if ($_SESSION['username'] !== 'admin') {
    echo "Access denied.";
    exit();
}

$result = $conn->query("SELECT * FROM logs ORDER BY id DESC");

echo "<h1>Admin Panel - Logs</h1>";
while ($row = $result->fetch_assoc()) {
    echo "<p>{$row['timestamp']} - {$row['user']} - {$row['action']}</p>";
}
?>
<a href="logout.php">Logout</a>
