import requests

# Org
import json
org_name = "Studio-Insplash"
url = f"https://api.github.com/orgs/{org_name}/repos"
repos = requests.get(url).json()

print(json.dumps(repos, indent=2))



# Personal
username = "Ju5tADeve10per"

url = f"https://api.github.com/users/{username}/repos"
repos = requests.get(url).json()

repo_count = len(repos)
stars = 0
total_bytes = 0
languages = set()

for repo in repos:
    stars += repo["stargazers_count"]

    # Retrieve lang data and num of bytes
    langs = requests.get(repo["languages_url"]).json()
    for lang, bytes_count in langs.items():
        languages.add(lang)
        total_bytes += bytes_count


#--- Overwrite README.md ---
stats_text = f"""
<ul>
    <li>🧩 Repositories: {repo_count}</li>
    <li>⭐ Stars: {stars}</li>
    <li>⚙️ Languages: {", ".join(list(languages))}</li>
    <li>🌱 Total Code Size: {total_bytes} bytes</li>
</ul>
"""

# Load README.md
with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

# Process README.md
start_tag = "<!-- STATS_START -->"
end_tag = "<!-- STATS_END -->"

before = content.split(start_tag)[0]
after = content.split(end_tag)[1]

# Build a new content
new_content = (
    before
    + start_tag
    + stats_text
    + end_tag
    + after
)

# Save a new content
with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_content)