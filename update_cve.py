import requests
from datetime import datetime

# Step 1: Get latest CVEs
url = "https://cve.circl.lu/api/last"
response = requests.get(url)
cves = response.json()

# Step 2: Format output
latest_cves = ""
for cve in cves[:5]:
    latest_cves += f"- [{cve['id']}]({cve['references'][0] if cve['references'] else '#'}) — {cve['summary'][:100]}...\n"

# Step 3: Update README.md
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

start_tag = "<!-- CVE-START -->"
end_tag = "<!-- CVE-END -->"

new_section = f"{start_tag}\n### 🔥 Latest CVEs (Updated {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')})\n\n{latest_cves}{end_tag}"
if start_tag in content and end_tag in content:
    new_content = content.split(start_tag)[0] + new_section + content.split(end_tag)[1]
else:
    new_content = content + "\n\n" + new_section

# Only update if something changed
if content != new_content:
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)

