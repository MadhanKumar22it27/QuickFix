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

Section - B1

Step 1 - Routing (write answers in README.md):
```
1. When a browser hits /api/method/quickfix.api.get_job_summary - what Python function handles this request and how does Frappe find it?

        When a browser hits /api/method/quickfix.api.get_job_summary, handler function handles this request.
        first, split the method path. when it see api/method, then it goes to handler.handle(). it imports the api/get_job_summary

2. When a browser hits /api/resource/Job Card/JC-2024-0001 - what happens differently compared to /api/method/?

        When a browser hits /api/resource/Job Card/JC-2024-0001, same handler handles this request but unlike api/method, it goes to REST resource handler. it doesn't require any whitelist method like api/method. api/resourse is working only on DocTypes.

3. When a browser hits /track-job - which file/function handles it and why?

        When a browser hits /track-job, it actually a website, not an API, so it has been handle by the router and website renderer. it checks whether the files are present inside the www folder and fetch the content using the get_context() and renders jinja HTML

```
Step 2 - Session & CSRF (write answers in README.md):
```
1. Open your Frappe site in browser devtools. Find the X-Frappe-CSRF-Token in a POST request. Where does this value come from and what would happen if you omitted it?

        X-Frappe-CSRF-Token is generated for the session and it stored in the cache or frappe.local. if you omitted it, post request was rejected and it throws a CSRF Validation error. it mainly  used for prevent the malicious user to make request for logged-in users.

2. In bench console, run: import frappe; frappe.session.data and describe what it contains

        frappe.session.data contains the data about the logged-in user details such as the user, user type, session id, role and login time.
```
Step 3 - Error visibility (write answers in README.md):
```
1. With developer_mode: 1 - trigger a Python exception in one of your whitelisted methods. What does the browser receive?

        it shows a full traceback which includes line number and file name. it really useful for the developer to easy to debug

2. Set developer_mode: 0 - repeat. What does the browser receive now? Why is this important for production?

        it shows generic error for the user and actual error goes to server log and error doctype. this is important for production because if the full traceback shows, it might reveals the secret and it leads to security risks

3. Where do production errors go if they are hidden from the browser?

        it remains stay in the error doctype which stores the error logs
```
Step 4 - Permission check location:
```
1. In a whitelisted method, call frappe.get_doc("Job Card", name) WITHOUT ignore_permissions. Then log in as a QF Technician user who is NOT assigned to that job. What error is raised and at what layer does Frappe stop the request?

        frappe.permissionError is raised in this situation and Frappe does stop the request at the frappe.model.Document.get_doc. normally permission is enforced in the data accesss layer.
```

Section - B2

