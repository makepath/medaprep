# geolt

## pre-commit setup
This project uses pre-commit, isort, black, and flake8 to help enforce best practices. These libraries are all included in `requirements-dev.txt` and can be installed with pip by running:
```console
pip install -r requirements-dev.txt
```
Once pre-commit is installed, install the hooks specified by the config file into .git:
```console
pre-commit install
```
You can then test pre-commit by running:
```console
pre-commit
```

pre-commit will now run the configured actions as git hooks specified in `.pre-commit-config.yaml`
