# SmartBursary Development Tunnel
# This creates a shareable link for your local development server

Write-Host "🚀 Starting SmartBursary Development Tunnel..." -ForegroundColor Green
Write-Host ""
Write-Host "📋 Your local server should be running on http://localhost:5174" -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠️  IMPORTANT: You need to download cloudflared first!" -ForegroundColor Red
Write-Host "   Download from: https://github.com/cloudflare/cloudflared/releases/latest" -ForegroundColor Cyan
Write-Host "   Download: cloudflared-windows-amd64.exe" -ForegroundColor Cyan
Write-Host "   Rename it to: cloudflared.exe" -ForegroundColor Cyan
Write-Host "   Place it in: C:\Windows\System32 or this folder" -ForegroundColor Cyan
Write-Host ""
Write-Host "Once cloudflared is installed, run:" -ForegroundColor Yellow
Write-Host "   cloudflared tunnel --url http://localhost:5174" -ForegroundColor Green
Write-Host ""
Write-Host "This will give you a public URL like: https://xxxx.trycloudflare.com" -ForegroundColor Magenta
Write-Host ""
Write-Host "Or use ngrok instead:" -ForegroundColor Yellow
Write-Host "   Download from: https://ngrok.com/download" -ForegroundColor Cyan
Write-Host "   Then run: ngrok http 5174" -ForegroundColor Green
Write-Host ""

# Check if cloudflared exists locally
if (Test-Path ".\cloudflared.exe") {
    Write-Host "✅ Found cloudflared.exe locally!" -ForegroundColor Green
    Write-Host "Starting tunnel..." -ForegroundColor Green
    .\cloudflared.exe tunnel --url http://localhost:5174
} elseif (Get-Command cloudflared -ErrorAction SilentlyContinue) {
    Write-Host "✅ Found cloudflared in PATH!" -ForegroundColor Green
    Write-Host "Starting tunnel..." -ForegroundColor Green
    cloudflared tunnel --url http://localhost:5174
} else {
    Write-Host "❌ cloudflared not found. Please download it first." -ForegroundColor Red
}
