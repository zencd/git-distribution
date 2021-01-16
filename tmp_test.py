import unittest

import pygit2


def git_pull(repo: pygit2.Repository, remote_name="origin"):
    """
    https://github.com/MichaelBoselowitz/pygit2-examples/blob/68e889e50a592d30ab4105a2e7b9f28fac7324c8/examples.py
    """

    branch = repo.head.shorthand

    for remote in repo.remotes:
        if remote.name == remote_name:
            remote.fetch()
            remote_master_id = repo.lookup_reference(f"refs/remotes/origin/{branch}").target
            merge_result, _ = repo.merge_analysis(remote_master_id)
            if merge_result & pygit2.GIT_MERGE_ANALYSIS_UP_TO_DATE:
                # Up to date, do nothing
                print('up to date')
                return
            elif merge_result & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
                # We can just fastforward
                print('fastforward')
                repo.checkout_tree(repo.get(remote_master_id))
                master_ref = repo.lookup_reference(f"refs/heads/{branch}")
                master_ref.set_target(remote_master_id)
                repo.head.set_target(remote_master_id)
            elif merge_result & pygit2.GIT_MERGE_ANALYSIS_NORMAL:
                raise Exception("Pulling remote changes leads to a conflict")
            else:
                raise AssertionError("Unknown merge analysis result")


class TmpTestCase(unittest.TestCase):
    def test_pull(self):
        r = pygit2.Repository('C:\\tempo\\pull\\pygit2')
        git_pull(r, 'origin')


if __name__ == '__main__':
    unittest.main()
