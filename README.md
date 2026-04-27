### Quickfix

QuickFix

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app quickfix
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/quickfix
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.


### License

mit

### Answer the Questions

Section-A2

1. what each config file is for, and what breaks if you accidentally put a secret in common_site_config.json
        site_config.json - Each site have the site_config.json file. it contains the details about the  site such as the db name, db password and etc.

        If you accidentally put a secret like API key in common_site_config.json, it becomes accessible for the all sites

2. list the 4 processes bench start launches (web, worker, scheduler, socketio) and explain what happens to background jobs if the worker process crashes.

        The 4 processes are web.1, socketio.1, schedule.1, and worker.1

        If the worker process crashes, then background jobs are queued