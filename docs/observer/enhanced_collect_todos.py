#!/usr/bin/env python3
"""
enhanced_collect_todos.py
Collect TODO/FIXME comments from all Python files in git history,
group by module, generate Markdown, and optionally create GitHub issues.
"""

import subprocess
import re
import requests
import argparse
import os

import github_keys

# --- Configuration ---
GITHUB_TOKEN = github_keys.TOKEN
GITHUB_REPO = github_keys.REPO
CREATE_ISSUES = False # Set True to create GitHub issues if you use manually
GITHUB_BASE_URL = f"https://github.com/{GITHUB_REPO}/develop"

# --- Regex ---
TODO_PATTERN = re.compile(r"#\s*(TODO|FIXME):?\s*(.*)")

# --- Functions ---
def get_all_commits():
    """Return all commit hashes, oldest first."""
    commits = subprocess.check_output(
        ["git", "log", "--pretty=format:%H", "--reverse"],
        text=True
    ).splitlines()
    return commits

def get_python_files_from_commit(commit_hash):
    """Return a list of Python files in a commit."""
    files = subprocess.check_output(
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit_hash],
        text=True
    ).splitlines()
    py_files = [f for f in files if f.endswith(".py")]
    return py_files

def extract_todos_from_file(commit_hash, file_path):
    """Extract TODOs from a single Python file in a given commit."""
    todos = []
    try:
        content = subprocess.check_output(
            ["git", "show", f"{commit_hash}:{file_path}"],
            text=True, errors='ignore'
        ).splitlines()
    except subprocess.CalledProcessError:
        return todos

    for i, line in enumerate(content, 1):
        match = TODO_PATTERN.search(line)
        if match:
            todos.append({
                "commit": commit_hash,
                "file": file_path,
                "line": i,
                "type": match.group(1),
                "text": match.group(2).strip()
            })
    return todos

def write_markdown_grouped(todos, filename="TODOs.md"):
    """Write TODOs grouped by file to Markdown."""
    grouped = {}
    for todo in todos:
        grouped.setdefault(todo['file'], []).append(todo)

    with open(filename, "w") as f:
        f.write("# Project TODOs Collected from Git History\n\n")
        for file, items in grouped.items():
            f.write(f"## `{file}`\n\n")
            for t in items:
                url = f"{GITHUB_BASE_URL}/{t['commit']}/{file}#L{t['line']}"
                f.write(f"- [{t['type']}] `{t['text']}` ([link]({url}))\n")
            f.write("\n")
    print(f"[+] Markdown file generated: {filename}")

def create_github_issue(todo):
    """Create a GitHub issue for a single TODO."""
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {
        "title": f"[{todo['type']}] {todo['text'][:50]}",
        "body": f"{todo['text']}\n\nFound in `{todo['file']}` at line {todo['line']} (commit `{todo['commit']}`)\n\n[View code]({GITHUB_BASE_URL}/{todo['commit']}/{todo['file']}#L{todo['line']})",
        "labels": [todo['type']]
    }
    response = requests.post(f"https://api.github.com/repos/{GITHUB_REPO}/issues", json=data, headers=headers)
    if response.status_code == 201:
        print(f"[+] Issue created: {response.json()['html_url']}")
    else:
        print(f"[!] Failed to create issue: {response.json()}")

# --- Main ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect TODOs/FIXMEs from all Python files in git history")
    parser.add_argument("--issues", action="store_true", help="Push TODOs as GitHub issues")
    parser.add_argument("--output", default="TODOs.md", help="Markdown output file")
    args = parser.parse_args()

    CREATE_ISSUES = args.issues
    output_file = args.output

    print("[*] Collecting all commits...")
    commits = get_all_commits()
    all_todos = []

    for commit in commits:
        py_files = get_python_files_from_commit(commit)
        for file_path in py_files:
            todos = extract_todos_from_file(commit, file_path)
            all_todos.extend(todos)

    if not all_todos:
        print("[*] No TODOs found in git history.")
    else:
        write_markdown_grouped(all_todos, output_file)

        if CREATE_ISSUES:
            print("[*] Creating GitHub issues...")
            for todo in all_todos:
                create_github_issue(todo)
