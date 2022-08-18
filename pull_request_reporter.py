import argparse
# from email.policy import default
import os
from modules import github_request
from modules import send_email
from modules import dot_env
import datetime


parser = argparse.ArgumentParser(
    description='Summarize pull requests and send summary email.')

parser = argparse.ArgumentParser()

parser.add_argument(
    '-r', '--repository', help='Repository to retrieve pull requests from', action='store', type=str, required=False, default="hashicorp/terraform-provider-azurerm")
parser.add_argument(
    '-e', '--email', help='Email to send pull request summary to', action='store', type=str, required=False)
parser.add_argument(
    '-d', '--daysago', help='Number of days ago to get latest pull requests.', type=int, action='store', required=False, default=7)
parser.add_argument(
    '-f', '--formatedEmail', help='Use CSS formated email', action='store_true', required=False)


args = parser.parse_args()

dot_env.load_env()

if hasattr(args, 'email'):
    print("Using Default Email in .env file")
    args.email = os.environ.get('DEFAULT_EMAIL')


previous_date = datetime.datetime.now() - datetime.timedelta(days=args.daysago)

print("Connecting to Github API")
gh = github_request.init_github()
print(f"Retrieving Pull Requests Updated After {previous_date.date()}")
prs = github_request.get_pull_request(
    gh, args.repository, previous_date)

if args.formatedEmail:
    html_body = github_request.html_body_template(
        args.repository, previous_date, prs['details'], prs['summary']
    )
else:
    html_body = github_request.html_body(
        args.repository, previous_date, prs['details'], prs['summary'])

summary_output = f"""

--------------------------------

Retrieved Pull Requests Summary:
 * Repo: {args.repository}
 * Sent to Email: {args.email}
 * Pull Requests Updated After: {previous_date.date()}
 * Open PRs: {prs['summary']['open']}
 * Closed PRs: {prs['summary']['closed']}
 * Draft PRs: {prs['summary']['draft']}

 --------------------------------

"""

print(summary_output)

print("Sending email.....")
send_email.send("crazyspammer@kazisolutions.com", args.email,
                f"Github Pull Request Report for {args.repository}", html_body)
