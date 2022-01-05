## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Algorithm](#algorithm)
* [Setup](#setup)
* [Results](#results)
* [References](#references)

## General info
The overall objective of gitscrap is to navigate github using its public API in such a way as to discover as many well ranked repositories as possible. The algorithm relies on Reinforcement learning with policy gradients techniques.

## Technologies
This project is developped in Python 3.9 and requires a Progress SQL server to persist KPI calculated for GitHub repositories and users. it uses the following libraries:
* psycopg2 to connect to progress SQL.
* numpy to perform the linear operations required by the machine learning algorithm.
* requests to connect to GitHub API.
* mathplotlib to prepare graphical representaion comparing the various algorithms

## Algorithm
In the context of GitHub Scraping, the main Reinforcement learning concepts consists of:
* GitScrap is a Python agent that fetches a set of information (the repository state) from any GitHub repository and stores them in a Progress database as a time series. It must do so without exceeding the GitHub API limitation of 5000 calls per hour.
* The state of the repository, in addition to a set descriptive fields (repository name, license…) consists of several key metrics:
    * Number of stars.
    * Number of forks.
    * Number of contributors.
    * Is the repo a fork or a master.
    * Number of commits.
    * Number of Pull requests.
* More advanced KPIs could be added as we see fit (e.g. size of code base,...).
* The reward of GitScrap agent is calculated while summing each repository rank in the action sequence. The repository rank is calculated from the key metrics of the repository and is mostly derived from the number of stars of the repository. The rank is null if the repository has already been processed by the agent in one of its last K actions.
* The possible actions of the agent are selected randomly :
    * Process the parent repository in case the current repository is a fork (MASTER).
    * Process one repository sharing the same owner (SAME OWNER).
    * Process one repository owned by a follower of the repository owner (FOLLOWERS).
    * Process one repository owned by a following of the repository owner (FOLLOWING).
    * Process the master repository of one fork owned by the repository owner (FORKS).
    * Process one repository where the repository owner has committed (COMMITS).
    * Process one master repository picked at random among the K last actions (STAK). This action will complete the trajectory (the sequence of actions and states).
* In case an action does not change the repository it is simply ignored, no rewards are granted and a new action is selected randomly.

When the algorithm has to pick a repository among many, it uses a biased random selection: the repository with the highest rank is selected out of T trials. 

In parallel a reporting engine regularly processes the top N repositories sorted by rank so that to build reliable evolution statistics on the pool of the best ranked repositories. User KPIs are also collected by the algorithm.

The algorithm has been first be implemented without reinforcement learning while assigning fixed probabilities to each action independently of the state of the system. This basic random walk through GitHub is not rapid enough to be useful to monitor GitHub. It can however serve as a baseline to evaluate the efficiency gains of reinforced learning. 

The repository score is calculated as follow:

<img src="https://render.githubusercontent.com/render/math?math=\color{brown}\large\ score = \log _{10}\left(stars %2B forks %2B branches %2B events %2B 10 * collaborators %2B \Large\frac{commits}{100}\right)">

## Setup
GitScrapt consists of the following components:
* Class GitRepositories: Allows to fetch and persits the main attributes of a repository object in GitHub
* Class GitUser: Allows to fetch and persits the main attributes of a repository user in GitHub
* A module with connections functions to connect to GitHub API and Progress SQL server.
* A module with the reinforced learning algorithms
* A module to organise GitScrap testing.
* A module to prepare graphics on the data collected.

To connect to gitHub you need to get an API token from your GitHub account such as token="ghp_xUiJ0LRNJYL34t6xhsGbtU7n155IvL1Z0aUZ"

The .env files in the root repository is used to stored passwords and API key so that they are not published on GitHub:

DATABASE_IP="10.28.0.3"

DATABASE_NAME="gitscrap"

DATABASE_USER="scraping"

DATABASE_PASSWORD="..."

GITHUB_USER="..."

GITHUB_API_KEY="..."

## Results
### Without reinforcement learning
In this case the algorithm moves from repositories to repositories using fixed and predetermined probabilities to decide between each of the seven possible actions.

In average GitScrap discovers 0.28 repositories each second which is not enough to cover the current growth rate of GitHub. An hourly pattern can be observed on the discovery speed. It corresponds to an improvable method to account for GitHub API speed limitation. 

As a reference, the average score of a pool of 30 Open Source repositories with successful commercial extensions is 4.16 (as compared with 1.72 for a random selection of repositories). When randomly selected 2.3% (est. 650000 public repositories) of the repositories have a score greater than 4. Even if the reinforced learning algorithm would only pick repositories with a score greater than 4 it would take him 6 months to inventory 90% of them.

![alt text](https://github.com/Yvelo/gitscrap/blob/main/rds_any_score_1.png?raw=true)

When we focus on the discovery of repositories with a score greater than 3 there are no indications of non-random bias in the discovery process. 

![alt text](https://github.com/Yvelo/gitscrap/blob/main/rds_score_gt_3.png?raw=true)

Modifying the set of action probabilities does not seem to have an observable impact on the discovery speed.The increase of the stack size form 100 to 1000 doesn't either seem to increase the algorithm velocity.

![alt text](https://github.com/Yvelo/gitscrap/blob/main/rds_any_score_2.png?raw=true)

#### Statistics for all test runs combined
* Repositories found: 20283.
* Distinct repositories found: 18259 (90.0 %).
* Distinct repositories with a score greater than 3: 1243 (6.1 %).
* Distinct repositories with a score greater than 4: 451 (2.2 %).
* Distinct repositories with a score greater than 5: 83 (0.4 %).
* Distinct repositories with a score greater than 6: 3 (0.0 %).

#### Statistics per test runs
* Session: Classic sequence probability vector [0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.1]
    * Processing time: 39927 seconds.
    * Repositories found: 4522 at a speed of 0.113 repository/second.
    * Distinct repositories found: 4021 (88.9 %) at a speed of 0.101 repository/second.
* Session: Classic sequence probability vector [0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.1]
    * Processing time: 20555 seconds.
    * Repositories found: 2132 at a speed of 0.104 repository/second.
    * Distinct repositories found: 2016 (94.6 %) at a speed of 0.098 repository/second.
* Session: Stack size 1000 and probability vector [0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.1]
    * Processing time: 26688 seconds.
    * Repositories found: 2693 at a speed of 0.101 repository/second.
    * Distinct repositories found: 2504 (93.0 %) at a speed of 0.094 repository/second.
* Session: Stack size 100 and probability vector [0.19, 0.1, 0.1, 0.2, 0.2, 0.2, 0.01]
    * Processing time: 30959 seconds.
    * Repositories found: 3073 at a speed of 0.099 repository/second.
    * Distinct repositories found: 2773 (90.2 %) at a speed of 0.090 repository/second.
* Session: Reference repositories
    * Processing time: 226 seconds.
    * Repositories found: 21 at a speed of 0.093 repository/second.
    * Distinct repositories found: 21 (100.0 %) at a speed of 0.093 repository/second.
* Session: Stack size 1000 and probability vector [0.19, 0.1, 0.1, 0.2, 0.2, 0.2, 0.01]
    * Processing time: 79289 seconds.
    * Repositories found: 7842 at a speed of 0.099 repository/second.
    * Distinct repositories found: 7024 (89.6 %) at a speed of 0.089 repository/second.

#### Reference repositories
* Repository https://github.com/torvalds/linux (score: 5.7, commits: 1060197, forks: 40484, found: 1).
* Repository https://github.com/strapi/strapi (score: 5.0, commits: 19755, forks: 5106, found: 1).
* Repository https://github.com/traefik/traefik (score: 4.9, commits: 4219, forks: 4007, found: 1).
* Repository https://github.com/hoppscotch/hoppscotch (score: 4.8, commits: 3943, forks: 2475, found: 1).
* Repository https://github.com/n8n-io/n8n (score: 4.6, commits: 5221, forks: 2035, found: 1).
* Repository https://github.com/matomo-org/matomo (score: 4.6, commits: 28046, forks: 2240, found: 1).
* Repository https://github.com/nocodb/nocodb (score: 4.5, commits: 1789, forks: 1250, found: 1).
* Repository https://github.com/meilisearch/MeiliSearch (score: 4.4, commits: 3223, forks: 715, found: 1).
* Repository https://github.com/ory/hydra (score: 4.4, commits: 2889, forks: 1150, found: 1).
* Repository https://github.com/wasmerio/wasmer (score: 4.2, commits: 11101, forks: 453, found: 1).
* Repository https://github.com/airbytehq/airbyte (score: 4.2, commits: 4389, forks: 826, found: 1).
* Repository https://github.com/gitpod-io/gitpod (score: 4.1, commits: 3096, forks: 698, found: 1).
* Repository https://github.com/quickwit-inc/tantivy (score: 4.0, commits: 2135, forks: 339, found: 1).
* Repository https://github.com/snyk/snyk (score: 3.9, commits: 4392, forks: 410, found: 1).
* Repository https://github.com/Teevity/ice (score: 3.9, commits: 251, forks: 445, found: 1).
* Repository https://github.com/polyaxon/polyaxon (score: 3.8, commits: 9659, forks: 295, found: 1).
* Repository https://github.com/chaoss/augur (score: 3.8, commits: 6774, forks: 530, found: 1).
* Repository https://github.com/frontity/frontity (score: 3.7, commits: 5806, forks: 213, found: 1).
* Repository https://github.com/kinvolk/inspektor-gadget (score: 3.2, commits: 879, forks: 57, found: 1).
* Repository https://github.com/robocorp/rpaframework (score: 3.2, commits: 1587, forks: 84, found: 1).
* Repository https://github.com/scilab/scilab (score: 3.2, commits: 55253, forks: 67, found: 1).

#### Top 100 repositories found
* Repository https://github.com/jtleek/datasharing (score: 6.4, commits: 29, forks: 239621, found: 3).
* Repository https://github.com/octocat/Spoon-Knife (score: 6.1, commits: 3, forks: 121096, found: 1).
* Repository https://github.com/tensorflow/tensorflow (score: 6.0, commits: 123266, forks: 86035, found: 1).
* Repository https://github.com/twbs/bootstrap (score: 6.0, commits: 21375, forks: 75665, found: 6).
* Repository https://github.com/github/gitignore (score: 5.9, commits: 3486, forks: 71403, found: 3).
* Repository https://github.com/jwasham/coding-interview-university (score: 5.9, commits: 1822, forks: 54448, found: 1).
* Repository https://github.com/EbookFoundation/free-programming-books (score: 5.8, commits: 6968, forks: 46707, found: 1).
* Repository https://github.com/nightscout/cgm-remote-monitor (score: 5.8, commits: 5915, forks: 60763, found: 4).
* Repository https://github.com/rdpeng/ExData_Plotting1 (score: 5.7, commits: 3, forks: 56120, found: 1).
* Repository https://github.com/facebook/react (score: 5.7, commits: 14701, forks: 36589, found: 1).
* Repository https://github.com/torvalds/linux (score: 5.7, commits: 1060197, forks: 40495, found: 5).
* Repository https://github.com/tensorflow/models (score: 5.7, commits: 7682, forks: 45322, found: 2).
* Repository https://github.com/vuejs/vue (score: 5.7, commits: 3220, forks: 31087, found: 1).
* Repository https://github.com/eugenp/tutorials (score: 5.7, commits: 23614, forks: 46118, found: 2).
* Repository https://github.com/996icu/996.ICU (score: 5.7, commits: 3019, forks: 21428, found: 1).
* Repository https://github.com/TheAlgorithms/Python (score: 5.7, commits: 2382, forks: 33676, found: 1).
* Repository https://github.com/firstcontributions/first-contributions (score: 5.6, commits: 35998, forks: 41985, found: 2).
* Repository https://github.com/ant-design/ant-design (score: 5.6, commits: 21429, forks: 31903, found: 2).
* Repository https://github.com/kubernetes/kubernetes (score: 5.6, commits: 105561, forks: 30811, found: 1).
* Repository https://github.com/github/docs (score: 5.6, commits: 19491, forks: 36665, found: 4).
* Repository https://github.com/public-apis/public-apis (score: 5.6, commits: 4213, forks: 19985, found: 1).
* Repository https://github.com/trekhleb/javascript-algorithms (score: 5.5, commits: 962, forks: 21551, found: 2).
* Repository https://github.com/airbnb/javascript (score: 5.5, commits: 1914, forks: 22485, found: 2).
* Repository https://github.com/microsoft/vscode (score: 5.5, commits: 91053, forks: 21117, found: 1).
* Repository https://github.com/flutter/flutter (score: 5.5, commits: 27041, forks: 20048, found: 2).
* Repository https://github.com/mui-org/material-ui (score: 5.5, commits: 18772, forks: 25501, found: 2).
* Repository https://github.com/facebook/create-react-app (score: 5.5, commits: 2745, forks: 23541, found: 5).
* Repository https://github.com/django/django (score: 5.5, commits: 30358, forks: 26284, found: 1).
* Repository https://github.com/vinta/awesome-python (score: 5.5, commits: 1624, forks: 20446, found: 1).
* Repository https://github.com/DefinitelyTyped/DefinitelyTyped (score: 5.5, commits: 78950, forks: 26415, found: 2).
* Repository https://github.com/iluwatar/java-design-patterns (score: 5.5, commits: 3188, forks: 22470, found: 1).
* Repository https://github.com/angular/angular (score: 5.5, commits: 22598, forks: 20651, found: 1).
* Repository https://github.com/scikit-learn/scikit-learn (score: 5.4, commits: 27703, forks: 22465, found: 2).
* Repository https://github.com/git/git (score: 5.4, commits: 65438, forks: 22716, found: 1).
* Repository https://github.com/jquery/jquery (score: 5.4, commits: 6549, forks: 20199, found: 1).
* Repository https://github.com/rails/rails (score: 5.4, commits: 82576, forks: 19993, found: 2).
* Repository https://github.com/slatedocs/slate (score: 5.4, commits: 675, forks: 21036, found: 2).
* Repository https://github.com/keras-team/keras (score: 5.4, commits: 6308, forks: 18961, found: 2).
* Repository https://github.com/vercel/next.js (score: 5.4, commits: 10221, forks: 15975, found: 1).
* Repository https://github.com/golang/go (score: 5.4, commits: 51038, forks: 13975, found: 2).
* Repository https://github.com/shadowsocks/shadowsocks (score: 5.4, commits: 1, forks: 19433, found: 1).
* Repository https://github.com/wesbos/JavaScript30 (score: 5.4, commits: 376, forks: 20851, found: 1).
* Repository https://github.com/atom/atom (score: 5.4, commits: 38462, forks: 16751, found: 2).
* Repository https://github.com/BVLC/caffe (score: 5.3, commits: 4156, forks: 18914, found: 4).
* Repository https://github.com/hakimel/reveal.js (score: 5.3, commits: 2861, forks: 15897, found: 1).
* Repository https://github.com/ColorlibHQ/AdminLTE (score: 5.3, commits: 2381, forks: 17302, found: 1).
* Repository https://github.com/CSSEGISandData/COVID-19 (score: 5.3, commits: 5006, forks: 18266, found: 4).
* Repository https://github.com/pytorch/pytorch (score: 5.3, commits: 42702, forks: 14582, found: 2).
* Repository https://github.com/atralice/Curso.Prep.Henry (score: 5.3, commits: 125, forks: 19198, found: 1).
* Repository https://github.com/protocolbuffers/protobuf (score: 5.3, commits: 8918, forks: 13598, found: 1).
* Repository https://github.com/30-seconds/30-seconds-of-code (score: 5.3, commits: 5397, forks: 9582, found: 1).
* Repository https://github.com/mmistakes/minimal-mistakes (score: 5.3, commits: 2670, forks: 17654, found: 1).
* Repository https://github.com/kdn251/interviews (score: 5.2, commits: 445, forks: 11714, found: 1).
* Repository https://github.com/MarlinFirmware/Marlin (score: 5.2, commits: 19208, forks: 15792, found: 3).
* Repository https://github.com/chartjs/Chart.js (score: 5.2, commits: 4135, forks: 11326, found: 1).
* Repository https://github.com/tastejs/todomvc (score: 5.2, commits: 2905, forks: 13923, found: 1).
* Repository https://github.com/avelino/awesome-go (score: 5.2, commits: 3994, forks: 9350, found: 1).
* Repository https://github.com/ethereum/go-ethereum (score: 5.2, commits: 13077, forks: 12759, found: 1).
* Repository https://github.com/bailicangdu/vue2-elm (score: 5.2, commits: 505, forks: 12069, found: 1).
* Repository https://github.com/gatsbyjs/gatsby (score: 5.2, commits: 19621, forks: 10071, found: 2).
* Repository https://github.com/ageron/handson-ml (score: 5.2, commits: 497, forks: 12583, found: 1).
* Repository https://github.com/expressjs/express (score: 5.2, commits: 5645, forks: 9403, found: 1).
* Repository https://github.com/Homebrew/legacy-homebrew (score: 5.2, commits: 63882, forks: 11879, found: 3).
* Repository https://github.com/scrapy/scrapy (score: 5.1, commits: 9044, forks: 9454, found: 2).
* Repository https://github.com/remix-run/react-router (score: 5.1, commits: 5189, forks: 8851, found: 2).
* Repository https://github.com/geekcomputers/Python (score: 5.1, commits: 2582, forks: 10584, found: 2).
* Repository https://github.com/godotengine/godot (score: 5.1, commits: 39979, forks: 8150, found: 1).
* Repository https://github.com/swisskyrepo/PayloadsAllTheThings (score: 5.1, commits: 1325, forks: 9156, found: 2).
* Repository https://github.com/etcd-io/etcd (score: 5.1, commits: 17486, forks: 8243, found: 1).
* Repository https://github.com/chrislgarry/Apollo-11 (score: 5.1, commits: 516, forks: 6750, found: 2).
* Repository https://github.com/udacity/fullstack-nanodegree-vm (score: 5.1, commits: 60, forks: 11961, found: 2).
* Repository https://github.com/mathiasbynens/dotfiles (score: 5.1, commits: 761, forks: 8708, found: 1).
* Repository https://github.com/laravel/framework (score: 5.1, commits: 32252, forks: 8787, found: 1).
* Repository https://github.com/thedaviddias/Front-End-Checklist (score: 5.1, commits: 694, forks: 5591, found: 1).
* Repository https://github.com/discourse/discourse (score: 5.0, commits: 43879, forks: 7497, found: 2).
* Repository https://github.com/ripienaar/free-for-dev (score: 5.0, commits: 3915, forks: 5610, found: 1).
* Repository https://github.com/kubernetes/website (score: 5.0, commits: 27396, forks: 10272, found: 1).
* Repository https://github.com/trustwallet/assets (score: 5.0, commits: 12743, forks: 10212, found: 1).
* Repository https://github.com/enaqx/awesome-react (score: 5.0, commits: 1925, forks: 5685, found: 1).
* Repository https://github.com/hashicorp/terraform (score: 5.0, commits: 29351, forks: 7204, found: 4).
* Repository https://github.com/RocketChat/Rocket.Chat (score: 5.0, commits: 20771, forks: 7111, found: 1).
* Repository https://github.com/videojs/video.js (score: 5.0, commits: 3785, forks: 7025, found: 1).
* Repository https://github.com/CocoaPods/Specs (score: 5.0, commits: 639713, forks: 8988, found: 1).
* Repository https://github.com/magento/magento2 (score: 5.0, commits: 126252, forks: 8742, found: 1).
* Repository https://github.com/udacity/create-your-own-adventure (score: 5.0, commits: 12664, forks: 9683, found: 1).
* Repository https://github.com/akullpp/awesome-java (score: 5.0, commits: 1584, forks: 6601, found: 1).
* Repository https://github.com/sindresorhus/awesome-nodejs (score: 5.0, commits: 821, forks: 5246, found: 1).
* Repository https://github.com/fffaraz/awesome-cpp (score: 5.0, commits: 1469, forks: 5916, found: 1).
* Repository https://github.com/strapi/strapi (score: 5.0, commits: 19755, forks: 5106, found: 1).
* Repository https://github.com/openssl/openssl (score: 5.0, commits: 30715, forks: 7549, found: 1).
* Repository https://github.com/facebook/jest (score: 5.0, commits: 5749, forks: 5541, found: 1).
* Repository https://github.com/coder/code-server (score: 5.0, commits: 3157, forks: 4195, found: 2).
* Repository https://github.com/babel/babel (score: 5.0, commits: 14971, forks: 5168, found: 1).
* Repository https://github.com/MunGell/awesome-for-beginners (score: 5.0, commits: 430, forks: 5424, found: 2).
* Repository https://github.com/judasn/IntelliJ-IDEA-Tutorial (score: 5.0, commits: 468, forks: 7248, found: 1).
* Repository https://github.com/jenkinsci/jenkins (score: 5.0, commits: 31953, forks: 7175, found: 1).
* Repository https://github.com/obsproject/obs-studio (score: 5.0, commits: 10299, forks: 5500, found: 1).
* Repository https://github.com/elastic/kibana (score: 4.9, commits: 49411, forks: 7006, found: 2).
* Repository https://github.com/foundation/foundation-sites (score: 4.9, commits: 17200, forks: 5685, found: 1).
* Repository https://github.com/aosabook/500lines (score: 4.9, commits: 3297, forks: 5888, found: 1).

Among the top 100 repositories 63 duplicates (38.7 %) have been found.


### Reinforced learning trajectories
Work in progress...

## References
* https://www.janisklaise.com/post/rl-policy-gradients/
* http://ufldl.stanford.edu/tutorial/supervised/SoftmaxRegression/
* https://medium.com/samkirkiles/reinforce-policy-gradients-from-scratch-in-numpy-6a09ae0dfe12
* https://machinelearningmastery.com/softmax-activation-function-with-python/.
* https://towardsdatascience.com/githubs-path-to-128m-public-repositories-f6f656ab56b1