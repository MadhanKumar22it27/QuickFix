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

Section - A2

```
1. what each config file is for, and what breaks if you accidentally put a secret in common_site_config.json
        site_config.json - Each site have the site_config.json file. it contains the details about the  site such as the db name, db password and etc.

        If you accidentally put a secret like API key in common_site_config.json, it becomes accessible for the all sites

2. list the 4 processes bench start launches (web, worker, scheduler, socketio) and explain what happens to background jobs if the worker process crashes.

        The 4 processes are web.1, socketio.1, schedule.1, and worker.1

        If the worker process crashes, then background jobs are queued
```

Section - C1

```
1. When you append a row to Job Card.parts_used and save, what 4 columns does Frappe automatically set on the child table row?

        The 4 columns are
                parent - parent doc name
                parent type - parent DocType
                parent field - field name
                idx - order of the row

2. What is the DB table name for the Part Usage Entry DocType?

        The DB table name for the Part Usage Entry DocType is tabPart Usage Entry.

3. If you delete row at idx=2 and re-save, what happens to idx values of remaining rows?

        when we delete a row at idx=2 and resave, it automatically resequenced like (1, 2)
```

Section - C3

```
1. Rename one of your test Technician records using the Rename Document feature. Then check: does the assigned_technician field on linked Job Cards automatically update? Why or why not? What does "track changes" mean in this context?

        Yes, It does update the assigned_technician field on linked job cards when rename the record of technician because frappe maintains the link integrity. rename can't break that. In this Context, Track Changes means monitor and display the changes occur in the field such as old name to new name.

2. Explain unique constraints: what is the difference between setting a field as "unique" in the DocType vs doing a frappe.db.exists() check in validate()?

        Unique Constraints - it used to ensures that no two documents have same data.

        setting a field as "unique" means it enforce the unique constraints in the Database level. In DB, index was created for UNIQUE so, even two users try enter the same data on the same time, it won't allow.
        frappe.db.exists() in validate() means it enforce the unique constraints in the App level. unlike setting a unique field property, it can't prevent the two users put the same data on the same time.
```