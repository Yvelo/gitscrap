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
* Repositories found: 12441.
* Distinct repositories found: 11289 (90.7 %).
* Distinct repositories with a score greater than 3: 733 (5.9 %).
* Distinct repositories with a score greater than 4: 282 (2.3 %).
* Distinct repositories with a score greater than 5: 53 (0.4 %).
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
    
#### Reference repositories
* Repository https://github.com/torvalds/linux scores 5.7 and has 1060197 commits
* Repository https://github.com/strapi/strapi scores 5.0 and has 19755 commits
* Repository https://github.com/traefik/traefik scores 4.9 and has 4219 commits
* Repository https://github.com/hoppscotch/hoppscotch scores 4.8 and has 3943 commits
* Repository https://github.com/n8n-io/n8n scores 4.6 and has 5221 commits
* Repository https://github.com/matomo-org/matomo scores 4.6 and has 28046 commits
* Repository https://github.com/nocodb/nocodb scores 4.5 and has 1789 commits
* Repository https://github.com/meilisearch/MeiliSearch scores 4.4 and has 3223 commits
* Repository https://github.com/ory/hydra scores 4.4 and has 2889 commits
* Repository https://github.com/wasmerio/wasmer scores 4.2 and has 11101 commits
* Repository https://github.com/airbytehq/airbyte scores 4.2 and has 4389 commits
* Repository https://github.com/gitpod-io/gitpod scores 4.1 and has 3096 commits
* Repository https://github.com/quickwit-inc/tantivy scores 4.0 and has 2135 commits
* Repository https://github.com/snyk/snyk scores 3.9 and has 4392 commits
* Repository https://github.com/Teevity/ice scores 3.9 and has 251 commits
* Repository https://github.com/polyaxon/polyaxon scores 3.8 and has 9659 commits
* Repository https://github.com/chaoss/augur scores 3.8 and has 6774 commits
* Repository https://github.com/frontity/frontity scores 3.7 and has 5806 commits
* Repository https://github.com/kinvolk/inspektor-gadget scores 3.2 and has 879 commits
* Repository https://github.com/robocorp/rpaframework scores 3.2 and has 1587 commits
* Repository https://github.com/scilab/scilab scores 3.2 and has 55253 commits

