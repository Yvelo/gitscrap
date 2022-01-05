import math
from scraper.connections import *
from pprint import pprint

class GitUser:

    def __init__(self, login):
        try:
            self.login = login
            self._query_github()
        except Exception as ex:
            print(f"User creation failed: {repr(ex)}")
            raise ex

    def __str__(self):
        return str(pprint(vars(self)))

    def _query_github(self):
        try:
            json_user=get_from_github(f"https://api.github.com/users/{self.login}")
            # mapping of the most important fields of github API
            self.id = json_user["id"]
            self.node_id = json_user["node_id"]
            self.site_admin = json_user["site_admin"]
            self.type = json_user["type"]

            json_followers = get_github_collection_count(f"https://api.github.com/users/{self.login}/followers")
            self.followers_count = json_followers

            json_following = get_github_collection_count(f"https://api.github.com/users/{self.login}/following")
            self.following_count = json_following

            json_subscriptions = get_github_collection_count(f"https://api.github.com/users/{self.login}/subscriptions")
            self.subscriptions_count = json_subscriptions

            json_organizations = get_github_collection_count(f"https://api.github.com/users/{self.login}/orgs")
            self.organizations_count = json_organizations

            json_repos = get_github_collection_count(f"https://api.github.com/users/{self.login}/repos")
            self.repos_count = json_repos

            json_events = get_github_collection_count(f"https://api.github.com/users/{self.login}/events")
            self.events_count = json_events

        except Exception as ex:
            print(f"API call failed: {repr(ex)}")
            raise ex

    def score(self):
        try:
            return math.log10(self.followers_count*10 + self.subscriptions_count + self.organizations_count
                            + self.repos_count*5 + self.events_count+1)
        except Exception:
            return 0

    def log(self, tag):
        try:
            persist_statements([f"""
            INSERT INTO users (
                login,
                user_id,
                node_id,
                site_admin,
                type,
                followers_count,
                following_count,
                subscriptions_count,
                organizations_count,
                repos_count,
                events_count,
                user_score,
                tag,
                recorded_on
            ) VALUES (
                '{self.login}',
                {self.id},
                '{self.node_id}',
                {self.site_admin},
                '{self.type}',
                {self.followers_count},
                {self.following_count},
                {self.subscriptions_count},
                {self.organizations_count},
                {self.repos_count},
                {self.events_count},
                {self.score()},
                '{tag}',
                NOW()
                )"""])
        except Exception as ex:
            print(f"SQL call failed: {repr(ex)}")
            raise ex
