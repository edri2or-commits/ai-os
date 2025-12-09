# Get DateTime Tool

**Purpose:** Provide accurate current date/time for Claude to prevent date calculation errors

## Problem Solved

**Before:** Claude guessed dates based on conversation context
- Example: "October 2023 is 13 months ago" ❌ (actually 26 months!)

**After:** Claude calls get_datetime() for exact current time
- Example: "October 2023 is 26 months ago (2025-12-04 minus 2023-10-01)" ✅

---

## Usage

### From Claude Desktop (via Desktop Commander MCP)

```
User: "What's today's date?"

Claude: [calls start_process with get_datetime.py]

Output:
{
  "date": "2025-12-04",
  "time": "03:30:48",
  "day_of_week": "Thursday",
  "unix": 1764811848
}

Response: "היום יום חמישי, 4 בדצמבר 2025, השעה 03:30"
```

### From Command Line

```bash
python tools/get_datetime.py
```

### From Python Script

```python
import subprocess
import json

result = subprocess.run(
    ['python', 'tools/get_datetime.py'],
    capture_output=True,
    text=True
)
data = json.loads(result.stdout)
print(f"Today is {data['date']}")
```

---

## Output Format

```json
{
  "date": "2025-12-04",        // YYYY-MM-DD
  "time": "15:52:30",          // HH:MM:SS (24h)
  "day_of_week": "Thursday",   // English day name
  "timezone": "Local",         // Local Windows timezone
  "iso": "2025-12-04T15:52:30", // ISO 8601 format
  "unix": 1733324730,          // Unix timestamp
  "year": 2025,
  "month": 12,
  "day": 4,
  "hour": 15,
  "minute": 52,
  "second": 30
}
```

---

## Protocol: Date Math

**Rule:** ALWAYS call get_datetime() before calculating date differences

**Example:**

```
User: "How old is research from October 2023?"

❌ WRONG (guessing):
Claude: "About 13 months old"

✅ CORRECT (calculated):
1. [call get_datetime()] → "2025-12-04"
2. [calculate] 2025-12 - 2023-10 = 26 months
3. Response: "המחקר בן 26 חודשים (2 שנים ו-2 חודשים)"
```

---

## Test Cases

### Test 1: Basic Call
```
python tools/get_datetime.py
Expected: JSON output with current date/time ✅
```

### Test 2: Date Math Accuracy
```
Given: Research published "2023-10-01"
Call: get_datetime() → "2025-12-04"
Calculate: (2025-12) - (2023-10) = 26 months
Expected: "26 months old" ✅
```

### Test 3: Day of Week
```
Call: get_datetime()
Check: day_of_week matches system calendar
Expected: Correct day name ✅
```

---

## Implementation Notes

- **No external dependencies:** Uses Python standard library only
- **Fast:** < 1 second execution
- **Cross-platform:** Works on Windows/Linux/Mac
- **JSON output:** Easy to parse

---

## Related Files

- **Script:** `tools/get_datetime.py`
- **Documentation:** This file
- **Usage Example:** See Protocol section above

---

## Changelog

**2025-12-04:** Initial implementation
- Created get_datetime.py
- Solves date calculation errors
- Protocol: Always call before date math

---

**Last Updated:** 2025-12-04 03:30 IST