Part A - Table naming (bench console, write output in README_internals.md):
```
1. Run: frappe.db.sql("SHOW TABLES LIKE '%Job%'") and list what you see. Explain the tab prefix convention

        In [2]: frappe.db.sql("SHOW TABLES LIKE '%Job%'")
        Out[2]: (('tabJob Card',), ('tabScheduled Job Log',), ('tabScheduled Job Type',))
        table name for the DocType should be "tab" and followed by the doctype name
        example: "Job Card - tabJob Card"

2. Run: frappe.db.sql("DESCRIBE `tabJob Card`", as_dict=True) and list 5 column names you recognise from your DocType fields.

        In [1]: frappe.db.sql("describe `tabJob Card`",as_dict=True)
        Out[1]: 
                [{'Field': 'name',
                'Type': 'varchar(140)',
                'Null': 'NO',
                'Key': 'PRI',
                'Default': None,
                'Extra': ''},
                {'Field': 'creation',
                'Type': 'datetime(6)',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'modified',
                'Type': 'datetime(6)',
                'Null': 'YES',
                'Key': 'MUL',
                'Default': None,
                'Extra': ''},
                {'Field': 'modified_by',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'owner',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'docstatus',
                'Type': 'int(1)',
                'Null': 'NO',
                'Key': '',
                'Default': '0',
                'Extra': ''},
                {'Field': 'idx',
                'Type': 'int(8)',
                'Null': 'NO',
                'Key': '',
                'Default': '0',
                'Extra': ''},
                {'Field': 'amended_from',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': 'MUL',
                'Default': None,
                'Extra': ''},
                {'Field': '_user_tags',
                'Type': 'text',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': '_comments',
                'Type': 'text',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': '_assign',
                'Type': 'text',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': '_liked_by',
                'Type': 'text',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'customer_name',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'customer_phone',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'customer_email',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'device_type',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'device_brand',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'imei_or_serial',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'problem_description',
                'Type': 'longtext',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'assigned_technician',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'diagonsis_notes',
                'Type': 'longtext',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'estimated_cost',
                'Type': 'decimal(21,9)',
                'Null': 'NO',
                'Key': '',
                'Default': '0.000000000',
                'Extra': ''},
                {'Field': 'diagnosis_date',
                'Type': 'date',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'priority',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': 'Normal',
                'Extra': ''},
                {'Field': 'parts_total',
                'Type': 'decimal(21,9)',
                'Null': 'NO',
                'Key': '',
                'Default': '0.000000000',
                'Extra': ''},
                {'Field': 'labour_charge',
                'Type': 'decimal(21,9)',
                'Null': 'NO',
                'Key': '',
                'Default': '0.000000000',
                'Extra': ''},
                {'Field': 'setting_link',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'final_amount',
                'Type': 'decimal(21,9)',
                'Null': 'NO',
                'Key': '',
                'Default': '0.000000000',
                'Extra': ''},
                {'Field': 'payment_status',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': 'Unpaid',
                'Extra': ''},
                {'Field': 'delivery_date',
                'Type': 'date',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'remarks',
                'Type': 'text',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'status',
                'Type': 'varchar(140)',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''},
                {'Field': 'diagnosis_notes',
                'Type': 'longtext',
                'Null': 'YES',
                'Key': '',
                'Default': None,
                'Extra': ''}]
```
Part D - DocStatus transitions (write answers in README_internals.md):
```
1. What are the three numeric values of docstatus and what state does each represent?

        The Three numeric values are 0, 1, and 2
        0 represents draft state
        1 represents submitted state
        2 represents cancelled state

2. Can you call doc.save() on a submitted document? What about doc.submit() on a cancelled one? Test in bench console and explain why.


        No, We cannot call doc.save() on a submitted document because when you change anything on submitted and try to call the save(), it throws an error called frappe.exceptions.ValidationError: Cannot edit submitted document
        No, We cannot call doc.submit() on a cancelled document because when you try to submit the cancelled document, you will get an error called frappe.exceptions.ValidationError: Cannot submit cancelled document

        Frappe strictly follow the document life cycle 
        (Draft(1) --> Submitted(1) --> Cancelled(2)). there is no back flow.

3. Why would you see a "Document has been modified after you have opened it" error and how does Frappe prevent concurrent overwrites?

        "Document has been modified after you have opened it" error can be thrown in the certain situations like
                1. two user open the same document at the same time
                2. a user try to save the other user's older version
        We can be prevent this by concurrency control like instead of lock the document, track the timestamp(modified) and validate it before saves
```
Part E - Dangerous patterns (identify and fix):
```
1.The following snippet has TWO bugs related to document lifecycle. Identify both and write
the corrected version:
def validate(self):
 self.total = sum(r.amount for r in self.items)
 self.save()
 other = frappe.get_doc("Spare Part", self.part)
 other.stock_qty -= self.qty
 other.save()

        First bug: self.save() inside the validate function because if we execute like this, it might led to recursion (infinity cycle)
        Second bug: other.save() other then self because if we execute like this, it should triggers the entire lifecycle

        def validate(self):
         self.total = sum(r.amount for r in self.items)

         other = frappe.get_doc("Spare Part", self.part)
         other.stock_qty -= self.qty
         other.db_update()
```