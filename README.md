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
### Pure random trajectories 
In this case the algorithm moves from repositories to repositories using fixed and predetermined probabilities to decide between each of the seven possible actions.

In average GitScrap discovers 0.28 repositories each second which is not enough to cover the current growth rate of GitHub. An hourly pattern can be observed on the discovery speed. It corresponds to an improvable method to account for GitHub API speed limitation. 

As a reference, the average score of a pool of 30 Open Source repositories with successful commercial extensions is 4.16 (as compared with 1.72 for a random selection of repositories). When randomly selected 2.3% (est. 650000 public repositories) of the repositories have a score greater than 4. Even if the reinforced learning algorithm would only pick repositories with a score greater than 4 it would take him 6 months to inventory 90% of them.

![alt text](https://github.com/Yvelo/gitscrap/blob/main/rds_any_score_1.png?raw=true)

When we focus on the discovery of repositories with a score greater than 3 there are no indications of non-random bias in the discovery process. 

![alt text](https://github.com/Yvelo/gitscrap/blob/main/rds_score_gt_3.png?raw=true)

Modifying the set of action probabilities does not seem to have an observable impact on the discovery speed.The increase of the stack size form 100 to 1000 doesn't either seem to increase the algorithm velocity.

![alt text](https://github.com/Yvelo/gitscrap/blob/main/rds_any_score_2.png?raw=true)

List of 15 repositories with scores greater than 5 found in 11 hours of scraping:
* ant-design/ant-design
* atralice/Curso.Prep.Henry
* bailicangdu/vue2-elm
* BVLC/caffe
* EbookFoundation/free-programming-books
* facebook/create-react-app
* geekcomputers/Python
* github/docs
* golang/go
* jwasham/coding-interview-university
* microsoft/vscode
* nightscout/cgm-remote-monitor
* scikit-learn/scikit-learn
* tensorflow/tensorflow
* vinta/awesome-python


### Reinforced learning trajectories

## References
* https://www.janisklaise.com/post/rl-policy-gradients/
* http://ufldl.stanford.edu/tutorial/supervised/SoftmaxRegression/
* https://medium.com/samkirkiles/reinforce-policy-gradients-from-scratch-in-numpy-6a09ae0dfe12
* https://machinelearningmastery.com/softmax-activation-function-with-python/.
* https://towardsdatascience.com/githubs-path-to-128m-public-repositories-f6f656ab56b1