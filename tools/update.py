import json
import os
import shutil
import stat
import sys
from multiprocessing import Process
from pathlib import Path

import pygit2
import requests

git_url = 'https://github.com/zencd/git-distribution'
git_branch = 'single-branch'
recent_commit_url = 'https://api.github.com/repos/zencd/git-distribution/commits/single-branch'
app_dir = str(Path(__file__).parent.parent)
work_dir = os.path.join(app_dir, 'work')
repo_dir_tmp = os.path.join(work_dir, 'repo')
local_history_file = os.path.join(app_dir, 'history.txt')
tmp_history_file = os.path.join(repo_dir_tmp, 'history.txt')
local_commit_file = os.path.join(work_dir, 'recent-commit.txt')


def rmtree(dir_):
    def onerror(func, path, exc_info):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    if os.path.exists(dir_):
        shutil.rmtree(dir_, onerror=onerror)


def _git_clone_impl(git_url, repo_dir_tmp, git_branch):
    pygit2.clone_repository(git_url, repo_dir_tmp, checkout_branch=git_branch)


def git_clone(git_url, repo_dir_tmp, git_branch):
    """В новом процессе потому что pygit2 clone_repository оставляет файлы открытыми"""
    p = Process(target=_git_clone_impl, args=(git_url, repo_dir_tmp, git_branch))
    p.start()
    p.join()
    if p.exitcode != 0:
        print(f'git clone failed, code {p.exitcode}')
        sys.exit(1)


def read_current_sha():
    if os.path.exists(local_commit_file):
        with open(local_commit_file, 'r') as fd:
            return fd.read().strip()
    else:
        return None


def write_current_sha(sha):
    with open(local_commit_file, 'w') as fd:
        return fd.write(sha)


def read_remote_sha():
    res = None
    try:
        resp = requests.get(recent_commit_url)
        if resp.ok:
            remote_commit = json.loads(resp.text)
            res = remote_commit['sha']
    except Exception as e:
        print(f'Error: {e}')
    return res


def read_repo_sha(local_repo: pygit2.Repository):
    if local_repo:
        return local_repo.head.target.hex
    return None


'''
def load_remote_history():
    url = 'https://raw.githubusercontent.com/zencd/git-distribution/release/history.txt'
    resp = requests.get(url)
    if not resp.ok:
        return []
    return [line.strip() for line in resp.text.splitlines()]
'''


def load_local_history(history_file):
    if os.path.exists(history_file):
        with open(history_file, 'r') as fd:
            return [line.strip() for line in fd]
    return []


def print_history_diff(history_before, history_after):
    diff = [x for x in history_after if x and x not in history_before]
    if diff:
        print('What is new:')
        for line in diff:
            print(line)


def copy_repo_tree(src_dir, dst_dir):
    for f in os.listdir(src_dir):
        if f != '.git':
            src_full = os.path.join(src_dir, f)
            dst_full = os.path.join(dst_dir, f)
            if os.path.isdir(src_full):
                rmtree(src_full)
                shutil.copytree(src_full, dst_full)
            else:
                shutil.copyfile(src_full, dst_full)


def main():
    print(f'App dir: {app_dir}')
    print(f'Updating from {git_url} branch {git_branch}')

    history_before = load_local_history(local_history_file)

    local_sha = read_current_sha()
    remote_sha = read_remote_sha()

    rmtree(repo_dir_tmp)
    git_clone(git_url, repo_dir_tmp, git_branch)
    repo_tmp = pygit2.Repository(repo_dir_tmp)
    tmp_sha = read_repo_sha(repo_tmp)

    has_update = (local_sha != tmp_sha) or (local_sha is None)
    if has_update:
        copy_repo_tree(repo_dir_tmp, app_dir)
        write_current_sha(tmp_sha)
        history_after = load_local_history(tmp_history_file)
        print_history_diff(history_before, history_after)
        print('Updated to the recent version')
    else:
        print('Nothing to update')

    rmtree(repo_dir_tmp)


if __name__ == '__main__':
    main()