#### Top 100 repositories found
* Repository https://github.com/jtleek/datasharing scores 6.4
* Repository https://github.com/octocat/Spoon-Knife scores 6.1
* Repository https://github.com/tensorflow/tensorflow scores 6.0
* Repository https://github.com/twbs/bootstrap scores 6.0
* Repository https://github.com/github/gitignore scores 5.9
* Repository https://github.com/jwasham/coding-interview-university scores 5.9
* Repository https://github.com/EbookFoundation/free-programming-books scores 5.8
* Repository https://github.com/nightscout/cgm-remote-monitor scores 5.8
* Repository https://github.com/torvalds/linux scores 5.7
* Repository https://github.com/tensorflow/models scores 5.7
* Repository https://github.com/996icu/996.ICU scores 5.7
* Repository https://github.com/firstcontributions/first-contributions scores 5.6
* Repository https://github.com/ant-design/ant-design scores 5.6
* Repository https://github.com/kubernetes/kubernetes scores 5.6
* Repository https://github.com/public-apis/public-apis scores 5.6
* Repository https://github.com/github/docs scores 5.6
* Repository https://github.com/trekhleb/javascript-algorithms scores 5.5
* Repository https://github.com/airbnb/javascript scores 5.5
* Repository https://github.com/microsoft/vscode scores 5.5
* Repository https://github.com/flutter/flutter scores 5.5
* Repository https://github.com/mui-org/material-ui scores 5.5
* Repository https://github.com/facebook/create-react-app scores 5.5
* Repository https://github.com/vinta/awesome-python scores 5.5
* Repository https://github.com/scikit-learn/scikit-learn scores 5.4
* Repository https://github.com/jquery/jquery scores 5.4
* Repository https://github.com/rails/rails scores 5.4
* Repository https://github.com/golang/go scores 5.4
* Repository https://github.com/shadowsocks/shadowsocks scores 5.4
* Repository https://github.com/atom/atom scores 5.4
* Repository https://github.com/BVLC/caffe scores 5.3
* Repository https://github.com/hakimel/reveal.js scores 5.3
* Repository https://github.com/ColorlibHQ/AdminLTE scores 5.3
* Repository https://github.com/pytorch/pytorch scores 5.3
* Repository https://github.com/atralice/Curso.Prep.Henry scores 5.3
* Repository https://github.com/MarlinFirmware/Marlin scores 5.2
* Repository https://github.com/ethereum/go-ethereum scores 5.2
* Repository https://github.com/bailicangdu/vue2-elm scores 5.2
* Repository https://github.com/gatsbyjs/gatsby scores 5.2
* Repository https://github.com/ageron/handson-ml scores 5.2
* Repository https://github.com/remix-run/react-router scores 5.1
* Repository https://github.com/geekcomputers/Python scores 5.1
* Repository https://github.com/godotengine/godot scores 5.1
* Repository https://github.com/swisskyrepo/PayloadsAllTheThings scores 5.1
* Repository https://github.com/chrislgarry/Apollo-11 scores 5.1
* Repository https://github.com/mathiasbynens/dotfiles scores 5.1
* Repository https://github.com/discourse/discourse scores 5.0
* Repository https://github.com/ripienaar/free-for-dev scores 5.0
* Repository https://github.com/kubernetes/website scores 5.0
* Repository https://github.com/trustwallet/assets scores 5.0
* Repository https://github.com/enaqx/awesome-react scores 5.0
* Repository https://github.com/hashicorp/terraform scores 5.0
* Repository https://github.com/RocketChat/Rocket.Chat scores 5.0
* Repository https://github.com/CocoaPods/Specs scores 5.0
* Repository https://github.com/magento/magento2 scores 5.0
* Repository https://github.com/udacity/create-your-own-adventure scores 5.0
* Repository https://github.com/sindresorhus/awesome-nodejs scores 5.0
* Repository https://github.com/fffaraz/awesome-cpp scores 5.0
* Repository https://github.com/strapi/strapi scores 5.0
* Repository https://github.com/openssl/openssl scores 5.0
* Repository https://github.com/facebook/jest scores 5.0
* Repository https://github.com/MunGell/awesome-for-beginners scores 5.0
* Repository https://github.com/elastic/kibana scores 4.9
* Repository https://github.com/foundation/foundation-sites scores 4.9
* Repository https://github.com/aosabook/500lines scores 4.9
* Repository https://github.com/neovim/neovim scores 4.9
* Repository https://github.com/Micropoor/Micro8 scores 4.9
* Repository https://github.com/yiisoft/yii2 scores 4.9
* Repository https://github.com/encode/django-rest-framework scores 4.9
* Repository https://github.com/yangshun/front-end-interview-handbook scores 4.9
* Repository https://github.com/mbadolato/iTerm2-Color-Schemes scores 4.9
* Repository https://github.com/facebookresearch/Detectron scores 4.9
* Repository https://github.com/isocpp/CppCoreGuidelines scores 4.9
* Repository https://github.com/traefik/traefik scores 4.9
* Repository https://github.com/Activiti/Activiti scores 4.9
* Repository https://github.com/github/personal-website scores 4.9
* Repository https://github.com/udacity/ud851-Exercises scores 4.9
* Repository https://github.com/swagger-api/swagger-codegen scores 4.9
* Repository https://github.com/scwang90/SmartRefreshLayout scores 4.9
* Repository https://github.com/hashicorp/terraform-provider-aws scores 4.8
* Repository https://github.com/emberjs/ember.js scores 4.8
* Repository https://github.com/hashicorp/consul scores 4.8
* Repository https://github.com/koajs/koa scores 4.8
* Repository https://github.com/bayandin/awesome-awesomeness scores 4.8
* Repository https://github.com/sudheerj/reactjs-interview-questions scores 4.8
* Repository https://github.com/lmoroney/dlaicourse scores 4.8
* Repository https://github.com/hoppscotch/hoppscotch scores 4.8
* Repository https://github.com/kaldi-asr/kaldi scores 4.8
* Repository https://github.com/jenkins-docs/simple-node-js-react-npm-app scores 4.8
* Repository https://github.com/v8/v8 scores 4.8
* Repository https://github.com/vuejs/devtools scores 4.8
* Repository https://github.com/sorin-ionescu/prezto scores 4.8
* Repository https://github.com/telegramdesktop/tdesktop scores 4.7
* Repository https://github.com/airbnb/lottie-ios scores 4.7
* Repository https://github.com/Dreamacro/clash scores 4.7
* Repository https://github.com/pytorch/fairseq scores 4.7
* Repository https://github.com/SwiftyJSON/SwiftyJSON scores 4.7
* Repository https://github.com/udacity/deep-learning-v2-pytorch scores 4.7
* Repository https://github.com/rms-support-letter/rms-support-letter.github.io scores 4.7
* Repository https://github.com/iissnan/hexo-theme-next scores 4.7
* Repository https://github.com/ReactiveX/rxjs scores 4.7

### Reinforced learning trajectories
Work in progress...

## References
* https://www.janisklaise.com/post/rl-policy-gradients/
* http://ufldl.stanford.edu/tutorial/supervised/SoftmaxRegression/
* https://medium.com/samkirkiles/reinforce-policy-gradients-from-scratch-in-numpy-6a09ae0dfe12
* https://machinelearningmastery.com/softmax-activation-function-with-python/.
* https://towardsdatascience.com/githubs-path-to-128m-public-repositories-f6f656ab56b1