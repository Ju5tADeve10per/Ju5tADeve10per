import requests

def fetch_github_stats(account_type):
    if account_type == "org":
        org_name = "Studio-Insplash"
        url = f"https://api.github.com/orgs/{org_name}/repos"
    elif account_type == "user":
        username = "Ju5tADeve10per"
        url = f"https://api.github.com/users/{username}/repos"
    else:
        raise ValueError("invalid account_type")

    repos = requests.get(url).json()
    repo_count = len(repos)
    stars = 0
    total_bytes = 0
    languages = set()

    for repo in repos:
        stars += repo["stargazers_count"]
        # Retrieve languages and number of bytes
        langs = requests.get(repo["languages_url"]).json()
        for lang, bytes_count in langs.items():
            languages.add(lang)
            total_bytes += bytes_count
    
    return {
        "repos": repo_count,
        "stars": stars,
        "languages": languages,
        "bytes": total_bytes
    }


#--- Overwrite README.md ---
# Organisation
org_section_text = f"""
### Organisation <sub>(Includes collaborative projects)</sub>
"""
org_stats = fetch_github_stats("org")
org_stats_text = f"""
<ul>
    <li>🧩 Repositories: {org_stats["repos"]}</li>
    <li>⭐ Stars: {org_stats["stars"]}</li>
    <li>⚙️ Languages: {", ".join(sorted(org_stats["languages"]))}</li>
    <li>🌱 Total Code Size: {org_stats["bytes"] / 1000:.1f} KB</li>
</ul>
"""
# Personal
user_section_text = f"""
### Personal
"""
user_stats = fetch_github_stats("user")
user_stats_text = f"""
<ul>
    <li>🧩 Repositories: {user_stats["repos"]}</li>
    <li>⭐ Stars: {user_stats["stars"]}</li>
    <li>⚙️ Languages: {", ".join(sorted(user_stats["languages"]))}</li>
    <li>🌱 Total Code Size: {user_stats["bytes"] / 1000:.1f} KB</li>
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
    + org_section_text
    + org_stats_text
    + user_section_text
    + user_stats_text
    + end_tag
    + after
)

# Save a new content
with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_content)