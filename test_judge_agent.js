const fs = require('fs');
const https = require('https');

async function runJudgeAgent() {
  // Step 1: Read events
  const timelineFile = '/workspace/truth-layer/timeline/EVENT_TIMELINE.jsonl';
  const sixHoursAgo = new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString();

  let events = [];
  const lines = fs.readFileSync(timelineFile, 'utf-8').split('\n');
  for (const line of lines) {
    if (!line.trim()) continue;
    try {
      const event = JSON.parse(line);
      if (event.ts_utc >= sixHoursAgo) {
        events.push(event);
      }
    } catch (e) {}
  }

  console.log('✅ Step 1: Found', events.length, 'events in last 6 hours');

  // Step 2: Load judge prompt
  const promptFile = '/workspace/prompts/judge_agent_prompt.md';
  const judgePrompt = fs.readFileSync(promptFile, 'utf-8');
  console.log('✅ Step 2: Loaded judge prompt (' + judgePrompt.length + ' chars)');

  // Step 3: Build full prompt
  const fullPrompt = judgePrompt + '\n\n---\n\n## Events to Analyze\n\n```json\n' + JSON.stringify(events, null, 2) + '\n```\n\nPlease analyze these events and return your FauxPas_Report in JSON format.';
  console.log('✅ Step 3: Built full prompt (' + fullPrompt.length + ' chars)');

  // Step 4: Call GPT-4o
  const apiKey = process.env.OPENAI_API_KEY;
  console.log('✅ Step 4: API Key available:', apiKey ? 'YES (' + apiKey.substring(0, 20) + '...)' : 'NO');

  return new Promise((resolve, reject) => {
    const payload = JSON.stringify({
      model: 'gpt-4o',
      messages: [{ role: 'user', content: fullPrompt }],
      temperature: 0.2,
      response_format: { type: 'json_object' }
    });

    const options = {
      hostname: 'api.openai.com',
      port: 443,
      path: '/v1/chat/completions',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
        'Content-Length': payload.length
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          const response = JSON.parse(data);
          if (response.choices && response.choices[0]) {
            const report = JSON.parse(response.choices[0].message.content);
            console.log('✅ Step 5: GPT-4o responded successfully');
            console.log('📊 Report Summary:', report.summary || 'No summary');
            console.log('🔍 FauxPas detected:', report.faux_pas_detected ? report.faux_pas_detected.length : 0);
            
            // Step 6: Write report
            const now = new Date();
            const timestamp = now.toISOString().replace(/:/g, '-').split('.')[0];
            const reportFile = `/workspace/truth-layer/drift/faux_pas/FP-${timestamp}.json`;
            fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));
            console.log('✅ Step 6: Report written to', reportFile);
            console.log('\n🎉 SUCCESS - Judge Agent pipeline completed!');
            resolve(reportFile);
          } else {
            console.error('❌ Unexpected response:', JSON.stringify(response));
            reject(new Error('Unexpected response format'));
          }
        } catch (e) {
          console.error('❌ Parse error:', e.message);
          console.error('Response:', data);
          reject(e);
        }
      });
    });

    req.on('error', (e) => {
      console.error('❌ Request error:', e.message);
      reject(e);
    });

    req.write(payload);
    req.end();
  });
}

runJudgeAgent()
  .then(() => process.exit(0))
  .catch((err) => {
    console.error('❌ Pipeline failed:', err);
    process.exit(1);
  });
