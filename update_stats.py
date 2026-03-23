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
    languages = dict()

    for repo in repos:
        stars += repo["stargazers_count"]
        # Retrieve languages and number of bytes
        langs = requests.get(repo["languages_url"]).json()
        for lang, bytes_count in langs.items():
            languages[lang] = languages.get(lang, 0) + bytes_count
            total_bytes += bytes_count
    
    return {
        "repos": repo_count,
        "stars": stars,
        "languages": languages,
        "bytes": total_bytes
    }

def render_language_stats(stats):
    total_bytes = stats["bytes"]
    language_lines = ""
    max_len = max(len(lang) for lang in stats["languages"])
    for lang, bytes_count in stats["languages"].items():
        pct = bytes_count / total_bytes * 100
        bar_length = int(pct / 100 * 20)
        if pct > 0 and bar_length == 0:
            bar_length = 1
        bar = "█" * bar_length
        language_lines += f"{lang.ljust(max_len)}: {bar} {pct:.1f}%<br>"
    return language_lines

#--- Overwrite README.md ---
# Organisation
org_section_text = f"""
### Organisation 
*Includes collaborative projects*
"""
org_stats = fetch_github_stats("org")
# Make languages text
language_lines = render_language_stats(org_stats)
# Make organisation stats text
org_stats_text = f"""
<ul>
    <li>🧩 Repositories: {org_stats["repos"]}</li>
    <li>⭐ Stars: {org_stats["stars"]}</li>
    <li>⚙️ Languages:<br><pre>{language_lines}</pre></li>
    <li>🌱 Total Code Size: {org_stats["bytes"] / 1000:.1f} KB</li>
</ul>
"""
# Personal
user_section_text = f"""
### Personal
"""
user_stats = fetch_github_stats("user")
# Make languages text
language_lines = render_language_stats(user_stats)
# Make user stats text
user_stats_text = f"""
<ul>
    <li>🧩 Repositories: {user_stats["repos"]}</li>
    <li>⭐ Stars: {user_stats["stars"]}</li>
    <li>⚙️ Languages:<br><pre>{language_lines}</pre></li>
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