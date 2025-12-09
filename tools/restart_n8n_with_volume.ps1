# Restart n8n with workspace volume
Write-Host "Stopping old containers..." -ForegroundColor Yellow
docker stop n8n-production qdrant-production

Write-Host "Removing old containers..." -ForegroundColor Yellow  
docker rm n8n-production qdrant-production

Write-Host "Starting with docker-compose..." -ForegroundColor Cyan
cd C:\Users\edri2\Desktop\AI\ai-os
docker-compose up -d

Write-Host "Waiting for n8n to be ready..." -ForegroundColor Gray
Start-Sleep -Seconds 5

Write-Host "Checking status..." -ForegroundColor Cyan
docker ps --filter "name=n8n-production"

Write-Host "`nDone! Check: http://localhost:5678" -ForegroundColor Green
