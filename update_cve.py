import requests
import datetime
import os
from dotenv import load_dotenv

# Load environment variables (for local testing)
load_dotenv()

# Fetch API key from env (GitHub Secret or .env file)
NVD_API_KEY = os.getenv("NVD_API_KEY")

if not NVD_API_KEY:
    raise ValueError("Missing NVD_API_KEY. Please set it as a GitHub Secret or in a .env file.")

# NVD CVE API URL
NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def fetch_latest_cves():
    headers = {
        "apiKey": NVD_API_KEY,
        "User-Agent": "github-action-cve-fetcher"
    }

    # Fetch CVEs published in the last 1 day
    params = {
        "pubStartDate": (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)).isoformat(),
        "resultsPerPage": 5,
        "startIndex": 0,
        "sortBy": "published",
        "sortDir": "desc"
    }

    response = requests.get(NVD_API_URL, params=params, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch CVEs: {response.status_code} {response.text}")

    data = response.json()
    return data.get("vulnerabilities", [])

def format_cve_markdown(cve_list):
    if not cve_list:
        return "### 🔒 Latest CVEs\n\nNo recent CVEs found in the last 24 hours.\n"

    md = "### 🔒 Latest CVEs (last 24h)\n\n"
    for cve_entry in cve_list:
        cve = cve_entry.get("cve", {})
        cve_id = cve.get("id", "Unknown CVE")
        description = cve.get("descriptions", [{}])[0].get("value", "No description available")
        url = f"https://nvd.nist.gov/vuln/detail/{cve_id}"
        md += f"- **[{cve_id}]({url})**: {description}\n"

    return md

def update_readme(cve_markdown):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<!-- START-CVE-SECTION -->"
    end_marker = "<!-- END-CVE-SECTION -->"

    if start_marker in content and end_marker in content:
        start = content.find(start_marker) + len(start_marker)
        end = content.find(end_marker)
        updated = content[:start] + "\n\n" + cve_markdown + "\n" + content[end:]
    else:
        # If markers not found, append
        updated = content + f"\n\n{start_marker}\n\n{cve_markdown}\n\n{end_marker}\n"

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated)

if __name__ == "__main__":
    cve_list = fetch_latest_cves()
    markdown = format_cve_markdown(cve_list)
    update_readme(markdown)
    print("✅ README.md updated with latest CVEs.")
