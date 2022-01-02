import math
from scraper.connections import *
from scraper.gituser import *
from pprint import pprint

class GitRepository:

    def __init__(self, repo_name, owner = None):
        self.full_name = repo_name
        self._query_github(owner)

    def __str__(self):
        return str(pprint(vars(self)))

    def _query_github(self, owner):
        try:
            json_repository=get_from_github(f"https://api.github.com/repos/{self.full_name}")

            # mapping of the most important fields of github API
            self.id = json_repository["id"]
            self.node_id = json_repository["node_id"]
            self.private = json_repository["private"]
            self.owner_id = json_repository["owner"]["id"]
            self.owner_login = json_repository["owner"]["login"]
            self.owner = owner if not isinstance(owner,type(None)) else GitUser(self.owner_login)
            self.description = json_repository["description"]
            self.size = json_repository["size"]
            self.stargazers_count = json_repository["stargazers_count"]
            self.watchers_count = json_repository["watchers_count"]
            self.topics = ", ".join(json_repository["topics"])
            self.visibility = json_repository["visibility"]
            self.fork = json_repository["fork"]
            self.forks = json_repository["forks"]
            self.parent_full_name = json_repository["parent"]["full_name"] if self.fork else self.full_name
            self.open_issues_count = int(json_repository["open_issues_count"])
            self.network_count = json_repository["network_count"]
            self.subscriber_count = json_repository["subscribers_count"]
            self.license = json_repository["license"]["name"] if not isinstance(json_repository["license"],type(None)) else ""

            json_collaborators = get_github_collection_count(f"https://api.github.com/repos/{self.full_name}/collaborators")
            self.collaborators_count = json_collaborators

            json_commits = get_github_collection_count(f"https://api.github.com/repos/{self.full_name}/commits")
            self.commits_count = json_commits

            json_events = get_github_collection_count(f"https://api.github.com/repos/{self.full_name}/events")
            self.events_count = json_events

            json_branches = get_github_collection_count(f"https://api.github.com/repos/{self.full_name}/branches")
            self.branches_count = json_branches

        except Exception as ex:
            print("API call failed: " + repr(ex))
            raise ex

    def score(self):
        try:
            return math.log10(self.stargazers_count+self.forks*10+self.commits_count/100+self.collaborators_count*10+self.events_count+self.branches_count+1)
        except:
            return 0

    def log(self, tag):
        persist_statements([f"""
        INSERT INTO repos (
            repository_id,
            node_id,
            full_name,
            private,
            owner_id,
            owner_login,
            description,
            size,
            stargazers_count,
            watchers_count,
            topics,
            visibility,
            fork,
            forks,
            open_issues_count,
            network_count,
            subscriber_count,
            license,
            collaborators_count,
            commits_count,
            events_count,
            branches_count,
            repository_score,
            tag,
            recorded_on
        ) VALUES (
            {self.id},
            '{self.node_id}',
            '{self.full_name}',
            {self.private},
            {self.owner_id},
            '{self.owner_login}',
            '{"" if isinstance(self.description,type(None)) else self.description.replace("'","''")}',
            {self.size},
            {self.stargazers_count},
            {self.watchers_count},
            '{self.topics}',
            '{self.visibility}',
            {self.fork},
            {self.forks},
            {self.open_issues_count},
            {self.network_count},
            {self.subscriber_count},
            '{self.license}',
            {self.collaborators_count},
            {self.commits_count},
            {self.events_count},
            {self.branches_count},
            {self.score()},
            '{tag}',
            NOW()
            )"""])
