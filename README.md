## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Algorithm](#algorithm)
* [Setup](#setup)
* [References](#references)

## General info
The overall objective of gitscrap is to navigate github using its public API in such a way as to discover as many well ranked repositories as possible. The algorithm will rely on Reinforcement learning with policy gradients techniques.

## Technologies
This project is developped in Python 3.9 and requires a Progress SQL server to persist KPI on GitHub repositories and users. it uses the following libraries:
* psycopg2 to connect to progress SQL
* numpy to perform the linear operations required by the machine learning algorithm
* requests to connect to GitHub API

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

In parallel a reporting engine will task GitScrap to regularly process the top N repositories sorted by rank so that to build reliable evolution statistics on the pool of the best ranked repositories. User KPIs are also collected by the algorithm.

The algorithm will first be implemented without reinforcement learning while assigning fixed probabilities to each action independently of the state of the system. Even a non-IA improved walk through GitHub might prove efficient enough to achieve the overall goal: monitor efficiently the best ranked repositories of GitHub. 

## Setup
GitScrapt consists of the following components:
* Class GitRepositories: Allows to fetch and persits the main attributes of a repository object in GitHub
* Class GitUser: Allows to fetch and persits the main attributes of a repository user in GitHub
* A module with connections functions to connect to GitHub API and Progress SQL server.
* A module with the reinforced learning algorithms
* A module to organise GitScrap testing.

To connect to gitHub you need to get an API token from your GitHub account such as token="ghp_xUiJ0LRNJYL34t6xhsGbtU7n155IvL1Z0aUZ"

The .env files in the root repository is used to stored passwords and API key so that they are not published on GitHub:

DATABASE_IP="10.28.0.3"

DATABASE_NAME="gitscrap"

DATABASE_USER="scraping"

DATABASE_PASSWORD="..."

GITHUB_USER="..."

GITHUB_API_KEY="..."

## References
* https://www.janisklaise.com/post/rl-policy-gradients/
* http://ufldl.stanford.edu/tutorial/supervised/SoftmaxRegression/
* https://medium.com/samkirkiles/reinforce-policy-gradients-from-scratch-in-numpy-6a09ae0dfe12
* https://machinelearningmastery.com/softmax-activation-function-with-python/ .