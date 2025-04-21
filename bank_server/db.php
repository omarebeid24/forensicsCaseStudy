<?php
$conn = new mysqli("localhost", "root", "", "bank");
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
