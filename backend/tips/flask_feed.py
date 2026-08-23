TIPS = [
    {
        "id": 1,
        "title": "A minimal Flask app",
        "definition": "A Flask() instance, a route decorator and a return value are everything a web endpoint needs. Middleware, ORMs, templates and auth are all opt-in — Flask stays small by design. From zero to a running server takes three lines and one command, which is why it is the classic choice for quick tools and small services.",
        "example": "from flask import Flask\n\napp = Flask(__name__)\n\n@app.get(\"/\")\ndef home():\n    return \"Hello, Flask!\"\n\napp.run(debug=True)   # http://127.0.0.1:5000",
        "usecase": "Spinning up an instant web UI or API for a standalone script, an internal dashboard, or a hackathon demo — with no framework boilerplate to strip out later.",
        "category": "flask"
    },
    {
        "id": 2,
        "title": "Route methods",
        "definition": "By default a route answers GET only; the methods argument declares which HTTP verbs it accepts. methods=[\"GET\", \"POST\"] lets one endpoint render a form and receive its submission, keeping the URL surface small while the same function handles both phases.",
        "example": "@app.route(\"/submit\", methods=[\"GET\", \"POST\"])\ndef submit():\n    if request.method == \"POST\":\n        save_form(request.form)\n        return redirect(url_for(\"done\"))\n    return render_template(\"submit.html\")",
        "usecase": "One endpoint serving both the form page (GET) and its submission (POST) — the classic pairing that avoids a second URL and a second function.",
        "category": "flask"
    },
    {
        "id": 3,
        "title": "url_for() reverses routes",
        "definition": "url_for('home') builds the URL for a named endpoint instead of hardcoding paths. Because the generated URLs always match the current routing table, moving a route updates every link that points at it automatically. Optional keyword arguments become path or query parameters.",
        "example": "from flask import url_for\n\nurl = url_for(\"home\")                    # '/'\nurl = url_for(\"profile\", username=\"ada\")  # '/u/ada'",
        "usecase": "Redirecting after a form save or generating nav links that stay correct when routes move — one rename never breaks a dozen templates.",
        "category": "flask"
    },
    {
        "id": 4,
        "title": "Jinja2 templates",
        "definition": "render_template() loads a Jinja2 template and injects the variables you pass as context. Templates combine HTML with a small, sandboxed language — loops, conditionals and includes — so page structure lives beside the markup while logic stays in the view.",
        "example": "from flask import render_template\n\ndef home():\n    return render_template(\"index.html\", user=current_user, posts=latest_posts())",
        "usecase": "Serving HTML pages driven by data — loops, conditionals and shared layout live in templates, and the Python stays free of markup strings.",
        "category": "flask"
    },
    {
        "id": 5,
        "title": "Template variables & filters",
        "definition": "{{ var }} prints a value and |filters transform it inline — title-casing a name, formatting a date, taking the length of a list. Filters keep display formatting out of Python, so views stay about data and templates own the presentation.",
        "example": "<p>{{ user.name|title }} — {{ posts|length }} posts</p>\n<p>Joined {{ user.created_at|date('%Y-%m-%d') }}</p>",
        "usecase": "Displaying names, counts and dates without helper functions in every view — one filter changes the whole site's formatting with a template edit.",
        "category": "flask"
    },
    {
        "id": 6,
        "title": "Static files built-in",
        "definition": "Files placed in a static/ folder are served automatically at /static, and url_for('static', ...) produces the correct URL for them. CSS, JavaScript and images ship with zero routing code, and the URL can point at a CDN later without touching the templates.",
        "example": "<link rel=\"stylesheet\" href=\"{{ url_for('static', filename='css/app.css') }}\">\n<script src=\"{{ url_for('static', filename='js/app.js') }}\" defer></script>",
        "usecase": "CSS, JS and images delivered on every page without wiring a single route by hand — and assets keep working when the app is deployed behind a CDN.",
        "category": "flask"
    },
    {
        "id": 7,
        "title": "Read form data",
        "definition": "request.form holds POSTed form fields as a MultiDict, and request.args holds query string values — both with a .get() that accepts a default. Reading user input this way is safe rows of boilerplate shorter than parsing the raw body yourself.",
        "example": "from flask import request\n\nname = request.form.get(\"name\", \"anonymous\")   # <form> fields\npage = request.args.get(\"page\", 1, type=int)  # ?page=2",
        "usecase": "Search boxes, login forms and settings forms — grabbing submitted values with sane defaults instead of KeyError-catching your way through every field.",
        "category": "flask"
    },
    {
        "id": 8,
        "title": "JSON in and out",
        "definition": "request.get_json() parses a JSON request body into Python structures, and jsonify() serializes a dict or list into a proper JSON response with the right Content-Type. Together they turn Flask into a small JSON API without any REST framework.",
        "example": "from flask import request, jsonify\n\ndata = request.get_json()\nreturn jsonify({\"ok\": True, \"received\": data}",
        "usecase": "A lightweight JSON API for SPAs, cron jobs or sensors — response shapes and status codes are yours to decide with no framework opinions.",
        "category": "flask"
    },
    {
        "id": 9,
        "title": "Redirects and aborts",
        "definition": "redirect() sends a 3xx response that moves the browser to another URL, and abort(status) stops the request by raising an error the handler can catch. Combining them gives you the two bread-and-butter controls every web app needs: send them somewhere, or refuse.",
        "example": "from flask import redirect, url_for, abort\n\nif not user:\n    abort(404)                      # bail out cleanly\nif not user.is_authenticated:\n    return redirect(url_for(\"login\"))  # send them to auth",
        "usecase": "Guarding endpoints, sending guests to login, or cutting off a request with a clean 404 — two functions instead of hand-rolling response codes.",
        "category": "flask"
    },
    {
        "id": 10,
        "title": "URL converters",
        "definition": "Angle-bracket segments in routes type-convert URL parts before your view runs: <int:user_id> guarantees an integer, <float:x> a float, and <path:rest> captures slashes. Validation happens at routing time, so your function receives clean, typed arguments.",
        "example": "@app.get(\"/users/<int:user_id>/<path:slug>\")\ndef user(user_id, slug):\n    # user_id is already an int, slug can contain slashes\n    ...",
        "usecase": "Clean, readable URLs with validation and coercion built in — no manual string-to-int parsing, and non-numeric IDs simply 404 instead of crashing.",
        "category": "flask"
    },
    {
        "id": 11,
        "title": "Config through app.config",
        "definition": "app.config is a plain dict for application settings, loaded at startup from a class, dict, object or file via from_mapping()/from_object(). All knobs — database URIs, upload limits, secret keys — live in one place rather than as scattered module globals.",
        "example": "app.config.from_mapping(\n    SECRET_KEY=\"dev-secret\",\n    MAX_CONTENT_LENGTH=16 * 1024 * 1024,\n    DATABASE=\"sqlite:///app.db\",\n)",
        "usecase": "A central home for DB URIs, upload limits and feature flags — swap environments by swapping config objects instead of hunting globals.",
        "category": "flask"
    },
    {
        "id": 12,
        "title": "Blueprints organize routes",
        "definition": "A Blueprint groups routes, templates and static files under a name and URL prefix, then registers onto the app like a mini-application. As projects grow, blueprints per feature — auth, admin, api — keep every module self-contained and the route table readable.",
        "example": "from flask import Blueprint\n\nbp = Blueprint(\"blog\", __name__, url_prefix=\"/blog\")\n\n@bp.get(\"/\")\ndef index():\n    return \"Blog home\"\n\napp.register_blueprint(bp)",
        "usecase": "Keeping auth, admin and API routes in their own modules as the project grows — new features slot in without touching the routing of the rest.",
        "category": "flask"
    },
    {
        "id": 13,
        "title": "App factory pattern",
        "definition": "A create_app() function builds and returns a configured Flask instance — the app object stops being a global and becomes a product of configuration. Tests get throwaway instances, and environments like 'dev' or 'prod' become arguments, not constants.",
        "example": "def create_app(config_name=\"dev\"):\n    app = Flask(__name__)\n    app.config.from_object(APP_CONFIGS[config_name])\n    db.init_app(app)\n    app.register_blueprint(main_bp)\n    return app\n\napp = create_app()",
        "usecase": "Running tests against a fresh app per test and multiple environments from one codebase — the pattern every serious Flask tutorial ends with.",
        "category": "flask"
    },
    {
        "id": 14,
        "title": "g for per-request data",
        "definition": "flask.g is a per-request namespace for storing whatever the request needs — a database connection, a cached user, a start timestamp. It lives and dies with the request, so it never leaks data between requests and needs no manual cleanup beyond a teardown hook.",
        "example": "from flask import g\n\ndef get_db():\n    if \"db\" not in g:\n        g.db = connect()\n    return g.db\n# later: rows = get_db().query(\"SELECT * FROM posts\")",
        "usecase": "Opening one database handle per request and reusing it across every helper — no globals, no connection per function call, and it closes with the request.",
        "category": "flask"
    },
    {
        "id": 15,
        "title": "Hooks before/after request",
        "definition": "before_request runs once before every view, and after_request tweaks every response on the way out. Anything that applies to all requests — auth checks, DB setup, security headers, timing — is written once here instead of repeated in each view.",
        "example": "@app.before_request\ndef load_user():\n    g.user = fetch_current_user()\n\n@app.after_request\ndef add_headers(response):\n    response.headers[\"X-Content-Type-Options\"] = \"nosniff\"\n    return response",
        "usecase": "Auth checks, DB setup, security headers and request timing applied to every route in one place — add a header and the whole site gets it.",
        "category": "flask"
    },
    {
        "id": 16,
        "title": "Custom error pages",
        "definition": "@app.errorhandler(404) (or any status or exception type) runs whenever that error occurs and returns your own page instead of the default. Errors become a designed part of the product rather than a jarring raw text screen.",
        "example": "@app.errorhandler(404)\ndef not_found(e):\n    return render_template(\"404.html\", requested=request.path), 404",
        "usecase": "Friendly, branded 404 and 500 pages with your navigation and styling — visitors get a helpful dead end instead of a bare error.",
        "category": "flask"
    },
    {
        "id": 17,
        "title": "Flash messages",
        "definition": "flash() queues a one-shot message that appears on the next rendered page via get_flashed_messages(). It's the standard companion to redirects: save the data, redirect, and show 'Saved!' on the destination — the post-redirect-get feedback loop.",
        "example": "from flask import flash, redirect, url_for, render_template\n\nflash(\"Account created!\", \"success\")\nreturn redirect(url_for(\"home\"))\n\n# in a template:\n{% for msg in get_flashed_messages() %}<div class=\"alert\">{{ msg }}</div>{% endfor %}",
        "usecase": "Saved/created/error notices after form submissions — exactly one message, shown exactly once, on the page the user lands on next.",
        "category": "flask"
    },
    {
        "id": 18,
        "title": "Sessions that 'just work'",
        "definition": "Flask sessions are signed cookies: you set session[key], and Flask serializes, signs and stores it in the browser; on the next request it's deserialized and verified. No server-side storage to configure — data follows the user across requests automatically.",
        "example": "from flask import session\n\nsession[\"user_id\"] = user.id          # store on login\n\n# next request:\nuid = session.get(\"user_id\")          # read it back\nsession.clear()                        # logout",
        "usecase": "Keeping users logged in and remembering preferences without running a session store — the cookie holds the state, signed so clients can't tamper with it.",
        "category": "flask"
    },
    {
        "id": 19,
        "title": "Set and read cookies",
        "definition": "response.set_cookie() stores a cookie on the client, and request.cookies reads them back on later requests, both with optional expiry via max_age. Cookies are lightweight, per-site state that survives page reloads — perfect for preferences that should persist without a login.",
        "example": "from flask import make_response, render_template, request\n\nresp = make_response(render_template('index.html'))\nresp.set_cookie('lang', 'en', max_age=60 * 60 * 24)   # 1 day\nreturn resp\n\n# next request:\nlang = request.cookies.get('lang', 'en')",
        "usecase": "Remembering language choice, theme or a dismiss-in-banner flag across visits — persisted in the browser with no server-side store to maintain.",
        "category": "flask"
    },
    {
        "id": 20,
        "title": "File uploads",
        "definition": "request.files exposes uploaded files as FileStorage objects with a .filename and a .save() method. Flask handles the multipart parsing, so a single route can accept avatars, CSVs or attachments — the file streams from the request straight to disk.",
        "example": "from flask import request\n\nf = request.files['avatar']\nf.save(f'uploads/{f.filename}')   # streams to disk\n\n# safer: use werkzeug.utils.secure_filename(f.filename) to sanitize",
        "usecase": "Avatar uploads, CSV imports and attachment handling with one import-free flow — no manual multipart parsing, and big files stream instead of loading into memory.",
        "category": "flask"
    },
    {
        "id": 21,
        "title": "Downloads with send_file",
        "definition": "send_file() streams a local file — or an in-memory BytesIO — to the client as a download, setting Content-Type and Content-Disposition for you. Generation can happen in memory and the file is piped out in chunks, so exports never need the whole blob in RAM at once.",
        "example": "from flask import send_file\nfrom io import BytesIO\n\ncsv_bytes = build_csv(data)          # in-memory bytes\nreturn send_file(BytesIO(csv_bytes), as_attachment=True, download_name='report.csv')",
        "usecase": "Exporting CSVs and PDFs from generated or stored files for thousands of rows — streamed to the browser without loading the entire payload into memory.",
        "category": "flask"
    },
    {
        "id": 22,
        "title": "Logging for free",
        "definition": "app.logger is a full Python logging logger pre-wired into the Flask context: levels, timestamps and formatting come configured, and the same calls work in dev and production. One call per event replaces scattered print() with searchable, leveled log lines.",
        "example": "app.logger.info('user %s signed up', user.id)\napp.logger.warning('retry 2 for order %s', order.id)\napp.logger.error('payment failed: %s', err, exc_info=True)",
        "usecase": "Tracing requests through logs after the fact instead of hunting for print output — levels keep debug noise out of production and errors land in your log sink.",
        "category": "flask"
    },
    {
        "id": 23,
        "title": "SQLite without an ORM",
        "definition": "Python's built-in sqlite3 module gives Flask apps a real relational database with zero dependencies. A connection, an execute and fetchall() cover most small-tool needs — and parameterized queries keep the same injection safety you'd get from any ORM.",
        "example": "import sqlite3\n\nconn = sqlite3.connect('app.db')\nrows = conn.execute(\n    'SELECT * FROM posts WHERE published = ?', (1,)\n).fetchall()",
        "usecase": "Prototypes and internal tools that need genuine queries and persistence but no install step — sqlite is always there and the file IS the database.",
        "category": "flask"
    },
    {
        "id": 24,
        "title": "Flask-SQLAlchemy setup",
        "definition": "Flask-SQLAlchemy binds the SQLAlchemy ORM to your app config: one db object, models subclassing db.Model, and queries through db.session. It handles connections per request and keeps models, relationships and queries Pythonic rather than raw SQL.",
        "example": "from flask_sqlalchemy import SQLAlchemy\nfrom flask import Flask\n\napp = Flask(__name__)\napp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'\ndb = SQLAlchemy(app)\n\nclass Post(db.Model):\n    id = db.Column(db.Integer, primary_key=True)\n    title = db.Column(db.String(200), nullable=False)",
        "usecase": "Real apps needing ORM queries, relationships and migrations on top of Flask — declare models in Python and let the ORM handle tables and sessions.",
        "category": "flask"
    },
    {
        "id": 25,
        "title": "Schema migrations with Flask-Migrate",
        "definition": "Flask-Migrate wraps Alembic so schema changes are recorded as migration files and applied with commands. You evolve tables — add columns, rename fields — the same safe, reviewable way every time, without dropping data to rebuild a table.",
        "example": "flask db init\nflask db migrate -m 'add posts table'\nflask db upgrade",
        "usecase": "Tweaking tables in production safely instead of clearing data and re-creating them — migrations replay the same history in dev, staging and prod.",
        "category": "flask"
    },
    {
        "id": 26,
        "title": "Form validation with WTForms",
        "definition": "WTForms (via Flask-WTF) declares a form as fields with validators — required, email, length — and renders them into HTML with CSRF protection built in. On an invalid submit it re-renders with per-field errors, so validation UI stays consistent across the whole app.",
        "example": "from flask_wtf import FlaskForm\nfrom wtforms import StringField, PasswordField, validators\n\nclass LoginForm(FlaskForm):\n    email = StringField('Email', [validators.Email()])\n    password = PasswordField('Password', [validators.Length(min=8)])",
        "usecase": "Login, signup and settings forms with CSRF protection, required/email/length checks and a consistent error UI — declared once, rendered and validated everywhere.",
        "category": "flask"
    },
    {
        "id": 27,
        "title": "jsonify for API responses",
        "definition": "jsonify() serializes a dict or list into a proper JSON response — correct Content-Type and escaping — instead of a bare string you'd have to format yourself. Small JSON APIs on Flask return jsonify() and go, with status codes passed as a second return value.",
        "example": "from flask import jsonify\n\n@app.get('/api/stats')\ndef stats():\n    return jsonify({'status': 'ok', 'items': items}), 200",
        "usecase": "Small JSON endpoints for dashboards, gadgets and script consumers — you own the response shape, and jsonify() guarantees it's valid JSON with the right headers.",
        "category": "flask"
    },
    {
        "id": 28,
        "title": "Test the whole app with test_client",
        "definition": "app.test_client() runs requests against your app in-process, with no server or network — cookies, redirects and the full routing stack all behave as if real. It turns the whole app into a testable unit, right down to asserting status codes and rendered content.",
        "example": "client = app.test_client()\n\nresp = client.get('/')\nassert resp.status_code == 200\nassert b'Hello' in resp.data\n\nresp = client.post('/login', data={'email': 'a@b.c', 'password': 'x'})\nassert resp.status_code == 302   # redirect after submit",
        "usecase": "CI smoke tests verifying routes, redirects and forms before every deploy — the fastest way to catch broken links or changed behavior in a full-stack test.",
        "category": "flask"
    },
    {
        "id": 29,
        "title": "Debug mode & reloader",
        "definition": "app.run(debug=True) (or FLASK_DEBUG=1 flask run) enables the dev reloader and an interactive traceback in the browser. Change code, save, and the server restarts; when something fails you get a debuggable stack trace with a console instead of a bare error page.",
        "example": "app.run(debug=True)\n# or: FLASK_DEBUG=1 flask run\n# save a file → server reloads automatically → errors show an interactive traceback",
        "usecase": "Development iterations — save, refresh, inspect the failing line right in the browser — with the reloader keeping the loop tight. Never enable debug in production.",
        "category": "flask"
    },
    {
        "id": 30,
        "title": "Settings from the environment",
        "definition": "Reading secrets and URLs from os.environ — or loading .env with python-dotenv — keeps credentials and environment-specific values out of the repository. One codebase then runs anywhere; the environment supplies the differences.",
        "example": "import os\n\napp.config['SECRET_KEY'] = os.environ['SECRET_KEY']\napp.config['DATABASE_URL'] = os.environ.get('DATABASE_URL', 'sqlite:///dev.db')",
        "usecase": "Deploying to multiple machines with different databases and keys from one repo — CI, staging and prod each provide their own environment.",
        "category": "flask"
    },
    {
        "id": 31,
        "title": "Custom CLI commands",
        "definition": "@app.cli.command registers a command on the flask CLI, so one-off jobs — seeding data, importing CSVs, cleanup — ship inside the app instead of as loose scripts. Click arguments make them configurable: flask seed 100, flask import --file x.csv.",
        "example": "import click\nfrom flask.cli import with_appcontext\n\n@app.cli.command('seed')\n@click.argument('n', default=10)\n@with_appcontext\ndef seed(n):\n    for i in range(int(n)):\n        db.session.add(Post(title=f'Post {i}'))\n    db.session.commit()\n    print(f'seeded {n} posts')",
        "usecase": "Running one-off data jobs like flask seed 100 or flask db-clean without writing and maintaining a separate script per task.",
        "category": "flask"
    },
    {
        "id": 32,
        "title": "Stream long responses",
        "definition": "Returning a generator (or async generator) makes Flask stream the response chunk by chunk instead of buffering it fully first. Long exports, log tails and LLM output start reaching the client almost immediately, and memory stays flat no matter how large the total is.",
        "example": "from flask import Response\n\ndef gen():\n    for i in range(100):\n        yield f'line {i}\\n'\nreturn Response(gen(), mimetype='text/plain')",
        "usecase": "Downloading huge reports or streaming incremental data as it's produced — the client sees progress and the server never builds the whole payload in memory.",
        "category": "flask"
    },
    {
        "id": 33,
        "title": "current_app inside blueprints",
        "definition": "current_app is a proxy to the app that owns the current request, accessible anywhere the app context is active — blueprints, helpers, Celery tasks and shell scripts. It gives background code access to config and logging without threading the app object through every call.",
        "example": "from flask import current_app\n\n# inside a Celery task or long-running worker:\ndef send_report():\n    db_url = current_app.config['DATABASE_URL']\n    current_app.logger.info('report job started')",
        "usecase": "Accessing config and loggers from workers and background code that outlive any single request — the app context bridges the gap between HTTP and async work.",
        "category": "flask"
    },
    {
        "id": 34,
        "title": "Cleanup with teardown_appcontext",
        "definition": "teardown_appcontext runs after each request or app-context usage, whether the request succeeded or raised — the reliable place to close database connections and release resources. Because it always runs, connections can't leak even on exceptions.",
        "example": "from flask import g, teardown_appcontext\n\n@teardown_appcontext\ndef close_db(exc):\n    if g.get('db') is not None:\n        g.db.close()   # runs on success AND on errors",
        "usecase": "Guaranteeing connection cleanup even when a request errors mid-flight — the safety net that keeps long-running deployments from exhausting connections.",
        "category": "flask"
    },
    {
        "id": 35,
        "title": "CORS for browser apps",
        "definition": "flask-cors adds the Access-Control-Allow-* headers browsers require before JavaScript from another origin may read responses. One CORS(app) call opens the API to your frontend — with optional fine-grained origin and header rules for production.",
        "example": "from flask_cors import CORS\n\nCORS(app)   # allow all origins\n# or: CORS(app, resources={r'/api/*': {'origins': ['http://localhost:3000']}})",
        "usecase": "A React, Vue or Remix frontend on :3000 fetching from the Flask API on :5000 — without the CORS headers the browser silently blocks every response.",
        "category": "flask"
    },
    {
        "id": 36,
        "title": "Werkzeug password hashing",
        "definition": "Werkzeug's generate_password_hash() creates a salted, one-way hash of a password, and check_password_hash() verifies a candidate against it. You store only the hash — never the plaintext — and verification happens in constant time, which is the correct way to handle credentials.",
        "example": "from werkzeug.security import generate_password_hash, check_password_hash\n\nhashed = generate_password_hash('secret')\n# store hashed\n\nassert check_password_hash(hashed, 'secret')   # True\nassert not check_password_hash(hashed, 'wrong')  # False",
        "usecase": "Storing user passwords safely in any Flask app — the framework ships the hashing so you never invent your own crypto or save plaintext.",
        "category": "flask"
    },
    {
        "id": 37,
        "title": "Routing order matters",
        "definition": "Routes are matched in the order they are defined, and the first match wins. A generic <int:id>, <string:name> or catch-all rule defined first will swallow any more specific literal route you add after it, so specific endpoints must be declared before the patterns they'd otherwise shadow.",
        "example": "@app.get('/post/latest')\ndef latest(): ...        # define BEFORE the <id> route\n\n@app.get('/post/<int:post_id>')\ndef post(post_id): ...  # 'latest' would match here otherwise",
        "usecase": "Avoiding '/post/latest' being swallowed by the '/post/<int:id>' pattern — the classic order bug that turns a literal URL into a 404 or wrong handler.",
        "category": "flask"
    },
    {
        "id": 38,
        "title": "Subdomain routes",
        "definition": "A blueprint (or route) declared with subdomain only matches requests hitting that host subdomain. One app can then serve api.example.com, admin.example.com and www.example.com from distinct code paths — handy for separating API from UI without separate deployments.",
        "example": "from flask import Blueprint\n\napi = Blueprint('api', __name__, subdomain='api')\n\n@api.get('/users')\ndef users():\n    ...\n\napp.register_blueprint(api)   # only on api.example.com",
        "usecase": "Serving api.example.com separately from the main site on one app and one repository — subdomain routing keeps the split organized in code.",
        "category": "flask"
    },
    {
        "id": 39,
        "title": "Custom 404 with templates",
        "definition": "An error handler can render a real template and return it with the status code, turning the default bare 404 into a designed page with your site's navigation and tone. Visitors land on something helpful instead of a wall of plain text.",
        "example": "@app.errorhandler(404)\ndef not_found(e):\n    return render_template('404.html', path=request.path), 404",
        "usecase": "Replacing the generic error page with one that matches your brand — a 404 that offers search or links home converts lost visitors instead of losing them.",
        "category": "flask"
    },
    {
        "id": 40,
        "title": "Max upload size",
        "definition": "MAX_CONTENT_LENGTH caps the size of request bodies, and Flask rejects oversized uploads early with a 413 response. It is the cheap, first line of defense against memory exhaustion from multi-gigabyte uploads hitting a small server.",
        "example": "app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024   # 8 MB\n\n@app.errorhandler(413)\ndef too_large(e):\n    return 'File too large', 413",
        "usecase": "Blocking huge uploads before they allocate memory or fill a disk — set the cap once and 413s protect every upload route automatically.",
        "category": "flask"
    },
    {
        "id": 41,
        "title": "Deploying with gunicorn",
        "definition": "Gunicorn is the production WSGI server for Flask: it runs your app across multiple worker processes behind the same port. Unlike the built-in dev server, it handles real concurrent traffic, and it pairs with nginx or a cloud platform for public deployments.",
        "example": "gunicorn -w 4 -b 0.0.0.0:8000 'app:create_app()'\n# or with a module-level app: gunicorn -w 4 app:app",
        "usecase": "Serving real traffic that would exhaust the threaded dev server — workers give concurrency, and the same app object serves in production untouched.",
        "category": "flask"
    },
    {
        "id": 42,
        "title": "chunks with iter_content pattern",
        "definition": "Proxying a remote file through Flask means fetching it in chunks with a streaming HTTP client and yielding each chunk to the response. Both sides stream, so the payload never exists fully in your memory — a clean pattern for gateways and file pass-throughs.",
        "example": "import requests\nfrom flask import Response\n\ndef proxy(url):\n    r = requests.get(url, stream=True)\n    for chunk in r.iter_content(chunk_size=8192):\n        if chunk:\n            yield chunk\n\nreturn Response(proxy('https://example.com/big.bin'))",
        "usecase": "Proxying large external files — hosting redirects, caching layers, wrappers — without buffering the file twice in memory along the way.",
        "category": "flask"
    },
    {
        "id": 43,
        "title": "JSON sorting — keep it off",
        "definition": "Flask's JSON encoder sorts keys alphabetically by default; JSON_SORT_KEYS=False keeps the insertion order of your dicts in the response. When clients hash, diff or stream responses field-by-field, the order you coded is the order they get.",
        "example": "app.config['JSON_SORT_KEYS'] = False\n\n# now: jsonify({'total': 3, 'items': [...]}) keeps 'total' first",
        "usecase": "APIs where field order matters for hashing, pretty diffs or forward compat — the response reads exactly as the code declares it.",
        "category": "flask"
    },
    {
        "id": 44,
        "title": "Per-request DB with factory + teardown",
        "definition": "The classic Flask pattern: a get_db() factory stores one connection on flask.g per request, and a teardown hook closes it when the request ends. Every handler shares one connection, and cleanup is guaranteed — even on exceptions.",
        "example": "from flask import g\n\ndef get_db():\n    if 'db' not in g:\n        g.db = connect_db()\n    return g.db\n\n@teardown_appcontext\ndef close_db(exc):\n    db = g.pop('db', None)\n    if db is not None:\n        db.close()",
        "usecase": "One connection per request, reused by every handler and closed deterministically — the pattern that keeps connection counts flat under load.",
        "category": "flask"
    },
    {
        "id": 45,
        "title": "Blueprint error handlers",
        "definition": "Blueprints can define their own error handlers, scoped to the routes they own. That lets different parts of the app answer errors differently — the API blueprint returns JSON errors while the UI blueprint returns HTML pages — from one codebase.",
        "example": "@api.errorhandler(404)\ndef api_not_found(e):\n    return jsonify({'error': 'not found'}), 404\n\n@ui.errorhandler(404)\ndef ui_not_found(e):\n    return render_template('404.html'), 404",
        "usecase": "The API module answers with machine-readable errors and the UI module with pretty pages — per-blueprint handlers keep each contract clean.",
        "category": "flask"
    },
    {
        "id": 46,
        "title": "Request context without a request",
        "definition": "app.test_request_context() temporarily creates a request context, letting you use request, session, url_for and current_app outside of an incoming HTTP request. Scripts, email generation and tests all benefit from building URLs and using context the same way views do.",
        "example": "from flask import url_for\n\nwith app.test_request_context('/'):\n    print(url_for('home'))          # '/'\n    print(url_for('profile', username='ada'))  # '/u/ada'",
        "usecase": "Generating URLs in background jobs, notification emails and tests — anywhere you need routing context but no live browser request.",
        "category": "flask"
    },
    {
        "id": 47,
        "title": "Method override via POST",
        "definition": "HTML forms only submit GET and POST natively, yet a RESTful API may expect PUT or DELETE. A hidden _method field in the form records the true verb so the same endpoint can expose REST semantics to plain HTML clients.",
        "example": "<!-- HTML form -->\n<form action=\"/posts/3\" method=\"post\">\n  <input type=\"hidden\" name=\"_method\" value=\"delete\">\n  <button>Delete</button>\n</form>",
        "usecase": "REST endpoints that plain HTML forms can use — a hidden field fakes the verb the browser won't send, keeping one URL per resource.",
        "category": "flask"
    },
    {
        "id": 48,
        "title": "Thread-safety of globals",
        "definition": "request, session and g are context-locals: what they resolve to depends on the current request's context, so concurrent requests each see their own values. A helper that reads request.headers is always reading this request's headers, even under threads.",
        "example": "def helper():\n    return request.headers.get('User-Agent')  # always THIS request's headers\n\n@app.get('/')\ndef home():\n    return helper()  # safe under concurrent traffic",
        "usecase": "Sharing helper functions and utilities across views without leaking data between simultaneous users — context-locals make it safe by design.",
        "category": "flask"
    },
    {
        "id": 49,
        "title": "Blueprint static folders",
        "definition": "Passing static_folder to a Blueprint gives that module its own CSS, JS and images, served under its own static_url_path. Feature assets travel with the feature — the admin module owns its styles instead of dumping them into the global static directory.",
        "example": "from flask import Blueprint\n\nadmin = Blueprint('admin', __name__, url_prefix='/admin',\n                   static_folder='static', static_url_path='/admin/static')\n# → /admin/static/css/admin.css resolves automatically",
        "usecase": "Admin or widget UI assets living beside the module that owns them — self-contained blueprints that drop into any project intact.",
        "category": "flask"
    },
    {
        "id": 50,
        "title": "Signal hookups",
        "definition": "Flask signals (request_started, request_finished, got_request_exception) fire application-wide at lifecycle points and let you attach instrumentation without editing individual views. Because they're built on blinker, any number of subscribers can listen to the same event, which makes them the low-noise way to add cross-cutting behavior.",
        "example": "from flask import got_request_exception, request_started\n\ndef mark_start(sender, **extra):\n    sender.logger.info('request started: %s', request.path)\n\ndef log_exception(sender, exception, **extra):\n    sender.logger.error('exception: %r', exception)\n\nrequest_started.connect(mark_start)\ngot_request_exception.connect(log_exception)",
        "usecase": "Central error and metrics instrumentation — log every exception, measure every request — without touching individual views or rewriting handlers.",
        "category": "flask"
    }
]
