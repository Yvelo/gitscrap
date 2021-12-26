def print_hi(name):
    print(f"Bonjour, {name}")


class GitRepository:
    repos_history = [""]

    def __init__(self, repo_name):
        self.repo_name = repo_name


class GitUser:

    def __init__(self, user_name):
        self.user_name = user_name


if __name__ == "__main__":
    print_hi("PyCharm")
