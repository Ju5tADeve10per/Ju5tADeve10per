import requests

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
<p>
    <h4>- Repositories: {repo_count}</h4>
    <h4>- Stars: {stars}</h4>
    <h4>- Languages: {", ".join(list(languages))}</h4>
    <h4>- Total Code Size: {total_bytes} bytes</h4>
</p>
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