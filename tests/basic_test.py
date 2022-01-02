from scraper.gitrepo import *
from scraper.gituser import *
from scraper.connections import *
from scraper.rl_agent import *

def reset_database():
    persist_statements(["DELETE FROM users", "DELETE FROM repos"])

def test_case_1():
    repository_list = ["torvalds/linux", "chaoss/augur", "airbytehq/airbyte", "frontity/frontity", "gitpod-io/gitpod",
                       "hoppscotch/hoppscotch", "kinvolk/inspektor-gadget", "meilisearch/MeiliSearch",
                       "matomo-org/matomo", "n8n-io/n8n", "nocodb/nocodb", "ory/hydra", "polyaxon/polyaxon",
                       "robocorp/rpaframework", "strapi/strapi", "quickwit-inc/tantivy", "Teevity/ice",
                       "traefik/traefik", "scilab/scilab", "snyk/snyk", "wasmerio/wasmer"]
    #repository_list=["learn-co-students/recursion-lab-v-000"]
    for repository in repository_list:
        print(f"Processing repository {repository}")
        git_repo=GitRepository(repository)
        git_repo.log("Reference repositories")
        git_repo.owner.log("Reference repositories")

    rows=get_cursor("SELECT * from repos ORDER BY ID DESC LIMIT 1")
    print(rows)

def test_case_2():
    probabilities = [0.1,0.1,0.1,0.2,0.2,0.2,0.1]
    git_repo = GitRepository("learn-co-students/recursion-lab-v-000")
    for number in range(100000):
        git_repo = move_to_next_repository(git_repo, probabilities, f"Classic sequence probability vector {str(probabilities)}")

#reset_database()
#test_case_1()
test_case_2()
