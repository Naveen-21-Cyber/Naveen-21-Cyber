import requests
from datetime import datetime

# Number of CVEs to fetch
NUM_CVES = 5

# CVE API endpoint (you can use CIRCL or another reliable CVE feed)
API_URL = f"https://cve.circl.lu/api/last/{NUM_CVES}"

def fetch_latest_cves():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching CVEs: {e}")
        return []

def generate_markdown(cves):
    if not cves:
        return "# 🔐 Latest CVEs\n\n*No CVE data available at the moment.*"

    markdown = "# 🔐 Latest CVEs\n\n"
    markdown += f"_Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}_\n\n"

    for cve in cves:
        cve_id = cve.get("id", "Unknown CVE")
        summary = cve.get("summary", "No description provided.")
        link = f"https://cve.mitre.org/cgi-bin/cvename.cgi?name={cve_id}"
        markdown += f"### [{cve_id}]({link})\n"
        markdown += f"{summary}\n\n"

    return markdown

def update_readme(markdown):
    try:
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(markdown)
        print("✅ README.md updated successfully.")
    except Exception as e:
        print(f"❌ Failed to write to README.md: {e}")

if __name__ == "__main__":
    latest_cves = fetch_latest_cves()
    markdown = generate_markdown(latest_cves)
    update_readme(markdown)
