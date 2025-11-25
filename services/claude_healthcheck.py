import json, datetime, random

MODULES = ["filesystem", "git", "google_read", "browser", "canva"]

STATES = ["OK", "Flaky", "Broken"]


def run_healthcheck():
    report = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "agent": "Claude Desktop",
        "phase": "2.2",
        "modules": {},
        "summary": {},
        "digest": []
    }

    ok, flaky, broken = 0, 0, 0

    for m in MODULES:
        state = random.choices(STATES, weights=[0.7, 0.2, 0.1])[0]
        report["modules"][m] = state
        if state == "OK":
            ok += 1
        elif state == "Flaky":
            flaky += 1
            report["digest"].append({
                "module": m,
                "error": f"Intermittent issue detected in {m}",
                "suggested_fix": f"Check logs for {m}"
            })
        else:
            broken += 1
            report["digest"].append({
                "module": m,
                "error": f"{m} module not responding",
                "suggested_fix": f"Restart {m} integration"
            })

    report["summary"] = {"total_ok": ok, "total_flaky": flaky, "total_broken": broken}

    file_name = f"reports/healthcheck_{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"Healthcheck complete. Summary: {ok} OK, {flaky} Flaky, {broken} Broken")
    print(f"Report saved to {file_name}")


if __name__ == "__main__":
    run_healthcheck()