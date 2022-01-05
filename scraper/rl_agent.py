import numpy as np
import time
from scraper.gitrepo import *
from scraper.gituser import *

MOVE_MASTER = 0
MOVE_SAME_OWNER = 1
MOVE_FROM_FOLLOWERS = 2
MOVE_FROM_FOLLOWING = 3
MOVE_FORKS = 4
MOVE_COMMITS = 5
MOVE_STACK = 6

REPOSITORY_STACK_SIZE = 1000
repository_stack=[]
np.random.seed(int(time.time()))
#np.random.seed(0)

def pile_repository(repo, tag):
    if repository_stack.count(repo) == 0:
        repo.log(tag)
        repo.owner.log(tag)
        repository_stack.append(repo)
        if len(repository_stack)>REPOSITORY_STACK_SIZE:
            repository_stack.pop(0)

def get_random_repo_from_repository_stack(current_repo):
    try:
        return repository_stack[int(len(repository_stack) * np.random.rand(1)[0])]
    except:
        return current_repo

def get_random_repo_from_owner(owner, current_repo):
    try:
        item_number = int(owner.repos_count * np.random.rand(1)[0])
        new_repo_full_name = get_github_collection_item(f"https://api.github.com/users/{owner.login}/repos", item_number)["full_name"]
        if new_repo_full_name == current_repo.full_name:
            new_repo_full_name = get_github_collection_item(f"https://api.github.com/users/{owner.login}/repos", (item_number + 1) % owner.repos_count)["full_name"]
        return GitRepository(new_repo_full_name, owner)
    except:
        return current_repo

def get_random_repo_from_followers(owner, current_repo,):
    try:
        item_number = int(owner.followers_count * np.random.rand(1)[0])
        follower_login = get_github_collection_item(f"https://api.github.com/users/{owner.login}/followers", item_number)["login"]
        follower = GitUser(follower_login)
        return get_random_repo_from_owner(follower, current_repo)
    except:
        return current_repo

def get_random_repo_from_following(owner, current_repo):
    try:
        item_number = int(owner.following_count * np.random.rand(1)[0])
        following_login = get_github_collection_item(f"https://api.github.com/users/{owner.login}/following", item_number)["login"]
        following = GitUser(following_login)
        return get_random_repo_from_owner(following, current_repo)
    except:
        return current_repo


def get_random_repo_from_forks(current_repo):
    try:
        item_number = int(current_repo.forks * np.random.rand(1)[0])
        fork_full_name = get_github_collection_item(f"https://api.github.com/repos/{current_repo.full_name}/forks", item_number)["full_name"]
        return GitRepository(fork_full_name)
    except:
        return current_repo

def get_random_repo_from_commits(current_repo):
    if current_repo.commits_count > 0:
        item_number = int(current_repo.commits_count * np.random.rand(1)[0])
        try:
            committer_login = get_github_collection_item(f"https://api.github.com/repos/{current_repo.full_name}/commits", item_number)["committer"]["login"]
        except:
            try:
                committer_login = get_github_collection_item(f"https://api.github.com/repos/{current_repo.full_name}/commits", item_number)["author"]["login"]
            except:
                committer_login = current_repo.owner_login
        committer = GitUser(committer_login)
        return get_random_repo_from_owner(committer, current_repo)
    else:
        return current_repo


def move_to_next_repository(current_repo, probabilities, tag):
    try:
        pile_repository(current_repo, tag)
        new_repo = current_repo
        random_level=np.random.rand(1)[0]

        # Case Master
        probability_level=probabilities[MOVE_MASTER]
        if probability_level>random_level:
            if current_repo.fork:
                new_repo = GitRepository(current_repo.parent_full_name)
            random_level = 1.0
            print(f"Case Master: Current repo is {current_repo.full_name} new repo is {new_repo.full_name}")

        # Case Owner
        probability_level += probabilities[MOVE_SAME_OWNER]
        if probability_level>random_level:
            new_repo = get_random_repo_from_owner(current_repo.owner, current_repo)
            random_level = 1.0
            print(f"Case Same owner: Current repo is {current_repo.full_name} new repo is {new_repo.full_name}")

        # Case Followers
        probability_level += probabilities[MOVE_FROM_FOLLOWERS]
        if probability_level>random_level:
            new_repo = get_random_repo_from_followers(current_repo.owner, current_repo)
            random_level = 1.0
            print(f"Case Followers: Current repo is {current_repo.full_name} new repo is {new_repo.full_name}")

        # Case Followings
        probability_level += probabilities[MOVE_FROM_FOLLOWING]
        if probability_level>random_level:
            new_repo = get_random_repo_from_following(current_repo.owner, current_repo)
            random_level = 1.0
            print(f"Case Followings: Current repo is {current_repo.full_name} new repo is {new_repo.full_name}")

        # Case Forks
        probability_level += probabilities[MOVE_FORKS]
        if probability_level>random_level:
            new_repo = get_random_repo_from_forks(current_repo)
            random_level = 1.0
            print(f"Case Forks: Current repo is {current_repo.full_name} new repo is {new_repo.full_name}")

        # Case Commits
        probability_level += probabilities[MOVE_COMMITS]
        if probability_level>random_level:
            new_repo = get_random_repo_from_commits(current_repo)
            random_level = 1.0
            print(f"Case Commits: Current repo is {current_repo.full_name} new repo is {new_repo.full_name}")

        # Case Stack
        probability_level += probabilities[MOVE_STACK]
        if probability_level>random_level:
            new_repo = get_random_repo_from_repository_stack(current_repo)
            print(f"Case Stack: Current repo is {current_repo.full_name} new repo is {new_repo.full_name}")

        return new_repo

    except:
        return current_repo
