# Judge Agent - Simple Working Version
# This creates a minimal working Judge Agent workflow

$workflow = @{
    name = "Judge Agent v2 - Working"
    nodes = @(
        @{
            parameters = @{
                rule = @{
                    interval = @(
                        @{
                            field = "hours"
                            hoursInterval = 6
                        }
                    )
                }
            }
            name = "Every 6 Hours"
            type = "n8n-nodes-base.scheduleTrigger"
            typeVersion = 1.1
            position = @(240, 300)
            id = "schedule1"
        },
        @{
            parameters = @{
                jsCode = @"
// Test: Just return success
return {
    json: {
        status: "Judge Agent is working!",
        timestamp: new Date().toISOString(),
        message: "If you see this, the workflow executed successfully"
    }
};
"@
            }
            name = "Test Node"
            type = "n8n-nodes-base.code"
            typeVersion = 2
            position = @(440, 300)
            id = "test1"
        }
    )
    connections = @{
        "Every 6 Hours" = @{
            main = @(
                @(
                    @{
                        node = "Test Node"
                        type = "main"
                        index = 0
                    }
                )
            )
        }
    }
    active = $false
}

$json = $workflow | ConvertTo-Json -Depth 10
$json | Set-Content "C:\Users\edri2\Desktop\AI\ai-os\n8n_workflows\judge_test.json" -Encoding UTF8

Write-Host "Created test workflow JSON"
Write-Host "Now importing to n8n..."

# Copy to container
docker cp "C:\Users\edri2\Desktop\AI\ai-os\n8n_workflows\judge_test.json" n8n-production:/tmp/

# Import
docker exec n8n-production sh -c "mkdir -p /tmp/import && cp /tmp/judge_test.json /tmp/import/"
docker exec n8n-production n8n import:workflow --input=/tmp/import

Write-Host "Test workflow imported. Check n8n UI to see if it appears."
