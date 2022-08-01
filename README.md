# geolt

## pre-commit setup
This project uses pre-commit to help enforce best practices. To install pre-commit use pip:
```console
pip install pre-commit
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
