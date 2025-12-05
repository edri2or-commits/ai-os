# Check if n8n API key exists
try {
    $response = Invoke-RestMethod -Uri 'http://localhost:5678/api/v1/workflows' -Method Get -ErrorAction Stop
    Write-Host "API works without key - this is unusual!"
} catch {
    $errorMessage = $_.Exception.Message
    if ($errorMessage -like "*X-N8N-API-KEY*") {
        Write-Host "API requires key (normal) - key may exist in UI"
    } else {
        Write-Host "Error: $errorMessage"
    }
}
