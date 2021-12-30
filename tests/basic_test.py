from scraper.gitrepo import *
from scraper.gituser import *
from scraper.connections import *
from scraper.rl_agent import *

repository_list=["torvalds/linux","chaoss/augur", "airbytehq/airbyte", "frontity/frontity", "gitpod-io/gitpod", "hoppscotch/hoppscotch", "kinvolk/inspektor-gadget", "meilisearch/MeiliSearch", "matomo-org/matomo", "n8n-io/n8n", "nocodb/nocodb", "ory/hydra", "polyaxon/polyaxon", "robocorp/rpaframework", "strapi/strapi", "quickwit-inc/tantivy", "Teevity/ice", "traefik/traefik", "scilab/scilab", "snyk/snyk", "wasmerio/wasmer"]
repository_list=["nfonrose/oliverjash.me"]

def test_case_1():
    persist_statements(["DELETE FROM users", "DELETE FROM repos"])
    for repository in repository_list:
        print(f"Processing repository {repository}")
        git_repo=GitRepository(repository)
        git_user=GitUser(git_repo.owner_login)

    rows=get_cursor("SELECT * from users ORDER BY ID DESC LIMIT 1")
    print(rows)

def test_case_2():
    git_repo = GitRepository("nfonrose/oliverjash.me")
    for number in range(2):
        git_repo = move_to_next_repository(git_repo, [0.2,0.2,0.2,0.1,0.1,0.1,0.1])
        print(git_repo)


test_case_2()
