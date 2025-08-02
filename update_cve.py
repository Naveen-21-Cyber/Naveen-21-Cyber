import feedparser
from datetime import datetime

# Fetch CVE RSS feed
feed = feedparser.parse("https://www.cvedetails.com/vulnerability-feed.php")

latest = feed.entries[0]
title = latest.title
link = latest.link
published = latest.published

# Read README
with open("README.md", "r", encoding="utf-8") as file:
    content = file.read()

# Replace placeholder
start = "<!-- START_CVE -->"
end = "<!-- END_CVE -->"
cve_info = f"{title}\n\n[Read more]({link})\n\n_Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}_"
updated = content.split(start)[0] + start + "\n" + cve_info + "\n" + end + content.split(end)[1]

# Write back
with open("README.md", "w", encoding="utf-8") as file:
    file.write(updated)