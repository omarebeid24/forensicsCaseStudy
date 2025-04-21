<?php
session_start();
require 'db.php';

if (!isset($_SESSION['username'])) {
    header("Location: index.php");
    exit();
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $to = $_POST['to'];
    $amount = floatval($_POST['amount']);
    $from = $_SESSION['username'];

    $conn->query("UPDATE users SET balance = balance - $amount WHERE username = '$from'");
    $conn->query("UPDATE users SET balance = balance + $amount WHERE username = '$to'");
    $conn->query("INSERT INTO transactions (sender, receiver, amount) VALUES ('$from', '$to', $amount)");
    $conn->query("INSERT INTO logs (user, action) VALUES ('$from', 'Transferred $$amount to $to')");
    echo "Transfer complete.";
}
?>

<form method="post">
    Transfer to: <input name="to"><br>
    Amount: <input name="amount"><br>
    <button type="submit">Send</button>
</form>
