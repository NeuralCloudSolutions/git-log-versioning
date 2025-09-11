# Git Log Versioning

This python script is used to create a Word Document that logs all commits and versions from a given GitHub repository and branch.

### Setup

You will need to have Python installed and pip.

```
git clone https://github.com/NeuralCloudSolutions/git-log-versioning.git
cd git-log-versioning
pip install -r requirements.txt
```

### Generating Logs

```
python generate_logs.py --path path/to/local/repo/directory
```

By default the branch used is `main`, but this can be changed with the following:

```
python generate_logs.py --path path/to/local/repo/directory --branch name_of_desired_branch
```