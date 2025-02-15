import requests
from datetime import datetime
import argparse

def get_user_contributions(username, repo_owner, repo_name):
    """
    Fetch contributions of a specific user to a public GitHub repository.

    Args:
        username (str): GitHub username of the contributor
        repo_owner (str): Owner of the repository
        repo_name (str): Name of the repository

    Returns:
        list: List of contribution dictionaries containing commit info
    """
    # GitHub API endpoint
    base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"

    # Headers for GitHub API
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }

    contributions = []

    try:
        # Get commits by the user
        commits_url = f"{base_url}/commits"
        params = {"author": username}
        response = requests.get(commits_url, headers=headers, params=params)
        response.raise_for_status()

        commits = response.json()

        # Get pull requests by the user
        pulls_url = f"{base_url}/pulls"
        params = {"state": "all", "creator": username}
        response = requests.get(pulls_url, headers=headers, params=params)
        response.raise_for_status()

        pull_requests = response.json()

        # Process commits
        for commit in commits:
            commit_data = {
                "type": "commit",
                "sha": commit["sha"][:7],
                "message": commit["commit"]["message"].split("\n")[0],
                "date": datetime.strptime(
                    commit["commit"]["author"]["date"],
                    "%Y-%m-%dT%H:%M:%SZ"
                ).strftime("%Y-%m-%d %H:%M:%S"),
                "url": commit["html_url"]
            }
            contributions.append(commit_data)

        # Process pull requests
        for pr in pull_requests:
            pr_data = {
                "type": "pull_request",
                "number": f"#{pr['number']}",
                "title": pr["title"],
                "state": pr["state"],
                "date": datetime.strptime(
                    pr["created_at"],
                    "%Y-%m-%dT%H:%M:%SZ"
                ).strftime("%Y-%m-%d %H:%M:%S"),
                "url": pr["html_url"]
            }
            contributions.append(pr_data)

        # Sort contributions by date
        contributions.sort(key=lambda x: x["date"], reverse=True)

        return contributions

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from GitHub: {e}")
        return []

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="List a user's contributions to a GitHub repository"
    )
    parser.add_argument("username", help="GitHub username of the contributor")
    parser.add_argument("repo_owner", help="Owner of the repository")
    parser.add_argument("repo_name", help="Name of the repository")

    args = parser.parse_args()

    # Get contributions
    contributions = get_user_contributions(
        args.username,
        args.repo_owner,
        args.repo_name
    )

    # username = "octocat"  # Replace with the actual username
    # repo_owner = "microsoft"    # Replace with the repository owner
    # repo_name = "vscode"      # Replace with the repository name

    # Get contributions
    # contributions = get_user_contributions(username, repo_owner, repo_name)


    # Print contributions
    if contributions:
        # print(f"\nContributions by {args.username} to {args.repo_owner}/{args.repo_name}:")
        print("-" * 80)

        for contribution in contributions:
            if contribution["type"] == "commit":
                print(f"\nCommit {contribution['sha']}")
                print(f"Date: {contribution['date']}")
                print(f"Message: {contribution['message']}")
                print(f"URL: {contribution['url']}")
            else:
                print(f"\nPull Request {contribution['number']}")
                print(f"Date: {contribution['date']}")
                print(f"Title: {contribution['title']}")
                print(f"State: {contribution['state']}")
                print(f"URL: {contribution['url']}")
    else:
        print(f"\nNo contributions found for {args.username} in {args.repo_owner}/{args.repo_name}")

if __name__ == "__main__":
    main()