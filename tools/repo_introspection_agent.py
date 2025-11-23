
import os, json, requests
OUTPUT_FILE = "docs/REPO_SNAPSHOT.json"
OWNER, REPO = "edri2or-commits", "ai-os"
GITHUB_TOKEN = os.getenv("GPT_FULL_ACCESS_TOKEN")
API_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/contents"
def get_repo_contents(path=""):
    url = f"{API_URL}/{path}" if path else API_URL
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    r = requests.get(url, headers=headers); r.raise_for_status()
    items = r.json(); files = []
    for i in items:
        if i["type"]=="dir": files.extend(get_repo_contents(i["path"]))
        elif i["type"]=="file":
            fr = requests.get(i["download_url"], headers=headers)
            if fr.status_code==200:
                files.append({"path": i["path"], "size": i["size"], "content": fr.text})
    return files
def main():
    print("🚀 Scanning repo..."); files = get_repo_contents()
    print(f"✅ Found {len(files)} files. Saving snapshot...")
    os.makedirs("docs", exist_ok=True)
    with open(OUTPUT_FILE,"w",encoding="utf-8") as f: json.dump(files, f, indent=2, ensure_ascii=False)
    print("📄 Snapshot saved at", OUTPUT_FILE)
if __name__=="__main__": main()
