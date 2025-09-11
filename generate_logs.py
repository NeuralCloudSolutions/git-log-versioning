from git import Repo
from argparse import ArgumentParser
from datetime import datetime, timezone, timedelta
from spire.doc import *
from spire.doc.common import *

class VersionNumber:
    def __init__(self, major=0, minor=0, patch=0):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def increment_major(self):
        self.major += 1
        self.minor = 0
        self.patch = 0

    def increment_minor(self):
        self.minor += 1
        self.patch = 0

    def increment_patch(self):
        self.patch += 1

parser = ArgumentParser(description="Log Commits")
parser.add_argument("--path", type=str,
                    required=True,
                    help="path to repo")
parser.add_argument("--branch", type=str,
                    default="main",
                    help="name of the branch to log commits from")

args = parser.parse_args()

repo = Repo(args.path)
commits = list(repo.iter_commits(args.branch))[::-1]

currentVersionNumber = VersionNumber(1, 0, 0)

grouped_commits = []
current_group = []

if commits[0].committed_datetime.day <= 15:
    current_start_date = commits[0].committed_datetime.replace(day=1, tzinfo=timezone.utc)
else:
    current_start_date = commits[0].committed_datetime.replace(day=16, tzinfo=timezone.utc)

for commit in commits:
    commit_date = commit.committed_datetime.astimezone(timezone.utc)
    if current_start_date.day == 1:
        current_end_date = current_start_date.replace(day=16)
    else:
        next_month = current_start_date.month % 12 + 1
        year = current_start_date.year + (current_start_date.month // 12)
        current_end_date = datetime(year, next_month, 1, 0, 0, 0, tzinfo=timezone.utc)
    if current_start_date <= commit_date < current_end_date:
        current_group.append(commit)
    else:
        if current_group:
            grouped_commits.append((current_start_date, current_end_date, current_group))
        current_group = [commit]
        if commit_date.day <= 15:
            current_start_date = commit_date.replace(day=1, tzinfo=timezone.utc)
        else:
            current_start_date = commit_date.replace(day=16, tzinfo=timezone.utc)
if current_group:
    grouped_commits.append((current_start_date, current_end_date, current_group))

html_string = """
<html>
<head>
    <title>Welcome to My Website</title>
    <style>
        body {
            font-family: Arial;
        }
        h1 {
            color: #000000;
            font-size: 21pt;
            margin-bottom: 20pt;
        }
        p {
            color: #333333;
            font-size: 12pt;
            margin-bottom: 10pt;
        }
        ul {
            margin-left: 20pt;
            margin-bottom: 15pt;
            font-size: 12pt;
        }
        li {
            font-size: 12pt;
            margin-bottom: 5pt;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 20pt;
            font-size: 12pt;
        }
        th, td {
            border: 1pt solid #000000;
            padding: 8pt;
            text-align: left;
        }
        th {
            background-color: #CCCCCC;
            font-weight: bold;
        }
        td {
            color: #000000;
        }
    </style>
</head>
<body>
    <h1>Commit Logs</h1>
    <table>
        <tr>
            <th>Date Range</th>
            <th>Version</th>
            <th>Features</th>
            <th>Commit IDs</th>
            <th>Contributors</th>
        </tr>
"""

for group in grouped_commits:
    date_range = f"{group[0].date().strftime('%m/%d/%Y')} to {(group[1].date() - timedelta(days=1)).strftime('%m/%d/%Y')}"
    version = str(currentVersionNumber)
    features = "* " + "<br>* ".join([commit.message.splitlines()[0] for commit in group[2]])
    commit_ids = "<br>".join([commit.hexsha[:7] for commit in group[2]])
    group_contributors = set(commit.author.name for commit in group[2])
    contributors_str = "<br>".join(sorted(list(group_contributors)))

    html_string += f"""
        <tr>
            <td>{date_range}</td>
            <td>{version}</td>
            <td>{features}</td>
            <td>{commit_ids}</td>
            <td>{contributors_str}</td>
        </tr>
    """

    currentVersionNumber.increment_patch()

html_string += "</table></body></html>"

document = Document()
section = document.AddSection()
paragraph = section.AddParagraph()
paragraph.AppendHTML(html_string)
document.SaveToFile("CommitLogs.docx", FileFormat.Docx2016)
document.Close()