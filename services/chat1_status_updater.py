import json, datetime, os

CONTROL_PLANE_PATH = os.getenv("CONTROL_PLANE_PATH", "docs/CONTROL_PLANE_SPEC.md")
TIMELINE_PATH = "EVENT_TIMELINE.jsonl"


def update_chat1_status(status: str, details: str = None):
    """Update chat1_status field in CONTROL_PLANE_SPEC.md and log event to timeline."""
    with open(CONTROL_PLANE_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if 'chat1_status' in line and '|' in line:
            parts = line.split('|')
            parts[-2] = f' {status} '
            new_lines.append('|'.join(parts))
        else:
            new_lines.append(line)

    with open(CONTROL_PLANE_PATH, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    # Log to timeline
    event = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "actor": "Chat1",
        "action": "Status Update",
        "status": status,
        "details": details or "",
        "phase": "2.3"
    }
    with open(TIMELINE_PATH, 'a', encoding='utf-8') as f:
        f.write(json.dumps(event) + "\n")

    print(f"Chat1 status updated to {status} and logged to {TIMELINE_PATH}.")


if __name__ == '__main__':
    update_chat1_status("OK", "Chat1 responding normally.")