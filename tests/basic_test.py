from scraper.gitrepo import *
from scraper.gituser import *
from scraper.connections import *

repository_list=["chaoss/augur", "airbytehq/airbyte", "frontity/frontity", "gitpod-io/gitpod", "hoppscotch/hoppscotch", "kinvolk/inspektor-gadget", "meilisearch/MeiliSearch", "matomo-org/matomo", "n8n-io/n8n", "nocodb/nocodb", "ory/hydra", "polyaxon/polyaxon", "robocorp/rpaframework", "strapi/strapi", "quickwit-inc/tantivy", "Teevity/ice", "traefik/traefik", "scilab/scilab", "snyk/snyk", "wasmerio/wasmer"]

persist_statements(["DELETE FROM users", "DELETE FROM repos"])
for repository in repository_list:
    print(f"Processing repository {repository}")
    git_repo=GitRepository(repository)
    git_user=GitUser(git_repo.owner_login)

rows=get_cursor("SELECT * from users ORDER BY ID DESC LIMIT 1")
print(rows)

