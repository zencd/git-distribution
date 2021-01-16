import errno
import json
import os
import shutil
import stat
import sys
import time
from multiprocessing import Process
from pathlib import Path

import pygit2
import requests

app_dir = os.getenv('APP_DIR') or str(Path(__file__).parent.parent)
work_dir = os.path.join(app_dir, 'work')
versions_dir = os.path.join(work_dir, 'versions')
new_ver_dir_short = str(int(time.time()))
new_ver_dir_full = os.path.join(versions_dir, new_ver_dir_short)
local_history_file = os.path.join(app_dir, 'history.txt')
tmp_history_file = os.path.join(new_ver_dir_full, 'history.txt')
local_commit_file = os.path.join(work_dir, 'current-commit')
cur_ver_file = os.path.join(work_dir, 'app-version')

git_url = 'https://github.com/zencd/git-distribution'
git_branch = 'single-branch'
recent_commit_url = 'https://api.github.com/repos/zencd/git-distribution/commits/single-branch'


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


# def copy_repo_tree(src_dir, dst_dir):
#     for f in os.listdir(src_dir):
#         if f != '.git':
#             src_full = os.path.join(src_dir, f)
#             dst_full = os.path.join(dst_dir, f)
#             if os.path.isdir(src_full):
#                 rmtree(dst_full)
#                 shutil.copytree(src_full, dst_full)
#             else:
#                 shutil.copyfile(src_full, dst_full)


def mkdirs_for_regular_file(filename: str):
    """Создаёт все необходимые директории чтобы можно было записать указанный файл"""
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        try:
            os.makedirs(dirname)
        except OSError as e:  # Guard against race condition
            if e.errno != errno.EEXIST:
                raise


def write_file(fname: str, content: str):
    mkdirs_for_regular_file(fname)
    with open(fname, 'w') as fd:
        return fd.write(content)


def main():
    print(f'App dir: {app_dir}')
    print(f'Updating from {git_url} branch {git_branch}')
    # print(f'File: {__file__}')
    # print(f'APP_DIR: {os.getenv("APP_DIR")}')
    # sys.exit(1)

    # history_before = load_local_history(local_history_file)

    # local_sha = read_current_sha()
    # remote_sha = read_remote_sha()

    rmtree(new_ver_dir_full)
    git_clone(git_url, new_ver_dir_full, git_branch)
    write_file(cur_ver_file, new_ver_dir_short)
    print('Updated to the recent version')
    # repo_tmp = pygit2.Repository(new_ver_dir)
    # tmp_sha = read_repo_sha(repo_tmp)
    #
    # app_dir_2 = os.getenv('APP_DIR')
    #
    # has_update = (local_sha != tmp_sha) or (local_sha is None)
    # if has_update:
    #     # copy_repo_tree(repo_dir_tmp, app_dir)
    #     write_current_sha(tmp_sha)
    #     history_after = load_local_history(tmp_history_file)
    #     print_history_diff(history_before, history_after)
    #     print('Updated to the recent version')
    # else:
    #     print('Nothing to update')

    # rmtree(new_ver_dir)


if __name__ == '__main__':
    main()
