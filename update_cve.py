import requests
import datetime
import os
import subprocess

def fetch_latest_cves():
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    params = {
        "resultsPerPage": 5,
        "pubStartDate": (datetime.datetime.utcnow() - datetime.timedelta(days=1)).isoformat() + "Z"
    }

    headers = {
        "User-Agent": "github-action-cve-fetcher"
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch CVEs: {response.status_code} {response.text}")

    data = response.json()
    cves = []

    for item in data.get("vulnerabilities", []):
        cve_id = item["cve"]["id"]
        description = item["cve"]["descriptions"][0]["value"]
        cves.append(f"- **{cve_id}**: {description[:180]}...")

    return cves

def update_readme(cves):
    with open("README.md", "r", encoding="utf-8") as file:
        content = file.readlines()

    start_marker = "<!-- CVE-START -->"
    end_marker = "<!-- CVE-END -->"

    try:
        start_index = content.index(start_marker + "\n") + 1
        end_index = content.index(end_marker + "\n")
    except ValueError:
        print("CVE markers not found in README.md")
        return

    # Build new CVE section
    new_cve_section = [f"{line}\n" for line in cves]

    # Update content
    updated_content = content[:start_index] + new_cve_section + content[end_index:]

    with open("README.md", "w", encoding="utf-8") as file:
        file.writelines(updated_content)

def commit_and_push():
    subprocess.run(["git", "config", "--global", "user.email", "github-actions[bot]@users.noreply.github.com"], check=True)
    subprocess.run(["git", "config", "--global", "user.name", "github-actions[bot]"], check=True)
    subprocess.run(["git", "add", "README.md"], check=True)
    subprocess.run(["git", "commit", "-m", "🛡️ Update README with latest CVEs"], check=True)
    subprocess.run(["git", "push"], check=True)

if __name__ == "__main__":
    cve_list = fetch_latest_cves()
    update_readme(cve_list)
    commit_and_push()
