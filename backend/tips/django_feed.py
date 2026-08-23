TIPS = [
    {
        "id": 1,
        "title": "Start a Django project",
        "definition": "django-admin startproject scaffolds a complete, battle-tested project skeleton in one command: settings.py, urls.py, wsgi/asgi entry points and manage.py. From that moment you have a working config that can run a dev server, connect to a database, and grow into a hobby blog or a multi-tenant SaaS backend without touching the plumbing.",
        "example": "django-admin startproject mysite\ncd mysite\npython manage.py runserver\n# open http://127.0.0.1:8000 — the classic rocket is yours",
        "usecase": "Bootstrapping anything from a personal blog to an enterprise SaaS backend — one command gets a production-grade project skeleton with settings, URL routing and an ORM wired up.",
        "category": "django"
    },
    {
        "id": 2,
        "title": "Apps are modules, projects are config",
        "definition": "A Django project holds configuration (settings.py, root urls, wsgi), while each app is a self-contained, swappable module bundling its own models, views, urls and templates. Features live in apps, not files tucked inside the project — that separation is what makes Django projects maintainable at scale.",
        "example": "python manage.py startapp blog\n# then add 'blog' to INSTALLED_APPS in settings.py\n# app has its own models.py, views.py, urls.py, migrations/",
        "usecase": "Keeping features isolated so the same blog or payments app can be reused in the next project untouched — a library inside your project, not spaghetti.",
        "category": "django"
    },
    {
        "id": 3,
        "title": "Models define your DB schema",
        "definition": "A model is a Python class that Django maps to a database table: each field becomes a column, and the ORM handles create, read, update and delete for you. You describe data in Python — relationships, indexes, constraints — and Django generates and applies the SQL through migrations.",
        "example": "from django.db import models\n\nclass Post(models.Model):\n    title = models.CharField(max_length=200)\n    published = models.BooleanField(default=False)\n\npost = Post.objects.create(title=\"Hello\", published=True)",
        "usecase": "Declaring users, orders, posts or inventory as classes, then letting Django generate the SQL and give you a query API — no handwritten DDL or CRUD boilerplate.",
        "category": "django"
    },
    {
        "id": 4,
        "title": "QuerySets are lazy",
        "definition": "Filtering a manager produces a QuerySet without touching the database — the SQL is composed but not executed. The query only runs when you evaluate the QuerySet: iterate it, convert it with list(), take len(), or call aggregates. This laziness lets you build complex queries across functions and pay the database cost exactly once, as late as possible.",
        "example": "qs = Post.objects.filter(published=True)    # no SQL yet\nqs = qs.filter(created_at__gte=start_date)     # still no SQL\nfirst_ten = list(qs[:10])                      # one SQL query, now",
        "usecase": "Composing complex filters across views and passing QuerySets around — the database is hit exactly when the data is needed, not one query per filter line.",
        "category": "django"
    },
    {
        "id": 5,
        "title": "Chain filter and exclude",
        "definition": "Each .filter() narrows a QuerySet and .exclude() drops matches; because every call returns a fresh QuerySet you can chain them in any order to stack criteria. Combined with field lookups like __gt, __icontains and __in, a readable sentence of chained calls becomes a precise SQL WHERE clause.",
        "example": "Post.objects.filter(\n    published=True,\n    title__icontains=\"django\",\n).exclude(author__isnull=True)\n# SQL: WHERE published AND title ILIKE AND author IS NOT NULL",
        "usecase": "Building report dashboards where criteria stack: active users of the last 30 days, orders above a threshold, invoices missing a payer — each filter is one line.",
        "category": "django"
    },
    {
        "id": 6,
        "title": "beat N+1 with select_related",
        "definition": "The N+1 problem hits when you fetch a list of rows and then touch a foreign key on each one — one query per row, on top of the listing query. select_related() folds forward foreign keys into a single JOIN, and prefetch_related() handles reverse and many-to-many relations with a fixed number of extra queries.",
        "example": "Post.objects.select_related(\"author\")       # one JOIN, author loaded\nPost.objects.prefetch_related(\"tags\")       # two queries total\nfor post in Post.objects.all():\n    print(post.author.name)                  # no per-row query",
        "usecase": "List views showing author names or tags — without select_related a 100-row page costs 101+ queries; with it, one or two.",
        "category": "django"
    },
    {
        "id": 7,
        "title": "aggregate vs annotate",
        "definition": "aggregate() reduces an entire QuerySet to a single summary value — one row back, like 'how many orders total'. annotate() instead adds a computed column to every row, so each object carries its own derived value alongside its fields. Picking the right one is the difference between one number and a per-record metric.",
        "example": "from django.db.models import Count, Sum\n\nPost.objects.aggregate(total=Count(\"id\"))        # {'total': 42} — one summary\nPost.objects.annotate(n=Count(\"comments\"))      # each post gains a .n field",
        "usecase": "Stat cards on a dashboard ('total orders', 'revenue this month') use aggregate; listings with per-row counts ('posts and their comment counts') use annotate.",
        "category": "django"
    },
    {
        "id": 8,
        "title": "ModelForm saves boilerplate",
        "definition": "A ModelForm generates form fields, validation and a .save() method straight from a model, so rendering on HTTP forms while staying in sync with the model is automatic. Add clean_<field>() methods for custom validation and you still never hand-write the repetitive per-field form logic.",
        "example": "from django import forms\nfrom .models import Post\n\nclass PostForm(forms.ModelForm):\n    class Meta:\n        model = Post\n        fields = [\"title\", \"published\"]\n\n# in a view:\nform = PostForm(request.POST)\nif form.is_valid():\n    post = form.save()",
        "usecase": "Comment forms, profile editors and admin panels — the form fields, validation and save stay consistent with the model automatically, so a model change updates the form too.",
        "category": "django"
    },
    {
        "id": 9,
        "title": "Class-based views for the win",
        "definition": "Class-based views (ListView, DetailView, CreateView and friends) ship the boilerplate of CRUD — pagination, context preparation, GET/POST handling — as reusable mixins and generics. Where a flow is custom, a plain function view stays the simplest option; the two sit side by side in the same project without friction.",
        "example": "from django.views.generic import ListView\nfrom django.views.generic.edit import CreateView\nfrom .models import Post\n\nclass PostList(ListView):\n    model = Post\n    paginate_by = 10\n\nclass PostCreate(CreateView):\n    model = Post\n    fields = [\"title\", \"published\"]\n    success_url = \"/posts/\"",
        "usecase": "CRUD screens come free — listing with pagination, detail, create/edit/delete — while occasional custom flows hand-roll in a function view without breaking the pattern.",
        "category": "django"
    },
    {
        "id": 10,
        "title": "URL converters & namespaces",
        "definition": "path() converters capture typed URL segments — <int:post_id> passes an integer, <slug:slug> a slug — so matching and coercion are declared, not parsed by hand. Naming routes and giving apps an app_name means you can reverse() a URL by name instead of hardcoding paths that break the moment a URL moves.",
        "example": "app_name = \"blog\"\nurlpatterns = [\n    path(\"posts/<int:post_id>/\", views.post_detail, name=\"post-detail\"),\n]\n\n# anywhere:\nurl = reverse(\"blog:post-detail\", args=[3])   # still correct if URLs change",
        "usecase": "Linking pages across templates and views without hardcoding paths — reverse() always produces the current URL, even after a big URL refactor.",
        "category": "django"
    },
    {
        "id": 11,
        "title": "Template loops and filters",
        "definition": "Django's template language (DTL) keeps logic out of Python and markup in templates: {% for %} and {% if %} drive iteration and branching, while |filters like truncatechars and date post-process values inline. Templates stay readable for designers because the heavy lifting lives in views and filters.",
        "example": "{% for post in posts %}\n  <h2>{{ post.title|truncatechars:50 }}</h2>\n  <p>{{ post.published_at|date:\"Y-m-d\" }}</p>\n  {% if post.pinned %}<span>PINNED</span>{% endif %}\n{% empty %}\n  <p>No posts yet.</p>\n{% endfor %}",
        "usecase": "Rendering lists, dates and conditionals in HTML while keeping views purely about data — and keeping JavaScript-free pages fast and server-rendered.",
        "category": "django"
    },
    {
        "id": 12,
        "title": "Template inheritance",
        "definition": "A layout template defines named {% block %} sections; child templates {% extends %} it and override only the blocks they care about. One base.html carries the shared HTML head, navigation and footer across the whole site, so a site-wide change is a single edit instead of a find-and-replace across every page.",
        "example": "<!-- base.html -->\n<html><body>\n  <nav>{% block nav %}Home{% endblock %}</nav>\n  {% block content %}{% endblock %}\n</body></html>\n\n<!-- posts/archive.html -->\n{% extends \"base.html\" %}\n{% block content %}\n  {% for post in page_obj %}<h2>{{ post.title }}</h2>{% endfor %}\n{% endblock %}",
        "usecase": "Shared navigation, footer and HTML head across every page — change the header once and the whole site updates, with no copy-pasted markup drifting out of sync.",
        "category": "django"
    },
    {
        "id": 13,
        "title": "Static files, managed",
        "definition": "The {% static %} tag resolves the correct URL for CSS, JavaScript and images from your STATICFILES settings — pointing at the local filesystem in development and the assembled collection or CDN in production. Because it recomputes against settings, the same markup works everywhere.",
        "example": "<link rel=\"stylesheet\" href=\"{% static 'css/app.css' %}\">\n<script src=\"{% static 'js/app.js' %}\" defer></script>",
        "usecase": "Referencing assets so they work in development from source and, after collectstatic, from a CDN or web server in production — without changing templates.",
        "category": "django"
    },
    {
        "id": 14,
        "title": "login_required decorator",
        "definition": "login_required redirects anonymous visitors to the login page (honoring next=), and permission_required checks a named permission before the view runs. Two decorators replace hand-rolled authentication checks that tend to forget the redirect and the next-aware return trip.",
        "example": "from django.contrib.auth.decorators import login_required, permission_required\n\n@login_required\ndef dashboard(request):\n    ...\n\n@permission_required(\"blog.delete_post\", raise_exception=True)\ndef delete_post(request, post_id):\n    ...",
        "usecase": "Gating member pages and admin-ish actions with two lines instead of hand-rolled redirects — and raising 403 for logged-in users without the right permission.",
        "category": "django"
    },
    {
        "id": 15,
        "title": "Swap in a custom User early",
        "definition": "Subclassing AbstractUser and pointing AUTH_USER_MODEL at it — before the first migration — gives you full control of the user model forever. Doing it after data exists means reparenting tables and references, which is painful. Five minutes at project start saves days later.",
        "example": "# accounts/models.py\nfrom django.contrib.auth.models import AbstractUser\n\nclass User(AbstractUser):\n    def display_name(self):\n        return self.get_full_name() or self.username\n\n# settings.py\nAUTH_USER_MODEL = \"accounts.User\"",
        "usecase": "Adding phone numbers, avatars or org membership to accounts later without rebuilding auth — the custom user grows the auth model instead of fighting it.",
        "category": "django"
    },
    {
        "id": 16,
        "title": "Admin is a query UI for free",
        "definition": "Registering a model in the Django admin instantly gives staff a full data management UI. list_display chooses the shown columns, list_filter adds sidebar filters, search_fields enables search, and both stay declarative — no routes, views or templates of your own to write or maintain.",
        "example": "from django.contrib import admin\nfrom .models import Post\n\n@admin.register(Post)\nclass PostAdmin(admin.ModelAdmin):\n    list_display = [\"title\", \"published\", \"created_at\"]\n    list_filter = [\"published\"]\n    search_fields = [\"title\"]\n    list_editable = [\"published\"]",
        "usecase": "Support teams filtering orders, editors reviewing drafts, operators fixing data — a usable internal tool with zero extra routes, built from a class and four fields.",
        "category": "django"
    },
    {
        "id": 17,
        "title": "Signals for side effects",
        "definition": "Signals like post_save and m2m_changed fire when model events happen, letting you trigger side effects — emails, counters, cache invalidation — without editing every call site that creates or updates objects. They keep cross-cutting behavior attached to the data change itself, not to each view.",
        "example": "from django.db.models.signals import post_save\nfrom django.dispatch import receiver\n\n@receiver(post_save, sender=User)\ndef on_user_saved(sender, instance, created, **kwargs):\n    if created:\n        send_welcome_email(instance.email)\n        UserStats.objects.create(user=instance)",
        "usecase": "Welcome emails, denormalized counters and cache invalidation triggered by row changes — the side effect fires wherever the data changes, not just through one controller.",
        "category": "django"
    },
    {
        "id": 18,
        "title": "Migrations are your schema diary",
        "definition": "makemigrations diffs your models against the applied migrations and generates the change steps; migrate applies them to a database. Because every schema change is a recorded, reviewable, version-controlled file, production databases evolve safely — and you never hand-edit a live schema.",
        "example": "python manage.py makemigrations          # create the migration\npython manage.py migrate                 # apply it\npython manage.py makemigrations --empty blog   # add hand-written data fix",
        "usecase": "Rolling schema changes to production safely — reviewing exactly what will run before it runs, and replaying the same steps across dev, staging and prod.",
        "category": "django"
    },
    {
        "id": 19,
        "title": "Settings from environment",
        "definition": "Reading secrets and environment-specific values from os.environ keeps settings.py portable, commit-safe and deployment-agnostic. Secrets like SECRET_KEY and database credentials never land in the repo, and the same codebase runs in dev, staging and production with different environment variables.",
        "example": "import os\n\nSECRET_KEY = os.environ[\"DJANGO_SECRET_KEY\"]\nDEBUG = os.environ.get(\"DJANGO_DEBUG\", \"\") == \"1\"\nALLOWED_HOSTS = os.environ.get(\"DJANGO_ALLOWED_HOSTS\", \"localhost\").split(\",\")",
        "usecase": "One repo deploying to dev, staging and prod with different keys, databases and debug flags — while CI and teammates see no secrets in the code.",
        "category": "django"
    },
    {
        "id": 20,
        "title": "Configure Django logging",
        "definition": "The LOGGING dict routes logger records to handlers — console, files, error trackers — with levels and formatting. Your views log via a module logger, and production verbosity is tuned in settings, never by editing print statements scattered through the codebase.",
        "example": "import logging\n\nlogger = logging.getLogger(__name__)\n\nlogger.info(\"Payment %s created for order %s\", payment.id, order.id)\nlogger.error(\"Payment failed: %s\", exc, exc_info=True)",
        "usecase": "Debugging production after the fact — every user action and failure lands in one searchable, leveled place, and errors can route to Sentry or similar without code changes.",
        "category": "django"
    },
    {
        "id": 21,
        "title": "Test views with the Client",
        "definition": "django.test.TestCase sets up a test database and exposes self.client, a simulated browser that makes GET and POST requests against your URLs through the full middleware stack. Response status, context and redirects all become assertable — view testing as easy as calling a function.",
        "example": "from django.test import TestCase\n\nclass PostTests(TestCase):\n    def test_list_ok(self):\n        resp = self.client.get(\"/posts/\")\n        self.assertEqual(resp.status_code, 200)\n        self.assertContains(resp, \"Recent posts\")\n\n    def test_detail_missing_404s(self):\n        resp = self.client.get(\"/posts/99999/\")\n        self.assertEqual(resp.status_code, 404)",
        "usecase": "Regression-proofing routes, forms and auth flows before every deploy — the test suite guards against the view changes that silently break pages.",
        "category": "django"
    },
    {
        "id": 22,
        "title": "DRF: serializers + viewsets",
        "definition": "Django REST Framework builds JSON APIs on top of your models: serializers declare input/output fields and validation, and viewsets bundle the CRUD endpoints into one class that a router mounts for you. Nested relations, pagination and permissions slot in declaratively.",
        "example": "from rest_framework import serializers, viewsets\nfrom rest_framework.routers import DefaultRouter\nfrom .models import Post\n\nclass PostSerializer(serializers.ModelSerializer):\n    class Meta:\n        model = Post\n        fields = [\"id\", \"title\", \"published\", \"author\"]\n\nclass PostViewSet(viewsets.ModelViewSet):\n    queryset = Post.objects.select_related(\"author\").all()\n    serializer_class = PostSerializer\n\nrouter = DefaultRouter()\nrouter.register(\"posts\", PostViewSet)",
        "usecase": "APIs for a SPA or mobile app — create, read, update, delete and nested output from one viewset class, with browsable docs and auth built in.",
        "category": "django"
    },
    {
        "id": 23,
        "title": "Paginator for long lists",
        "definition": "Paginator splits a QuerySet into fixed-size pages, and Paginator.get_page() returns a Page object with has_previous, has_next and the neighboring page numbers. The queryset is only sliced for the current page, so a million-row table renders a 10-row page.",
        "example": "from django.core.paginator import Paginator\n\npage_obj = Paginator(Post.objects.all(), 10).get_page(request.GET.get(\"page\"))\n# template: {{ page_obj.number }} / {{ page_obj.paginator.num_pages }}\n#          {% if page_obj.has_next %} next page {% endif %}",
        "usecase": "Blog archives, admin tables and tag pages — a 10-item slice with page links instead of one massive page that drags the database and the browser.",
        "category": "django"
    },
    {
        "id": 24,
        "title": "Middleware wraps every request",
        "definition": "Middleware runs a hook before and after every request on its way through Django — the place to add headers, authenticate, throttle or short-circuit maintenance mode. One __call__ returns the response for all views, so cross-cutting concerns live in exactly one class.",
        "example": "class SecurityBoostMiddleware:\n    def __init__(self, get_response):\n        self.get_response = get_response\n\n    def __call__(self, request):\n        response = self.get_response(request)\n        response[\"X-Frame-Options\"] = \"DENY\"\n        response[\"X-Request-Id\"] = request.headers.get(\"X-Request-Id\", \"\")\n        return response",
        "usecase": "Security headers on every response, compression, maintenance mode, or stamping a request id for tracing logs — implemented once for the whole application.",
        "category": "django"
    },
    {
        "id": 25,
        "title": "Cache the slow stuff",
        "definition": "cache_page stores the entire rendered response for N seconds, and the low-level cache.set/cache.get keep arbitrary values (query results, computed lists) keyed with a timeout. The slowest, most-repeated parts of a site — dashboards, leaderboards, popular queries — become cheap cache hits.",
        "example": "from django.views.decorators.cache import cache_page\nfrom django.core.cache import cache\n\n# whole view cached for 5 minutes\nurlpatterns = [path(\"stats/\", cache_page(60 * 5)(views.stats))]\n\n# or cache a specific value\nmetrics = cache.get(\"metrics_v1\")\nif metrics is None:\n    metrics = compute_expensive_metrics()\n    cache.set(\"metrics_v1\", metrics, 300)",
        "usecase": "Dashboard queries that cost seconds — serve them from cache for minutes, keeping page load fast and the database load flat under spikes.",
        "category": "django"
    }
]
