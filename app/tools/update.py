import json
import os
import shutil
import stat
import sys
from multiprocessing import Process
from pathlib import Path

import pygit2
import requests


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


def get_local_and_remote_shas(local_repo):
    resp = requests.get('https://api.github.com/repos/zencd/git-distribution/commits/release')
    if resp.ok:
        remote_commit = json.loads(resp.text)
        remote_sha = remote_commit['sha']
    else:
        print(f'Cannot get latest release')
        remote_sha = None

    local_sha = None
    if local_repo:
        head = local_repo.head
        local_sha = head.target.hex

    return local_sha, remote_sha


def main():
    git_url = 'https://github.com/zencd/git-distribution'
    git_branch = 'release'
    app_dir = str(Path(__file__).parent.parent)
    repo_dir = os.path.join(app_dir, 'repo')
    repo_dir_tmp = os.path.join(app_dir, 'repo_')

    print(f'App dir: {app_dir}')
    print(f'Updating from {git_url} branch {git_branch}')

    repo = None

    if os.path.exists(repo_dir):
        repo = pygit2.Repository(repo_dir)
        local_sha, remote_sha = get_local_and_remote_shas(repo)
        if (local_sha == remote_sha) and (local_sha is not None) and (remote_sha is not None):
            print(f'Already up to date')
            return

    rmtree(repo_dir_tmp)
    git_clone(git_url, repo_dir_tmp, git_branch)
    rmtree(repo_dir)
    shutil.copytree(repo_dir_tmp, repo_dir)
    rmtree(repo_dir_tmp)
    print('Updated to the recent version')


if __name__ == '__main__':
    main()
