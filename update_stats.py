import requests

username = "Ju5tADeve10per"

url = f"https://api.github.com/users/{username}/repos"
repos = requests.get(url).json()

repo_count = len(repos)

stars = 0
languages = set()

for repo in repos:
    stars += repo["stargazers_count"]

    if repo["language"]:
        languages.add(repo["language"])

print("repos:", repo_count)
print("stars:", stars)
print("languages:", " ".join(list(languages)))