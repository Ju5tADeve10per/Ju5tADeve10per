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


print("repos:", repo_count)
print("stars:", stars)
print("languages:", list(languages))
print("total bytes:", total_bytes)