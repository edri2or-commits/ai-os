"""
Get Current DateTime Tool
Returns current system date and time in structured format

Usage:
    python tools/get_datetime.py

Output (JSON):
    {
        "date": "2025-12-04",
        "time": "15:52:30",
        "day_of_week": "Thursday",
        "timezone": "IST",
        "iso": "2025-12-04T15:52:30+02:00",
        "unix": 1733324730
    }
"""

import json
from datetime import datetime
import sys

def get_current_datetime():
    """Get current datetime in multiple formats"""
    try:
        # Windows doesn't have pytz by default, use basic datetime
        now = datetime.now()
        
        result = {
            'date': now.strftime('%Y-%m-%d'),
            'time': now.strftime('%H:%M:%S'),
            'day_of_week': now.strftime('%A'),
            'timezone': 'Local',  # Windows local time
            'iso': now.isoformat(),
            'unix': int(now.timestamp()),
            'year': now.year,
            'month': now.month,
            'day': now.day,
            'hour': now.hour,
            'minute': now.minute,
            'second': now.second
        }
        
        return result
        
    except Exception as e:
        return {
            'error': str(e),
            'status': 'failed'
        }

if __name__ == '__main__':
    result = get_current_datetime()
    print(json.dumps(result, indent=2))
