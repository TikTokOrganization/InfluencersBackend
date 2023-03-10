# InfluencersBackEnd  

## For Developers  
### Setting up dev environment
First, make sure you have the latest version of python installed, from this [link](https://www.python.org/). Ensure that the default package manager `pip` is included in the installation.  
Next, clone the repository by running `git clone https://github.com/TikTokOrganization/InfluencersBackend.git`  
After the repository is cloned, make sure you can inside the root folder of the repository and run the `pip install -r requirements.txt` to install all dependencies required for the project.  
You are all set!

### Best Practices 
When dealing with APIs on client-side software, ***never*** include API keys when pushing. The repository is public and anyone can see this information.  

Most of your development work should not take place in `dev` and **never** in `main`. Instead, switch to `dev` and pull all latest changes by running `git pull`.  
Then, checkout a new branch with `git checkout -b [brach name]`.  
Suggestions for branch names:
 - If it is a new feature, the branch name can be `feature/[unique-id]/[small phrase describing feauture]`. The Unique ID is just a combination of numbers that will be generated by Jira to link issues to git branches. The small phrase should be succint and define what the feature accomplishes. For example, if you are implementing a login form, your branch name can be `feature/1AHD92E0Q8/Login-Form`. Since spaces cannot be included in branch names, subsitute them with hypens instead. 
 - If you are testing or trying out a completely new idea, create a proof-of-concept branch that can be called `poc/[unique-id][description]`
 - When fixing a bug, pull all latest changes from `dev` and then name your branch `bug/[unique-id][description]`
 - Special case: sometimes, bugs can make it past code checks and be pulled into `dev` and then `main`. To fix these issues as fast as possible, checkout a hotfix branch directly from main that is intended to fix the issue as quickly as possible. You can name these `hotfix/[unique-id][description]`. Since these branches would be directly pulled into `main`, they require more code reviews to make sure no erroneous code is added.   

### Pushing and Merge Requests  
Stage all changes that you wish to commit by running `git add [files to be staged]`  
Then, commit them by running `git commit -m [Your name: small description of what you did]`  
Once your changes have been committed, push them by running `git push`  

When submitting a pull request (PR), a code review from at least 2 developers will need to be submitted, as well as all unit and integration tests passing as well. An auto-formatter and linter will also be run on your code as well to maintain consistency. Once all checks and code reviews have been performed, you will be able to merge your changes.  
