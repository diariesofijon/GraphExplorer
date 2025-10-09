#!/usr/bin/env python3
import os
import requests

# Load from environment
TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPO")

if not TOKEN or not REPO:
    raise EnvironmentError("Missing GITHUB_TOKEN or GITHUB_REPO environment variables.")

API_URL = f"https://api.github.com/repos/{REPO}"

# Example: Get repository info
def get_repo_info():
    headers = {"Authorization": f"TOKEN {TOKEN}"}
    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()
    return response.json()

# Example: Create a new issue
def create_issue(title, body=None):
    headers = {"Authorization": f"TOKEN {TOKEN}"}
    data = {"title": title, "body": body or ""}
    response = requests.post(f"{API_URL}/issues", json=data, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    # 1️⃣ Fetch repo info
    info = get_repo_info()
    print(f"Repository: {info['full_name']}")
    print(f"Stars: {info['stargazers_count']}, Forks: {info['forks_count']}")

    # 2️⃣ Create an issue
    issue = create_issue("Test issue from API", "This is a secure test issue created via Python API.")
    print(f"Issue created: {issue['html_url']}")
