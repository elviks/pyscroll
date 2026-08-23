TIPS = [
    {
        "id": 1,
        "title": "engine, the connection factory",
        "definition": "The Engine is the entry point of SQLAlchemy: it holds the database URL, a connection pool and dialect-specific behavior, and creates connections lazily only when work begins. Configuring one engine at application startup and passing it everywhere keeps credentials, pooling and logging configuration in a single, testable place.",
        "example": "from sqlalchemy import create_engine, text\n\nengine = create_engine(\n    \"postgresql+psycopg://app:secret@localhost/appdb\",\n    pool_size=5, max_overflow=10, echo=True,\n)\nwith engine.connect() as conn:\n    print(conn.scalar(text(\"select 1\")))",
        "usecase": "Every project starts here — one shared, pooled engine is the connection source for ORM and Core alike.",
        "category": "sqlalchemy"
    },
    {
        "id": 2,
        "title": "declarative, class equals table",
        "definition": "In the declarative style a Python class maps to one table: attributes become columns, the registry pairs classes with metadata, and rows come back as typed objects. Declaring models as classes makes the schema readable in code while queries return objects — the core ergonomics that made the ORM popular.",
        "example": "from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column\n\nclass Base(DeclarativeBase):\n    pass\n\nclass User(Base):\n    __tablename__ = \"users\"\n    id: Mapped[int] = mapped_column(primary_key=True)\n    email: Mapped[str] = mapped_column(unique=True)",
        "usecase": "Defining schemas that double as natural Python classes, so models, queries and type hints stay in one place.",
        "category": "sqlalchemy"
    },
    {
        "id": 3,
        "title": "columns, types and constraints",
        "definition": "mapped_column bundles the database type, constraints and defaults onto one attribute: types like String and Integer, plus nullable, unique, default and index flags. Because everything is declared on the attribute, each field reads as one line and CREATE TABLE statements are generated from the same definition.",
        "example": "from sqlalchemy import String\n\nclass Item(Base):\n    __tablename__ = \"items\"\n    id: Mapped[int] = mapped_column(primary_key=True)\n    sku: Mapped[str] = mapped_column(String(32), unique=True, index=True)\n    qty: Mapped[int] = mapped_column(default=0, nullable=False)",
        "usecase": "Communicating real database constraints — not just Python attributes — in one line per column.",
        "category": "sqlalchemy"
    },
    {
        "id": 4,
        "title": "select, the 2.0 way",
        "definition": "SQLAlchemy 2.0 unified everything around the select() construct: the same expression works for Core connections and ORM session queries. It reads top-down, composes with joins and filters, and executes through session.execute() into result objects that stream rows with typing.",
        "example": "from sqlalchemy import select\n\nstmt = select(User.email, User.id).where(User.active == True)\nwith Session(engine) as session:\n    rows = session.execute(stmt).all()",
        "usecase": "One querying API across Core and ORM, with results that behave the same everywhere.",
        "category": "sqlalchemy"
    },
    {
        "id": 5,
        "title": "where, filter like a query",
        "definition": "The .where() method narrows a select with column expressions — equality, LIKE, IN, BETWEEN — and composes, so each call stacks another AND condition. Columns are attribute references rather than strings, so typos surface as AttributeError early and the compiler handles all quoting differences between dialects.",
        "example": "from sqlalchemy import select, or_\n\nstmt = select(User).where(\n    or_(User.email.like(\"%@example.com\"), User.name == \"admin\"),\n    User.active == True,\n)",
        "usecase": "Composing precise filters programmatically and reusing the same select with different conditions at each call site.",
        "category": "sqlalchemy"
    },
    {
        "id": 6,
        "title": "session, the unit of work",
        "definition": "The Session tracks loaded objects in its identity map, queues inserts, updates and deletes, and flushes them together when told to commit. Everything inside one session is one atomic unit of work: either all changes land or rollback undoes them — the mental model behind reliable database writes.",
        "example": "with Session(engine) as session:\n    session.add(User(email=\"ada@example.com\"))\n    session.add_all([User(email=\"bob@example.com\"), User(email=\"carol@example.com\")])\n    session.commit()",
        "usecase": "Grouping related writes so they commit or roll back together, keeping the database consistent by construction.",
        "category": "sqlalchemy"
    },
    {
        "id": 7,
        "title": "session.get, primary key lookup",
        "definition": "session.get(Model, pk) fetches a row by primary key and consults the identity map first — if the object is already in memory, no SQL runs at all. It returns None when the row is missing instead of raising, which makes it the clean, idiomatic single-object lookup of the ORM.",
        "example": "with Session(engine) as session:\n    user = session.get(User, 7)\n    if user is not None:\n        print(user.email)",
        "usecase": "Loading one row by id without exception handling — the bread-and-butter of endpoints and services.",
        "category": "sqlalchemy"
    },
    {
        "id": 8,
        "title": "add, flush, commit phases",
        "definition": "session.add() stages an object, flush() emits the INSERT early so generated values like autoincrement ids become available, and commit() flushes then ends the transaction. Calling flush yourself lets you read new ids before the transaction closes, while automatic flushing at query time keeps behavior predictable.",
        "example": "with Session(engine) as session:\n    u = User(email=\"new@example.com\")\n    session.add(u)\n    session.flush()           # INSERT now\n    print(u.id)               # id populated by the DB\n    session.commit()",
        "usecase": "Needing the generated primary key of a fresh row before the transaction ends, for example child rows referencing it.",
        "category": "sqlalchemy"
    },
    {
        "id": 9,
        "title": "rollback, the rescue hatch",
        "definition": "When a flush or commit raises, the session falls back into a partial transaction, and rollback() discards every pending change and restores the identity map. A failed transaction poisons its session until rolled back, so wrapping write flows in try/rollback is the standard way to keep sessions reusable.",
        "example": "with Session(engine) as session:\n    try:\n        session.add_all(batch)\n        session.commit()\n    except IntegrityError:\n        session.rollback()\n        log.warning(\"duplicate rows skipped\")",
        "usecase": "Batches where one bad row must not kill the whole run — roll back and continue with the next chunk.",
        "category": "sqlalchemy"
    },
    {
        "id": 10,
        "title": "one session per transaction",
        "definition": "A session is not thread-safe and belongs to one unit of work, so web apps create one per request and close it when the request ends — via handlers, middleware or dependency injection. Reusing one long-lived session across requests hides stale state and merges transactions that should stay separate.",
        "example": "@app.get(\"/users/{user_id}\")\ndef get_user(user_id: int, session: Session = Depends(open_session)):\n    user = session.get(User, user_id)\n    return {\"email\": user.email} if user else {\"error\": \"not found\"}",
        "usecase": "Request-scoped sessions keep transactions short and stale reads out of web services.",
        "category": "sqlalchemy"
    },
    {
        "id": 11,
        "title": "identity map, one row one object",
        "definition": "Within one session, the identity map guarantees that every row with the same primary key is the same Python object. Mutating one reference mutates them all, and repeated lookups cost no extra SQL. That invariance is what makes session-level caching correct and consistent with the database.",
        "example": "with Session(engine) as session:\n    a = session.get(User, 1)\n    b = session.get(User, 1)\n    print(a is b)             # True — one object, one identity\n    a.email = \"x@example.com\"\n    session.commit()          # single UPDATE",
        "usecase": "Cache-safe, pointer-equal reads inside one transaction, with zero duplicate-object drift.",
        "category": "sqlalchemy"
    },
    {
        "id": 12,
        "title": "relationships, cross table objects",
        "definition": "A relationship() descriptor turns a foreign key pair into an object attribute, so user.orders traverses the join without writing SQL by hand. Configuring back_populates mirrors the link on both sides, and the load strategy — lazy, joined or selectin — decides how and when that SQL runs.",
        "example": "class Order(Base):\n    __tablename__ = \"orders\"\n    id: Mapped[int] = mapped_column(primary_key=True)\n    user_id: Mapped[int] = mapped_column(ForeignKey(\"users.id\"))\n\nclass User(Base):\n    __tablename__ = \"users\"\n    id: Mapped[int] = mapped_column(primary_key=True)\n    orders: Mapped[list[\"Order\"]] = relationship(back_populates=\"user\")",
        "usecase": "Navigating graphs of tables as ordinary object attributes while keeping SQL generation in the ORM.",
        "category": "sqlalchemy"
    },
    {
        "id": 13,
        "title": "lazy loading and the N+1 trap",
        "definition": "By default, related collections load lazily: one query fetches the parent rows, then every touch of user.orders fires another query per parent. That N-plus-one signature cripples loops that read a relationship for each row. Recognizing it is the first half of the fix; eager loading is the second.",
        "example": "# slow: 1 query for users + 1 query per user for orders\nfor user in session.scalars(select(User)).all():\n    print(user.email, len(user.orders))",
        "usecase": "Spotting the N-plus-one signature in performance work before rewriting queries blindly.",
        "category": "sqlalchemy"
    },
    {
        "id": 14,
        "title": "selectinload, kill N+1",
        "definition": "selectinload() prefetches a relationship with a single extra IN query, while joinedload() pulls it into the parent query with a JOIN. Both collapse N-plus-one into exactly two statements, and choosing per statement — not globally — keeps control where the data shape is actually known.",
        "example": "from sqlalchemy.orm import selectinload\n\nstmt = select(User).options(selectinload(User.orders)).where(User.active == True)\nusers = session.scalars(stmt).all()\nprint([len(u.orders) for u in users])   # exactly 2 queries total",
        "usecase": "Listing collections without per-row lookups — dashboards, reports and API list endpoints.",
        "category": "sqlalchemy"
    },
    {
        "id": 15,
        "title": "back_populates, mirror the link",
        "definition": "back_populates connects two relationship() definitions so either side of the association stays in sync: appending to user.orders also sets order.user, and the reverse assignment works the same way. Without the mirror the ORM treats the attributes as independent and can miss updates until flush.",
        "example": "class User(Base):\n    __tablename__ = \"users\"\n    id: Mapped[int] = mapped_column(primary_key=True)\n    orders: Mapped[list[\"Order\"]] = relationship(back_populates=\"user\")\n\nclass Order(Base):\n    __tablename__ = \"orders\"\n    id: Mapped[int] = mapped_column(primary_key=True)\n    user: Mapped[\"User\"] = relationship(back_populates=\"orders\")",
        "usecase": "Maintaining both navigation directions of an association without duplicating state logic.",
        "category": "sqlalchemy"
    },
    {
        "id": 16,
        "title": "many-to-many via a join table",
        "definition": "Many-to-many needs an association table: one model holding the two foreign keys, with relationships crossing it through secondary or the explicit model. Association objects can carry their own columns — quantity, role, grade — which is why the explicit model wins whenever the link itself holds data.",
        "example": "class Enrollment(Base):\n    __tablename__ = \"enrollments\"\n    student_id: Mapped[int] = mapped_column(ForeignKey(\"students.id\"), primary_key=True)\n    course_id: Mapped[int] = mapped_column(ForeignKey(\"courses.id\"), primary_key=True)\n    grade: Mapped[str] = mapped_column(String(2), default=\"A\")\n\nclass Student(Base):\n    __tablename__ = \"students\"\n    id: Mapped[int] = mapped_column(primary_key=True)\n    courses: Mapped[list[\"Course\"]] = relationship(secondary=\"enrollments\")",
        "usecase": "Student-course style links where the relationship itself carries attributes, not just existence.",
        "category": "sqlalchemy"
    },
    {
        "id": 17,
        "title": "cascade, control delete flow",
        "definition": "The cascade option on relationship() decides what happens to children when parents are deleted or orphaning occurs: options like all and delete-orphan automate child removal, while restrictive settings force explicit cleanup. Choosing a cascade is a data-integrity decision, not a convenience flag.",
        "example": "class Parent(Base):\n    __tablename__ = \"parents\"\n    id: Mapped[int] = mapped_column(primary_key=True)\n    children: Mapped[list[\"Child\"]] = relationship(\n        cascade=\"all, delete-orphan\", back_populates=\"parent\")",
        "usecase": "Whole-tree deletion — deleting a parent should take its children with it, not strand them.",
        "category": "sqlalchemy"
    },
    {
        "id": 18,
        "title": "self-referential relationships",
        "definition": "A relationship pointing at its own class models trees and hierarchies: a Node holding a parent_id foreign key to the same table represents arbitrary depth. Loading children or parents of one node then walks the tree, and combining it with lazy collections gives natural recursion in Python.",
        "example": "class Category(Base):\n    __tablename__ = \"categories\"\n    id: Mapped[int] = mapped_column(primary_key=True)\n    parent: Mapped[\"Category\"] = relationship(\n        remote_side=\"Category.id\", back_populates=\"children\")\n    children: Mapped[list[\"Category\"]] = relationship(\n        back_populates=\"parent\")",
        "usecase": "Org charts, comment threads and file trees stored in one table with unbounded depth.",
        "category": "sqlalchemy"
    },
    {
        "id": 19,
        "title": "server_default, let the DB decide",
        "definition": "server_default pushes defaults into the database — CURRENT_TIMESTAMP, sequences or any SQL expression — instead of into Python. That keeps behavior identical across every client that writes, and the ORM reflects computed values back onto loaded objects so code sees them without a manual refresh.",
        "example": "from sqlalchemy import func\n\nclass Ticket(Base):\n    __tablename__ = \"tickets\"\n    id: Mapped[int] = mapped_column(primary_key=True)\n    created_at: Mapped[datetime] = mapped_column(\n        server_default=func.now(), server_onupdate=func.now())",
        "usecase": "Timestamps and sequence ids where every writer — ORM, raw SQL, migrations — must observe the same default.",
        "category": "sqlalchemy"
    },
    {
        "id": 20,
        "title": "hybrid properties, logic in both worlds",
        "definition": "A hybrid_property computes a value in Python from column attributes while exposing the same expression for SQL: the same code that filters a query also works on already-loaded objects. Derived fields — full names, totals, computed statuses — no longer need dual implementations.",
        "example": "from sqlalchemy.ext.hybrid import hybrid_property\n\nclass User(Base):\n    __tablename__ = \"users\"\n    id: Mapped[int] = mapped_column(primary_key=True)\n    first: Mapped[str] = mapped_column(String(50))\n    last: Mapped[str] = mapped_column(String(50))\n\n    @hybrid_property\n    def full_name(self):\n        return f\"{self.first} {self.last}\"",
        "usecase": "Derived fields usable in both Python objects and SQL WHERE clauses from a single definition.",
        "category": "sqlalchemy"
    },
    {
        "id": 21,
        "title": "text(), the raw SQL escape hatch",
        "definition": "text() wraps hand-written SQL so it runs through the same engine, session and result pipeline as compiled statements, with :named parameters binding values safely. It is the escape hatch for vendor-specific features the ORM has not wrapped, while bound parameters keep injections out of hand-built queries.",
        "example": "from sqlalchemy import text\n\nwith engine.connect() as conn:\n    stmt = text(\"select id, email from users where active = :flag\")\n    rows = conn.execute(stmt, {\"flag\": True}).all()",
        "usecase": "Legacy queries and vendor SQL that compiled expressions do not cover, without losing parameter safety.",
        "category": "sqlalchemy"
    },
    {
        "id": 22,
        "title": "result objects, rows as data",
        "definition": "Execute calls return Result objects that stream rows instead of piling them all into memory. .all() materializes everything, .scalar() grabs a single value, .first() takes the leading row, and .mappings() yields dict-like rows — choosing the right accessor keeps memory bounded and intent obvious.",
        "example": "with Session(engine) as session:\n    stmt = select(User.id, User.email).order_by(User.id)\n    for row in session.execute(stmt):\n        print(row.id, row.email)",
        "usecase": "Iterating large result sets row by row and extracting single values without building full object lists.",
        "category": "sqlalchemy"
    },
    {
        "id": 23,
        "title": "group by, aggregate in SQL",
        "definition": "func.count(), func.sum() and friends push aggregation into the database, where GROUP BY collapses rows per group. Projecting the grouped key alongside the aggregate yields exactly the summary needed — per-user counts, per-month totals — without dragging full rows into Python.",
        "example": "from sqlalchemy import func, select\n\nstmt = select(Order.user_id, func.count(Order.id)).group_by(Order.user_id)\nrows = session.execute(stmt).all()\nprint({uid: count for uid, count in rows})",
        "usecase": "Dashboard summaries and reports that count and total by dimension directly in the database.",
        "category": "sqlalchemy"
    },
    {
        "id": 24,
        "title": "joins, assemble the query",
        "definition": "select(A).join(B, condition) composes tables into one statement, with join() inferring the ON clause from the foreign key when it can. Combining joins and where filters yields unified rows from several tables in a single round trip — the canonical alternative to loading relationships one object at a time.",
        "example": "stmt = select(User.email, Order.total).join(Order, Order.user_id == User.id)\nstmt = stmt.where(Order.total > 100)\nrows = session.execute(stmt).all()",
        "usecase": "Reporting queries across tables where a flat, filtered row set beats object traversal.",
        "category": "sqlalchemy"
    },
    {
        "id": 25,
        "title": "order, limit, offset pagination",
        "definition": ".order_by() sorts by column asc or desc, .limit() bounds the row count and .offset() skips a slice — page two, size twenty-five, classic pagination. Offset paging is easy and correct for small tables, though deep pages force the database to scan from the start, which is where keyset pagination takes over.",
        "example": "from sqlalchemy import desc\n\nstmt = select(User).order_by(desc(User.created_at)).limit(25).offset(25)\npage2 = session.scalars(stmt).all()",
        "usecase": "Admin tables and API list endpoints that slice one screen of rows per request.",
        "category": "sqlalchemy"
    },
    {
        "id": 26,
        "title": "keyset pagination, deep pages fast",
        "definition": "Keyset pagination replaces OFFSET with a WHERE on the ordering columns: fetch rows newer than the last seen key, ordered by the same keys. Each page starts from the bookmark, so cost stays proportional to page size even ten thousand pages deep — no full scans, no duplicates as rows shift.",
        "example": "from sqlalchemy import tuple_\n\nlast = (User.created_at, User.id)      # bookmark from the previous page\nstmt = select(User).order_by(User.created_at, User.id).where(\n    tuple_(User.created_at, User.id) > last\n).limit(25)",
        "usecase": "Infinite-scroll feeds and audit tables with millions of rows, where offset pages slow with every page.",
        "category": "sqlalchemy"
    },
    {
        "id": 27,
        "title": "delete and bulk deletes",
        "definition": "session.delete(obj) removes one loaded object and the ORM issues its DELETE on flush, applying configured cascades. For whole ranges, a Core delete() statement skips object loading entirely — careful with cascade rules, but bulk statements are the right tool for cleanup jobs.",
        "example": "from sqlalchemy import delete\n\nwith Session(engine) as session:\n    session.delete(expired_user)                     # one object, cascades applied\n    session.execute(delete(Log).where(Log.ts < cutoff))  # whole range, no loading\n    session.commit()",
        "usecase": "Removing a single entity through the ORM and mass-cleanup in bulk SQL without loading the rows.",
        "category": "sqlalchemy"
    },
    {
        "id": 28,
        "title": "bulk inserts, executemany style",
        "definition": "session.add_all() plus commit rides the ORM with per-object lifecycle and returned ids, while execute(insert().values(batch)) goes straight through executemany for raw throughput. ORM bulk operations preserve behaviors like defaults and cascades; Core inserts trade those for speed — choose by workload.",
        "example": "from sqlalchemy import insert\n\nrows = [{\"user_id\": u, \"score\": s} for u, s in pairs]\nwith engine.begin() as conn:\n    conn.execute(insert(Score), rows)     # one executemany, no objects built",
        "usecase": "Seeding scripts and ETL loads pushing thousands of rows in a single round trip.",
        "category": "sqlalchemy"
    },
    {
        "id": 29,
        "title": "upsert, insert on conflict",
        "definition": "insert().on_conflict_do_update() — the PostgreSQL dialect build — turns inserts into upserts: on a primary key or unique violation the existing row is updated instead of erroring. It is the idempotent writer for sync jobs that must run repeatedly against the same keys.",
        "example": "from sqlalchemy.dialects.postgresql import insert\n\nstmt = insert(Inventory).values(id=7, qty=5)\nstmt = stmt.on_conflict_do_update(\n    index_elements=[\"id\"], set_={\"qty\": stmt.excluded.qty})\nconn.execute(stmt)",
        "usecase": "Idempotent sync jobs that must rerun safely — write-or-update rows coming from external feeds.",
        "category": "sqlalchemy"
    },
    {
        "id": 30,
        "title": "locking, with_for_update",
        "definition": "with_for_update() adds SELECT ... FOR UPDATE, holding a row lock until the transaction ends — the database's own handshake against lost updates. Long transactions holding locks invite waits and deadlocks, so the pattern pairs locking with the shortest possible transaction window.",
        "example": "with Session(engine) as session:\n    row = session.scalars(\n        select(Balance).where(Balance.id == acct).with_for_update()\n    ).one()\n    row.amount -= withdrawal\n    session.commit()        # lock held exactly until here",
        "usecase": "Ledger and inventory updates where two concurrent requests must not overwrite each other's read.",
        "category": "sqlalchemy"
    },
    {
        "id": 31,
        "title": "refresh and expunge, control state",
        "definition": "session.refresh(obj) re-reads a row from the database, repopulating attributes and discarding local unflushed changes; expunge() detaches an object from the session entirely. These are the controls for pulling fresh state in long-lived services or moving objects safely outside transaction scope.",
        "example": "with Session(engine) as session:\n    u = session.get(User, 7)\n    session.refresh(u)      # latest committed values from the DB\n    session.expunge(u)\n    print(u.email)          # usable after the session closes",
        "usecase": "Live dashboards and workers that must observe committed changes without re-querying entire objects.",
        "category": "sqlalchemy"
    },
    {
        "id": 32,
        "title": "expired attributes, surprise selects",
        "definition": "After a commit the ORM expires object attributes by default, so touching one fires a fresh SELECT inside a new transaction — behavior that sometimes shows up as unexpected queries in logs. Setting expire_on_commit=False keeps values as they were after commit, trading staleness for zero surprise SQL.",
        "example": "from sqlalchemy.orm import sessionmaker\n\nSession = sessionmaker(engine, expire_on_commit=False)\n\nwith Session() as session:\n    u = session.get(User, 7)\n    email = u.email\n    session.commit()\n    print(u.email)          # no surprise re-select afterwards",
        "usecase": "Services that read the same attributes after commit and want deterministic, query-free behavior.",
        "category": "sqlalchemy"
    },
    {
        "id": 33,
        "title": "merge, reconcile identity",
        "definition": "session.merge(obj) copies the state of a detached object into the session — refreshing an already-loaded identity or inserting a fresh copy when the primary key is new. It is the bridge for objects that crossed session boundaries: cached, serialized, or handed between threads.",
        "example": "cached = get_from_redis(user_id)     # detached object\nwith Session(engine) as session:\n    merged = session.merge(cached)\n    merged.email = \"new@example.com\"\n    session.commit()",
        "usecase": "Re-attaching cached or API-deserialized objects to a live session cleanly.",
        "category": "sqlalchemy"
    },
    {
        "id": 34,
        "title": "reflection, introspect the DB",
        "definition": "autoload_with=engine inspects an existing table or view and builds the SQLAlchemy metadata for it — no model classes required. Reflecting legacy schemas makes read-only tooling instant, while hand-written models still win when code needs rich behavior on top of the schema.",
        "example": "from sqlalchemy import MetaData, Table\n\nmeta = MetaData()\nlegacy = Table(\"legacy_customers\", meta, autoload_with=engine)\nprint(legacy.columns.keys())",
        "usecase": "Pointing one-off reports and migration audits at databases you never modeled in code.",
        "category": "sqlalchemy"
    },
    {
        "id": 35,
        "title": "create_all, declare and create",
        "definition": "Base.metadata.create_all(engine) issues CREATE TABLE statements for every mapped table, skipping ones that already exist. It is ideal for prototypes and tests where schema follows code; production evolution belongs to Alembic migrations, though create_all remains a fast bootstrap for local environments.",
        "example": "Base.metadata.create_all(engine)\n\nwith Session(engine) as session:\n    session.add(User(email=\"ada@example.com\"))\n    session.commit()",
        "usecase": "Zero-config local setups and test suites that materialize the whole schema straight from models.",
        "category": "sqlalchemy"
    },
    {
        "id": 36,
        "title": "Alembic for real migrations",
        "definition": "Alembic, the SQLAlchemy migration tool, records schema evolution as versioned, ordered scripts and applies them up or down. autogenerate diffs your models against the live database to draft each step, so releases move schemas forward reproducibly instead of by hand-edited SQL.",
        "example": "# terminal: draft and apply schema steps from your models\nalembic revision --autogenerate -m \"add email index\"\nalembic upgrade head",
        "usecase": "Shipping schema changes with applications — reviewable, rollback-able migrations in CI.",
        "category": "sqlalchemy"
    },
    {
        "id": 37,
        "title": "connection pooling, stay warm",
        "definition": "The engine recycles connections through a pool instead of opening a fresh one per call, tuned with pool_size, max_overflow and pool_pre_ping. Pre-ping verifies connections before handing them out, preventing stale socket errors after idle gaps — a single configuration that removes whole classes of flaky failures.",
        "example": "engine = create_engine(\n    \"postgresql+psycopg://app:secret@localhost/appdb\",\n    pool_size=10, max_overflow=5, pool_pre_ping=True,\n)",
        "usecase": "Web services behind NATs and load balancers where idle connections silently die between requests.",
        "category": "sqlalchemy"
    },
    {
        "id": 38,
        "title": "echo=True, watch every statement",
        "definition": "Engine logging with echo=True, or a configured logger, prints every SQL statement, its parameters and execution metadata to the console. That trace is the fastest way to see what the ORM actually emits — join shapes, query counts, bound parameters — turning mystery behavior into evidence.",
        "example": "engine = create_engine(url, echo=True)\n\nwith Session(engine) as session:\n    users = session.scalars(select(User)).all()   # SQL appears on stdout",
        "usecase": "Debugging surprising N-plus-one patterns, unexpected defaults or opaque ORM statements in minutes.",
        "category": "sqlalchemy"
    },
    {
        "id": 39,
        "title": "sessionmaker, the session factory",
        "definition": "sessionmaker(engine) bakes the engine and configuration into a callable that produces sessions — the recommended way to provide sessions to dependency injection or context managers. Async variants and scoped registries build on it, keeping one factory as the single place session behavior is defined.",
        "example": "from sqlalchemy.orm import sessionmaker\n\nSession = sessionmaker(bind=engine, expire_on_commit=False)\n\nwith Session() as session:\n    user = session.get(User, 7)",
        "usecase": "Standardizing session creation app-wide — DI containers, FastAPI dependencies, workers, tests.",
        "category": "sqlalchemy"
    },
    {
        "id": 40,
        "title": "AsyncSession, async database work",
        "definition": "SQLAlchemy's async support runs the same session API on an AsyncSession with await on execute, commit and rollback. Dialects like asyncpg and aiosqlite lift the whole ORM onto asyncio, so one codebase serves sync CLI tools and async web apps without changing the queries.",
        "example": "from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker\n\nengine = create_async_engine(\"postgresql+asyncpg://app:secret@localhost/appdb\")\nAsyncSession = async_sessionmaker(engine)\n\nasync with AsyncSession() as session:\n    user = await session.get(User, 7)",
        "usecase": "Async web frameworks like FastAPI with async database drivers, without abandoning the ORM.",
        "category": "sqlalchemy"
    },
    {
        "id": 41,
        "title": "load_only, trim the payload",
        "definition": "load_only() fetches only the listed columns of an entity, and defer() delays the rest into lazy SELECTs on access. List endpoints that project a handful of fields stop deserializing entire heavy rows — a memory and bandwidth win on hot paths and wide tables.",
        "example": "from sqlalchemy.orm import load_only\n\nstmt = select(User).options(load_only(User.id, User.email)).order_by(User.id)\nusers = session.scalars(stmt).all()",
        "usecase": "List and search endpoints that only need a few columns, not whole heavy rows.",
        "category": "sqlalchemy"
    },
    {
        "id": 42,
        "title": "three flavors of defaults",
        "definition": "default runs in Python when the ORM inserts; server_default lives in the database for every client; onupdate stamps values on each update of the row. Composing them, a created_at timestamp comes from the database once, an updated_at refreshes on change, and app-side defaults cover values only the ORM knows.",
        "example": "class Audit(Base):\n    __tablename__ = \"audit\"\n    id: Mapped[int] = mapped_column(primary_key=True)\n    created_at: Mapped[datetime] = mapped_column(server_default=func.now())\n    updated_at: Mapped[datetime] = mapped_column(\n        server_default=func.now(), onupdate=func.now())",
        "usecase": "Choosing where truth lives — Python-only values on the app side, timestamps owned by the database.",
        "category": "sqlalchemy"
    },
    {
        "id": 43,
        "title": "enums, close the value set",
        "definition": "A typed column backed by an Enum gives a closed set of values enforced by the schema itself, whichever client writes. Python Enum classes or plain strings map through the dialect, keeping invalid states out at the storage layer — the natural home for workflow status machines.",
        "example": "from enum import Enum\n\nclass OrderStatus(Enum):\n    pending = \"pending\"\n    paid = \"paid\"\n    shipped = \"shipped\"\n\nclass Order(Base):\n    __tablename__ = \"orders\"\n    id: Mapped[int] = mapped_column(primary_key=True)\n    status: Mapped[OrderStatus] = mapped_column(\n        Enum(OrderStatus), default=OrderStatus.pending)",
        "usecase": "State machines stored as enums — workflow columns that only accept declared states.",
        "category": "sqlalchemy"
    },
    {
        "id": 44,
        "title": "JSON columns for flexible data",
        "definition": "Postgres JSONB gives a document inside a relational row, queryable by path and containment in SQL. SQLAlchemy maps dict and list values onto it transparently, and the JSONB build adds containment operators — flexible attributes get schema-less storage with the same joins and indexes around it.",
        "example": "from sqlalchemy.dialects.postgresql import JSONB\n\nclass Product(Base):\n    __tablename__ = \"products\"\n    id: Mapped[int] = mapped_column(primary_key=True)\n    attrs: Mapped[dict] = mapped_column(JSONB, default=dict)\n\np.attrs[\"color\"] = \"midnight blue\"",
        "usecase": "Evolving product metadata, feature flags and settings blobs that do not fit a fixed schema.",
        "category": "sqlalchemy"
    },
    {
        "id": 45,
        "title": "datetime columns, stay aware",
        "definition": "DateTime(timezone=True) stores timestamps with timezone where the dialect supports it, Postgres first among them. Storing naive UTC and interpreting at the boundary is one consistent policy; mixing naive and aware values across systems is where bugs hide — pick a policy and enforce it.",
        "example": "from datetime import datetime, timezone\n\nclass Event(Base):\n    __tablename__ = \"events\"\n    id: Mapped[int] = mapped_column(primary_key=True)\n    at: Mapped[datetime] = mapped_column(\n        DateTime(timezone=True),\n        default=lambda: datetime.now(timezone.utc),\n    )",
        "usecase": "Global apps logging events across servers and timezones without ambiguity.",
        "category": "sqlalchemy"
    },
    {
        "id": 46,
        "title": "count in SQL, not in Python",
        "definition": "Counting and filtering belong in the database with func.count(), where the engine counts rows in its own fast way. Pulling rows into Python just to len() them wastes bandwidth and memory, and pairing count with group by produces per-bucket totals in the same single round trip.",
        "example": "from sqlalchemy import func, select\n\ntotal = session.scalar(select(func.count()).select_from(User))\nper_status = session.execute(\n    select(Order.status, func.count()).group_by(Order.status)\n).all()",
        "usecase": "Stats endpoints and badges needing totals and distributions without shipping every row.",
        "category": "sqlalchemy"
    },
    {
        "id": 47,
        "title": "exists, prove without loading",
        "definition": "The exists() construct compiles to a WHERE EXISTS subquery that checks for at least one matching row without carrying its data. Used inside filters, it answers membership questions — is there a row — in the cheapest way the database can, and pairs naturally with NOT to invert the test.",
        "example": "from sqlalchemy import exists\n\nstmt = select(User.id, User.email).where(\n    exists().where(Order.user_id == User.id)\n)\nrows = session.execute(stmt).all()",
        "usecase": "Filtering by membership — users who placed at least one order — without materializing child rows.",
        "category": "sqlalchemy"
    },
    {
        "id": 48,
        "title": "subqueries, compose statements",
        "definition": "A select can act as building material: .subquery() embeds it into a FROM clause under an alias, and .scalar_subquery() turns a one-column aggregate into a comparison value. Chaining statements builds multi-stage queries — maxima per group, filters against counts — in pure Python composition.",
        "example": "from sqlalchemy import func, select\n\nmax_qty = select(func.max(Order.qty)).scalar_subquery()\nstmt = select(Order).where(Order.qty == max_qty)\ntop = session.scalars(stmt).all()",
        "usecase": "Stage-aware queries — compare against aggregates, or reuse computed sets as derived tables.",
        "category": "sqlalchemy"
    },
    {
        "id": 49,
        "title": "indexes, speed the reads that exist",
        "definition": "Indexes on single or combined columns make lookups and ordering fast at the cost of write and storage overhead. Unique indexes double as constraints, and per-dialect index types — GIN for JSONB, expression indexes, partial indexes — serve query shapes a plain B-tree cannot.",
        "example": "from sqlalchemy import func\n\nclass User(Base):\n    __tablename__ = \"users\"\n    id: Mapped[int] = mapped_column(primary_key=True)\n    email: Mapped[str] = mapped_column(String(255), unique=True)\n    last_seen: Mapped[datetime] = mapped_column(\n        DateTime(timezone=True), index=True, default=func.now())",
        "usecase": "Putting indexes behind the filters and sorts real queries use, measured with EXPLAIN.",
        "category": "sqlalchemy"
    },
    {
        "id": 50,
        "title": "one transaction, or none",
        "definition": "The classic discipline: wrap one unit of work in one transaction, commit once, and let every statement inside it share the same snapshot and outcome. Scattered commits break atomicity, while read-only work gains nothing from committing at all — begin, act, commit, end.",
        "example": "with engine.begin() as conn:       # one transaction, commit on exit\n    conn.execute(insert(Order), order_rows)\n    conn.execute(insert(OrderItem), item_rows)\n# all or nothing; any exception rolls back",
        "usecase": "Multi-table writes — order plus items — that must land together or not at all.",
        "category": "sqlalchemy"
    }
]
