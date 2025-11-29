from git import Repo
from argparse import ArgumentParser
from datetime import datetime, timezone, timedelta


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

log = []

for commit in commits:
    message = commit.message.strip()
    if '\n' in message:
        message = message.split('\n')[0] + "..."

    log.append(
        f"{currentVersionNumber} - {commit.hexsha} - {commit.committed_datetime.isoformat()} - {message}"
    )
    currentVersionNumber.increment_patch()


for entry in reversed(log):
    print(entry)
