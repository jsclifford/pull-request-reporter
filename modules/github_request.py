import os
from pprint import pprint
from github import Github
import datetime


def init_github():
    gh = Github(os.environ.get('GITHUB_ACCESS_TOKEN'))
    return gh


def get_pull_request(gh, repo: str, previous_date: datetime):
    # Get Repos
    repo = gh.get_repo(repo)
    pulls = repo.get_pulls(state='all', sort='updated', direction='desc')
    pr_details = []
    pr_summary = {
        "open": 0,
        "closed": 0,
        "draft": 0
    }
    for pr in pulls:
        if pr.updated_at > previous_date:
            pr_table_row = f"<tr><td>{pr.id}</td><td>{pr.state}</td><td>{pr.created_at.date()}<td>{pr.updated_at.date()}</td><td>{pr.title}</td></tr>"
            pr_details.append(pr_table_row)

            if pr.state == 'open':
                pr_summary['open'] = pr_summary['open'] + 1
            elif pr.state == 'closed':
                pr_summary['closed'] = pr_summary['closed'] + 1
            elif pr.draft:
                pr_summary['draft'] = pr_summary['draft'] + 1
            else:
                print(
                    f"No state was matched. Status: {pr.state} ; Draft: {pr.draft}")
        else:
            print(
                f"Found {len(pr_details)} PRs updated after {previous_date.date()}")
            break

    return {'details': pr_details, 'summary': pr_summary}


def html_body(repo, previous_date: datetime, details: list, summary: dict):
    table_rows = ""
    for row in details:
        table_rows = f"{table_rows} {row}"

    html_content = f"""
<strong>Summary of Pull Requests for Repo {repo}</strong>
<br/>
Summary:
<ul>
  <li>PRs Updated After {previous_date.date()}</li>
  <li>Open: {summary['open']}</li>
  <li>Closed: {summary['closed']}</li>
  <li>Draft: {summary['draft']}</li>
</ul>

PR Details:

<table>
  <tr>
    <th>ID</th>
    <th>Status</th>
    <th>Created Date</th>
    <th>Updated Date</th>
    <th>Title</th>
  </tr>
  {table_rows}
</table>
"""

    return html_content
