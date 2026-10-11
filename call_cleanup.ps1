# Script to call the cleanup endpoint on production

Write-Output "🔑 Logging in as super admin..."
$loginBody = @{
    email = "admin@smartbursary.com"
    password = "ChangeMe123!"
} | ConvertTo-Json

try {
    $loginResponse = Invoke-WebRequest -Uri "https://smartbursary-backend.onrender.com/api/auth/login" -Method POST -Body $loginBody -ContentType "application/json" -UseBasicParsing
    $loginData = $loginResponse.Content | ConvertFrom-Json
    $token = $loginData.access_token
    Write-Output "✅ Login successful!"
    
    Write-Output "`n🧹 Cleaning up database..."
    $cleanupResponse = Invoke-WebRequest -Uri "https://smartbursary-backend.onrender.com/api/admin/cleanup-database" -Method POST -Headers @{Authorization="Bearer $token"} -UseBasicParsing
    
    Write-Output "✅ Cleanup response:"
    $cleanupResponse.Content | ConvertFrom-Json | ConvertTo-Json -Depth 5
    
} catch {
    Write-Output "❌ Error: $($_.Exception.Message)"
}
