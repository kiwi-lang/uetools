import subprocess


def git_status(repo):
    """Return git status of a given repo"""
    return subprocess.check_output(["git", "status"], cwd=repo, text=True)


def git_diff(repo):
    """Return git diff of a given repo"""
    return subprocess.check_output(["git", "diff"], cwd=repo, text=True)
