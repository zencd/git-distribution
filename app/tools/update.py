import os
import shutil
import stat
import sys
from multiprocessing import Process
from pathlib import Path

import pygit2


def rmtree(dir_):
    def onerror(func, path, exc_info):
        os.chmod(path, stat.S_IWRITE)
        func(path)

    if os.path.exists(dir_):
        shutil.rmtree(dir_, onerror=onerror)


def _git_clone_impl(git_url, repo_dir_tmp, git_branch):
    pygit2.clone_repository(git_url, repo_dir_tmp, checkout_branch=git_branch)


def git_clone(git_url, repo_dir_tmp, git_branch):
    p = Process(target=_git_clone_impl, args=(git_url, repo_dir_tmp, git_branch))
    p.start()
    p.join()
    if p.exitcode != 0:
        print(f'git clone failed, code {p.exitcode}')
        sys.exit(1)


if __name__ == '__main__':
    git_url = 'https://github.com/zencd/git-distribution'
    git_branch = 'release'
    app_dir = str(Path(__file__).parent.parent)
    windows_dir = str(Path(__file__).parent)
    repo_dir = os.path.join(app_dir, 'repo')
    repo_dir_tmp = os.path.join(app_dir, 'repo_')

    print(f'App dir: {app_dir}')
    print(f'Updating from {git_url} branch {git_branch}')

    rmtree(repo_dir_tmp)
    git_clone(git_url, repo_dir_tmp, git_branch)
    rmtree(repo_dir)
    shutil.copytree(repo_dir_tmp, repo_dir)
    rmtree(repo_dir_tmp)
