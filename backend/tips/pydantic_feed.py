TIPS = [
    {
        "id": 1,
        "title": "BaseModel is the heart of Pydantic",
        "definition": "Subclassing pydantic.BaseModel turns your class into a validated data container: every field you declare as an annotated class attribute gets type-checked and coerced at instantiation time. Invalid input raises a ValidationError instantly, so malformed data never survives into your business logic. Model instances then serialize back to dicts or JSON with one call, giving you a single trusted shape for data crossing API, database and config boundaries.",
        "example": "from pydantic import BaseModel\n\nclass User(BaseModel):\n    name: str\n    age: int\n\nu = User(name=\"Ada\", age=37)      # works\nbad = User(name=\"Ada\", age=\"x\")  # ValidationError raised",
        "usecase": "Defining the contract of every payload in your service — request bodies, config files and database rows all validate at the boundary, before they touch domain logic.",
        "category": "pydantic"
    },
    {
        "id": 2,
        "title": "Annotations declare the schema",
        "definition": "In Pydantic the field type IS the schema: writing age: int declares both the type hint your editor sees and the runtime validation rules. There is no separate schema file to keep in sync, no double source of truth. Because the annotation is Python itself, anything the type system can express — unions, lists, nested models, Literal values — becomes validation automatically.",
        "example": "from pydantic import BaseModel\nfrom typing import Literal, List\n\nclass Order(BaseModel):\n    items: List[str]\n    status: Literal[\"pending\", \"paid\", \"shipped\"]\n\nOrder(items=[\"a\"], status=\"paid\")       # ok\nOrder(items=\"a\", status=\"paid\")         # fails: items must be a list",
        "usecase": "Modeling API requests where the type hints in your function signatures and the runtime validation are the same declarations — nothing drifts out of sync.",
        "category": "pydantic"
    },
    {
        "id": 3,
        "title": "Required vs optional fields",
        "definition": "Fields without a default are required — omitting them raises ValidationError. Adding a default or Optional[str] marks the field optional. In modern Python you write name: str | None = None instead of Optional, and Pydantic treats fields with defaults as optional while still validating any value that IS provided, so optional never means untyped.",
        "example": "from pydantic import BaseModel\n\nclass Profile(BaseModel):\n    username: str                     # required\n    bio: str | None = None            # optional\n    verified: bool = False            # optional, defaulted\n\nProfile(username=\"ada\")              # ok, bio and verified default\nProfile()                             # ValidationError: username missing",
        "usecase": "Shaping partial data like user profiles and settings where some fields always exist while others (bio, avatar) appear only when the user fills them in.",
        "category": "pydantic"
    },
    {
        "id": 4,
        "title": "Defaults are validated too",
        "definition": "Pydantic validates not only the input you pass but also the default value of a field when it is used. A typo like a default string where an int is annotated fails at class definition time or at first instantiation, catching errors that plain Python dataclasses would silently ship. Defaults can also be functions or factories via default_factory for mutable values like lists and dicts.",
        "example": "from pydantic import BaseModel, Field\nfrom typing import List\n\nclass Cart(BaseModel):\n    items: List[str] = []                      # bad: shared mutable default\n\nclass Cart(BaseModel):\n    items: List[str] = Field(default_factory=list)  # correct: fresh per instance",
        "usecase": "Every model with defaulted collections — cart items, tags, permissions — gets a fresh list per instance instead of all instances sharing one global mutable default.",
        "category": "pydantic"
    },
    {
        "id": 5,
        "title": "Field() adds metadata and constraints",
        "definition": "pydantic.Field configures a single field: constraints like min_length, ge/le, and pattern, plus metadata like description, examples and titles that flow into generated JSON schemas. Field is the per-field counterpart of ConfigDict, and when combined with Annotated it can live entirely inside the type annotation so the constraint travels with the type itself.",
        "example": "from pydantic import BaseModel, Field\n\nclass Product(BaseModel):\n    sku: str = Field(min_length=4, max_length=20, description=\"Stock keeping unit\")\n    price: float = Field(gt=0, le=100000)\n\nProduct(sku=\"AB12\", price=9.99)   # ok\nProduct(sku=\"x\", price=-1)        # ValidationError on both",
        "usecase": "Enforcing business rules at the data boundary: SKU length, price ranges, age limits — constraints live next to the field they govern, not scattered through validation code.",
        "category": "pydantic"
    },
    {
        "id": 6,
        "title": "String constraints: length and pattern",
        "definition": "Pydantic validates strings with min_length and max_length, and regex constraints through pattern= in Field or the Pattern[...] type. Length checks run first, then the compiled regex matches the whole string, not a substring — so pattern=\"\\d{3}\" rejects '12a34'. This makes format validation declarative: the annotation states what a valid string looks like.",
        "example": "from pydantic import BaseModel, Field\n\nclass Code(BaseModel):\n    zip: str = Field(pattern=r\"\\d{5}\")\n    tag: str = Field(min_length=2, max_length=10)\n\nCode(zip=\"12345\", tag=\"hi\")      # ok\nCode(zip=\"12a45\", tag=\"x\")       # fails both constraints",
        "usecase": "Enforcing formats like ZIP codes, phone numbers, or internal identifiers at the API edge so every downstream consumer receives strings of a guaranteed shape.",
        "category": "pydantic"
    },
    {
        "id": 7,
        "title": "Numeric constraints: gt, ge, lt, le",
        "definition": "Field(gt=0) means strictly greater than, ge means greater-or-equal, lt and le the mirror image — the four cover almost every range rule an integer or float field needs. Pydantic enforces them after type coercion, so '42' passes the int coercion then the bound check, while 0 fails the constraint itself.",
        "example": "from pydantic import BaseModel, Field\n\nclass Score(BaseModel):\n    points: int = Field(ge=0, le=100)\n    ratio: float = Field(gt=0, lt=1)\n\nScore(points=99, ratio=0.5)   # ok\nScore(points=101, ratio=0.5)  # ValidationError: <= 100 violated",
        "usecase": "Rejecting impossible domain values before they propagate — scores over 100, negative inventory, ratios outside (0, 1) — in a single declarative line per field.",
        "category": "pydantic"
    },
    {
        "id": 8,
        "title": "EmailStr validates real email syntax",
        "definition": "EmailStr is a string subtype that runs a real email-address parser from the email-validator package — not a naive regex — checking local part, domain and basic rules. Install pydantic[email] to enable it. It rejects things a regex misses, like double dots, and normalizes the parsed address for later use.",
        "example": "from pydantic import BaseModel, EmailStr\n\nclass Contact(BaseModel):\n    email: EmailStr\n\nContact(email=\"ada@example.com\")       # ok\nContact(email=\"ada@example\")            # ValidationError: no dot domain\nContact(email=\"ada@@example.com\")      # ValidationError: double @",
        "usecase": "Validating user signup forms and contact endpoints so bad addresses fail at the API edge instead of flooding your email-sending pipeline with junk.",
        "category": "pydantic"
    },
    {
        "id": 9,
        "title": "Literal restricts values to a closed set",
        "definition": "Literal[\"pending\", \"paid\"] means the value must be exactly one of the listed strings (or ints, or bools) — a type-level enum without the class boilerplate. Pydantic enforces it at runtime, your editor autocompletes the options, and the constraint is visible in the generated JSON schema as an enum list for frontend validation.",
        "example": "from pydantic import BaseModel\nfrom typing import Literal\n\nclass Task(BaseModel):\n    status: Literal[\"todo\", \"done\", \"archived\"]\n    priority: Literal[1, 2, 3]\n\nTask(status=\"done\", priority=2)     # ok\nTask(status=\"cancelled\", priority=2)  # ValidationError",
        "usecase": "Modeling state machines and enums — order status, task states, severity levels — where a misspelled state is caught immediately instead of silently matching no branch.",
        "category": "pydantic"
    },
    {
        "id": 10,
        "title": "Unions give a field multiple allowed types",
        "definition": "x: int | str accepts an integer OR a string, and Pydantic tries each branch in order, coercing where possible. This models data that legitimately arrives in more than one shape — a stringified ID or a numeric one, an int count or None. Narrow with Literal tags or discriminated unions when branches become ambiguous.",
        "example": "from pydantic import BaseModel\n\nclass Payment(BaseModel):\n    amount: int | str   # card vs check number\n    ref: int | None = None\n\nPayment(amount=50)               # int branch, stays int\nPayment(amount=\"abc\")            # string branch (int coercion fails)\nPayment(ref=None)                # optional union accepts None",
        "usecase": "Modeling pragmatic APIs where fields vary — an amount sent as '50' or 50, an id as int or str — without writing or-branches in every validation handler.",
        "category": "pydantic"
    },
    {
        "id": 11,
        "title": "ValidationError exposes every problem",
        "definition": "When validation fails Pydantic raises ValidationError, and str(exc) renders a readable report listing every invalid field, the error type and the offending value. exc.errors() returns structured dicts with loc, msg and input that you can map to HTTP 422 responses or form errors — no need to re-parse human text.",
        "example": "from pydantic import BaseModel, ValidationError\n\nclass User(BaseModel):\n    name: str\n    age: int\n\ntry:\n    User(name=1, age=\"x\")\nexcept ValidationError as e:\n    print(e.errors())\n    # [{'loc': ('name',), 'msg': 'Input should be a valid string', ...}, ...]",
        "usecase": "Turning validation failures into precise API responses: each error object becomes one 422 detail entry the frontend can map directly onto its form fields.",
        "category": "pydantic"
    },
    {
        "id": 12,
        "title": "field_validator for single-field logic",
        "definition": "The @field_validator decorator registers a method that runs after a field is validated, receiving the value and returning the (possibly transformed) value. Set mode=\"before\" to run on the raw input before type coercion, which is where messy data like \"   \" whitespace or '0' strings get cleaned. The validator's name must match the field name.",
        "example": "from pydantic import BaseModel, field_validator\n\nclass User(BaseModel):\n    name: str\n\n    @field_validator(\"name\")\n    @classmethod\n    def strip_name(cls, v):\n        v = v.strip()\n        if not v:\n            raise ValueError(\"name cannot be blank\")\n        return v",
        "usecase": "Normalizing inputs that users actually type — stripping whitespace, uppercasing SKUs, rejecting empty strings — while keeping the coercion rules declarative.",
        "category": "pydantic"
    },
    {
        "id": 13,
        "title": "model_validator for cross-field checks",
        "definition": "The @model_validator decorator operates on the whole model instead of one field. With mode=\"after\" it receives the fully validated instance, letting you compare fields — password vs password_confirmation — and raise ValueError to reject the whole model. mode=\"before\" sees the raw dict before any field validation.",
        "example": "from pydantic import BaseModel, model_validator\n\nclass Signup(BaseModel):\n    password: str\n    confirm: str\n\n    @model_validator(mode=\"after\")\n    def check_match(self):\n        if self.password != self.confirm:\n            raise ValueError(\"passwords do not match\")\n        return self",
        "usecase": "Enforcing relationship rules between fields — matching passwords, start before end dates, credit-limit within account limit — where no single field carries enough information.",
        "category": "pydantic"
    },
    {
        "id": 14,
        "title": "Validators can rewrite the value",
        "definition": "A validator's return value replaces the input: strip whitespace, lowercase an email, pad an ID, convert 'yes'/'no' to True/False. Because the returned value is validated afterward, you can normalize first and let type checks catch the result. Validators returning the value unchanged act as pure assertions.",
        "example": "from pydantic import BaseModel, field_validator\n\nclass Tag(BaseModel):\n    name: str\n\n    @field_validator(\"name\")\n    @classmethod\n    def lower(cls, v):\n        return v.strip().lower()   # value is replaced",
        "usecase": "Canonicalizing free-form user input into stored form — emails lowercased, tags trimmed and deduplicated — so the database always sees one consistent spelling.",
        "category": "pydantic"
    },
    {
        "id": 15,
        "title": "mode=\"before\" sees raw input",
        "definition": "A validator with mode=\"before\" runs on the raw incoming value before any coercion, which is the right place for forgiving input handling: stripping whitespace that would break an int coercion, treating None and \"\" alike, or mapping legacy field names. It receives whatever the caller actually passed, typed as Any.",
        "example": "from pydantic import BaseModel, field_validator\n\nclass Cfg(BaseModel):\n    retries: int\n\n    @field_validator(\"retries\", mode=\"before\")\n    @classmethod\n    def empty_is_zero(cls, v):\n        if v in (None, \"\"):\n            return 0\n        return v",
        "usecase": "Absorbing sloppy legacy clients: empty strings for numbers, None for optional tokens, whitespace in IDs — fixed in one layer instead of patched call-site by call-site.",
        "category": "pydantic"
    },
    {
        "id": 16,
        "title": "mode=\"wrap\" combines before and after",
        "definition": "A wrap validator wraps the validation handler itself: it receives the raw value and a callable handler that performs the default validation. The validator can transform the value, call handler() to run normal checks, and inspect or override the handler's result — giving full control for cases like falling back to a default on error.",
        "example": "from pydantic import BaseModel, field_validator\n\nclass Cfg(BaseModel):\n    port: int\n\n    @field_validator(\"port\", mode=\"wrap\")\n    @classmethod\n    def fallback(cls, v, handler):\n        try:\n            return handler(v)\n        except ValueError:\n            return 8080",
        "usecase": "Graceful degradation when parsing imperfect data — a bad port falls back to the default, a malformed date falls back to today — without catching exceptions at every call site.",
        "category": "pydantic"
    },
    {
        "id": 17,
        "title": "ConfigDict controls model behavior",
        "definition": "The model_config class attribute takes ConfigDict keys like extra, frozen, str_strip_whitespace, validate_assignment and populate_by_name. These model-wide switches replace dozens of per-field tweaks, and str_strip_whitespace alone removes the need for strip validators on every string field. Config applies to the class and its subclasses.",
        "example": "from pydantic import BaseModel, ConfigDict\n\nclass User(BaseModel):\n    model_config = ConfigDict(str_strip_whitespace=True, frozen=True)\n    name: str\n    age: int\n\nu = User(name=\"  Ada  \", age=1)\nprint(u.name)      # \"Ada\"\nu.name = \"Bob\"     # raises: instance is frozen",
        "usecase": "Standardizing hygiene across an entire model tree — trimming all strings, forbidding unknown fields, freezing immutable configs — in two lines instead of per-field work.",
        "category": "pydantic"
    },
    {
        "id": 18,
        "title": "extra controls unknown fields",
        "definition": "extra=\"forbid\" makes unknown keys raise ValidationError, extra=\"ignore\" (default) silently drops them, and extra=\"allow\" stores them on the instance. Forbid catches typos in config dicts and payloads early; allow is useful for pass-through proxies that echo extra attributes.",
        "example": "from pydantic import BaseModel, ConfigDict\n\nclass Strict(BaseModel):\n    model_config = ConfigDict(extra=\"forbid\")\n    name: str\n\nStrict(name=\"Ada\", agge=37)\n# ValidationError: extra fields not permitted ('agge')",
        "usecase": "Protecting config files and API payloads from typos — one misspelled key becomes a loud error instead of a silently ignored setting that haunts production.",
        "category": "pydantic"
    },
    {
        "id": 19,
        "title": "validate_assignment re-validates on set",
        "definition": "By default Pydantic validates at construction, then attribute assignment (m.age = 99) is unguarded. Setting validate_assignment=True in ConfigDict makes every assignment go through validation: type checks, constraints and validators all re-run. It costs a little performance but closes the mutation hole for mutable models.",
        "example": "from pydantic import BaseModel, ConfigDict\n\nclass Counter(BaseModel):\n    model_config = ConfigDict(validate_assignment=True)\n    value: int = 0\n\nc = Counter()\nc.value = 5      # ok\nc.value = \"x\"    # ValidationError now, silently accepted before",
        "usecase": "Keeping validation guarantees for long-lived mutable objects — live dashboards, game state, interactive sessions — where data changes many times after construction.",
        "category": "pydantic"
    },
    {
        "id": 20,
        "title": "frozen=True makes models immutable",
        "definition": "model_config = ConfigDict(frozen=True) makes every instance raise on attribute assignment or mutation of model values, giving you true immutability for configs and value objects. It's set() under the hood plus hashability: a frozen model can be used as a dict key or stored in a set, which plain mutable models cannot.",
        "example": "from pydantic import BaseModel, ConfigDict\n\nclass Point(BaseModel):\n    model_config = ConfigDict(frozen=True)\n    x: int\n    y: int\n\np = Point(x=1, y=2)\npoints = {p: \"origin-ish\"}   # hashable, usable as key",
        "usecase": "Modeling value objects and immutable configuration that should never change after load — swapping one accidentally shared between threads is safe and explicit.",
        "category": "pydantic"
    },
    {
        "id": 21,
        "title": "model_dump exports back to a dict",
        "definition": "model_dump() serializes an instance to a plain dict of validated values, undoing the coercion with the original types restored: datetime objects back, nested models to dicts, Path back to path objects. It's the reverse of model_validate, and its flags — exclude, exclude_none, exclude_unset — shape exactly what gets exported.",
        "example": "from pydantic import BaseModel\nfrom datetime import date\n\nclass Event(BaseModel):\n    name: str\n    when: date\n    note: str | None = None\n\ne = Event(name=\"launch\", when=\"2026-01-01\")\nprint(e.model_dump(exclude_none=True))\n# {'name': 'launch', 'when': datetime.date(2026, 1, 1)}",
        "usecase": "Converting validated models into plain dicts for database inserts, JSON responses or template rendering, while controlling which optional fields actually appear.",
        "category": "pydantic"
    },
    {
        "id": 22,
        "title": "model_dump_json for JSON output",
        "definition": "model_dump_json() serializes to a JSON string directly from the Rust core, without the intermediate Python dict that model_dump plus json.dumps would build. Dates serialize as ISO strings, enums as values, and bytes become base64. It's the standard way to emit response bodies from validated models.",
        "example": "from pydantic import BaseModel\n\nclass User(BaseModel):\n    name: str\n    age: int\n\nu = User(name=\"Ada\", age=37)\nprint(u.model_dump_json())\n# '{\"name\":\"Ada\",\"age\":37}'",
        "usecase": "Emitting API response bodies from validated models with correct ISO date handling and no manual field-by-field serialization code.",
        "category": "pydantic"
    },
    {
        "id": 23,
        "title": "model_validate from any source",
        "definition": "model_validate accepts a dict, another model instance, or any object exposing an iteration protocol and builds a validated instance from it, re-running every check. Unlike the constructor, it also accepts values like a namespaced object with attribute access. It's the canonical entry point when data comes from outside your code.",
        "example": "from pydantic import BaseModel\n\nclass User(BaseModel):\n    name: str\n    age: int\n\ndata = {\"name\": \"Ada\", \"age\": 37}\nu = User.model_validate(data)\nu2 = User.model_validate(u)     # model -> model\nprint(u2.name)",
        "usecase": "Building trusted models from untrusted origins — parsed JSON, ORM rows, external services — in one explicit call that documents where validation happens.",
        "category": "pydantic"
    },
    {
        "id": 24,
        "title": "model_validate_json avoids double parsing",
        "definition": "model_validate_json takes a JSON string and parses AND validates it in one pass inside the Rust core — skipping the intermediate Python objects that json.loads followed by model_validate would create. For big payloads that's measurably faster, and it keeps the validation boundary at exactly one line.",
        "example": "from pydantic import BaseModel\n\nclass User(BaseModel):\n    name: str\n    age: int\n\nraw = '{\"name\": \"Ada\", \"age\": 37}'\nu = User.model_validate_json(raw)   # parse + validate in one call",
        "usecase": "Processing large JSON payloads — webhook bodies, message queue messages, file imports — with parse and validate fused into one fast operation.",
        "category": "pydantic"
    },
    {
        "id": 25,
        "title": "TypeAdapter validates standalone values",
        "definition": "TypeAdapter wraps a bare type — a list, a dict, a union, a dataclass — and gives it the full model API: validate_python, validate_json, dump_python and json_schema, without needing a BaseModel at all. It's how Pydantic validates 'just a list of ints' or a free-form API key without inventing a class for it.",
        "example": "from pydantic import TypeAdapter\n\nints = TypeAdapter(list[int])\nprint(ints.validate_python([1, 2, 3]))   # [1, 2, 3]\nprint(ints.validate_python([1, \"a\"]))\n# ValidationError: Input should be a valid integer\nraw = '[1, 2, 3]'\nprint(ints.validate_json(raw))           # parse + validate",
        "usecase": "Validating values that don't need a whole model — endpoint query lists, individual settings, arbitrary JSON blobs — with the same error quality as full models.",
        "category": "pydantic"
    },
    {
        "id": 26,
        "title": "Nested models validate recursively",
        "definition": "A field can be another BaseModel: validation recurses through the whole object graph, so a bad value anywhere inside is caught and reported with a full loc path like ('address', 'city'). Nesting also builds nested JSON schemas automatically, mirroring your real data structure instead of flattening it.",
        "example": "from pydantic import BaseModel\n\nclass Address(BaseModel):\n    street: str\n    city: str\n\nclass Person(BaseModel):\n    name: str\n    address: Address\n\np = Person(name=\"Ada\", address={\"street\": \"1 Main\", \"city\": \"London\"})\nprint(p.address.city)   # validated nested object",
        "usecase": "Modeling hierarchical data — orders with shipping addresses, users with preferences, jobs with retry policies — with the full validation depth of the whole tree.",
        "category": "pydantic"
    },
    {
        "id": 27,
        "title": "Lists and sets get element validation",
        "definition": "list[Model] validates every element as a full model; list[int] coerces and checks each int; set[str] guarantees uniqueness and hashability. Errors carry the failing index in loc, so a bad element at position 4 is reported as ('items', 4, ...). Collections are containers whose contents receive the same strictness as top-level fields.",
        "example": "from pydantic import BaseModel\nfrom typing import List\n\nclass Cart(BaseModel):\n    items: List[int]\n\nCart(items=[1, 2, 3])      # ok\nCart(items=[1, \"x\", 3])\n# ValidationError: Input should be a valid integer at loc ('items', 1)",
        "usecase": "Validating arrays from JSON APIs — order lines, tag lists, team member IDs — so every element is checked, not just the fact that it's a list.",
        "category": "pydantic"
    },
    {
        "id": 28,
        "title": "dict fields validate keys and values",
        "definition": "dict[str, int] validates each key as a string and each value as an int; dict[str, Model] turns a JSON object into a map of validated models keyed by name. Like list errors, failures report the exact key in loc. It's the idiomatic way to model maps with a known value shape.",
        "example": "from pydantic import BaseModel\n\nclass Scoreboard(BaseModel):\n    scores: dict[str, int]\n\ns = Scoreboard(scores={\"ada\": 98, \"bob\": 87})\nprint(s.scores[\"ada\"])     # 98\nScoreboard(scores={\"ada\": \"high\"})  # ValidationError on the value",
        "usecase": "Modeling name-keyed data — feature flags, per-user limits, region configs — where each value must pass the same validation as a top-level field.",
        "category": "pydantic"
    },
    {
        "id": 29,
        "title": "datetime parses ISO strings automatically",
        "definition": "A field typed datetime accepts both datetime objects and ISO-8601 strings, parsing them in one step — no manual datetime.fromisoformat at every boundary. Same for date, time and timedelta. This makes JSON APIs pleasant: frontends send strings, the model hands your logic real datetime objects.",
        "example": "from pydantic import BaseModel\nfrom datetime import datetime\n\nclass Event(BaseModel):\n    starts: datetime\n\nprint(Event(starts=\"2026-08-20T18:00:00Z\").starts)\n# 2026-08-20 18:00:00+00:00 — a real datetime object",
        "usecase": "API payloads and database rows carrying timestamps — parsed to real datetime objects at the edge so every handler works with typed time instead of strings.",
        "category": "pydantic"
    },
    {
        "id": 30,
        "title": "UUID fields validate format",
        "definition": "A field typed UUID accepts the string form and stores a uuid.UUID object — canonicalizing dashes, casing and the four versions according to the RFC. The example shows that any valid UUID string form is accepted and normalized, while garbage like 'not-a-uuid' fails instantly with a clear message.",
        "example": "from pydantic import BaseModel\nfrom uuid import UUID\n\nclass Job(BaseModel):\n    job_id: UUID\n\nj = Job(job_id=\"12345678-1234-5678-1234-567812345678\")\nprint(j.job_id)   # UUID('12345678-1234-...')",
        "usecase": "Receiving UUID identifiers from clients and databases — validated and normalized to real UUID objects, so downstream code never parses string IDs by hand.",
        "category": "pydantic"
    },
    {
        "id": 31,
        "title": "HttpUrl and UrlStr validate links",
        "definition": "HttpUrl (legacy) and UrlStr (new) validate that a string is a parseable URL with a scheme and host, normalizing the stored value via urlparse. You get a structured object with .host, .path and .port instead of a raw string. Broken URLs — missing scheme, empty host — fail validation instead of failing later at fetch time.",
        "example": "from pydantic import BaseModel, UrlStr\n\nclass Link(BaseModel):\n    site: UrlStr\n\nl = Link(site=\"https://example.com/docs\")\nprint(l.site.host)   # 'example.com'\nLink(site=\"not a url\")   # ValidationError: invalid URL",
        "usecase": "Sanitizing webhook URLs, avatar links and redirect targets at the boundary so downstream fetchers only ever receive parseable, structured URLs.",
        "category": "pydantic"
    },
    {
        "id": 32,
        "title": "SecretStr keeps secrets out of repr",
        "definition": "SecretStr wraps a value so repr, str and debug output show '**********' instead of the real secret. Use .get_secret_value() when you truly need it, and prefer comparing secrets directly without ever materializing the raw string in logs.",
        "example": "from pydantic import BaseModel, SecretStr\n\nclass App(BaseModel):\n    name: str\n    api_key: SecretStr\n\na = App(name=\"billing\", api_key=\"sk-live-12345\")\nprint(a)          # api_key=SecretStr('**********')\nprint(a.api_key.get_secret_value())  # 'sk-live-12345'",
        "usecase": "Storing API keys, passwords and tokens in models that get logged, printed or serialized — the secret never leaks through repr in error reports.",
        "category": "pydantic"
    },
    {
        "id": 33,
        "title": "Aliases let JSON names differ from Python",
        "definition": "Field(alias=\"user_id\") maps the Python field user_id to the JSON key user_id and accepts the aliased name in model_validate, while the instance attribute stays user_id. With populate_by_name=True both the alias and the field name are accepted. It's how you embrace snake_case in code but camelCase on the wire.",
        "example": "from pydantic import BaseModel, Field\n\nclass User(BaseModel):\n    model_config = ConfigDict(populate_by_name=True)\n    user_id: int = Field(alias=\"userId\")\n\nu = User.model_validate({\"userId\": 7})   # alias accepted\nprint(u.user_id)                          # 7",
        "usecase": "Integrating camelCase third-party APIs and legacy JSON while keeping idiomatic Python names in your domain code — the mapping lives in one place.",
        "category": "pydantic"
    },
    {
        "id": 34,
        "title": "exclude_unset for partial updates",
        "definition": "model_dump(exclude_unset=True) exports only the fields the caller actually provided, dropping defaults. This powers PATCH-style updates: merge the incoming payload onto the stored object, then persist only what changed, without overwriting existing data with defaults.",
        "example": "from pydantic import BaseModel\n\nclass Profile(BaseModel):\n    name: str\n    bio: str = \"\"\n    private: bool = False\n\nincoming = Profile.model_validate({\"name\": \"Ada\"})\nprint(incoming.model_dump(exclude_unset=True))\n# {'name': 'Ada'}  — defaults not included",
        "usecase": "Building PATCH endpoints where the client sends only the fields to change — defaults and untouched values are never clobbered by the merge.",
        "category": "pydantic"
    },
    {
        "id": 35,
        "title": "model_copy for modified copies",
        "definition": "model_copy(update={\"status\": \"paid\"}) returns a new instance with chosen fields replaced, leaving the original untouched. Combined with frozen=True it gives a safe functional-update pattern: state changes are explicit copies, never in-place mutation, which makes reasoning about shared objects much easier.",
        "example": "from pydantic import BaseModel\n\nclass Order(BaseModel):\n    id: int\n    status: str = \"pending\"\n\no = Order(id=1)\npaid = o.model_copy(update={\"status\": \"paid\"})\nprint(o.status)     # 'pending' — original unchanged\nprint(paid.status)  # 'paid'",
        "usecase": "Audit logs and event-sourced flows where each state change must be a new object — original orders stay intact while derived copies carry the new status.",
        "category": "pydantic"
    },
    {
        "id": 36,
        "title": "PrivateAttr for non-field attributes",
        "definition": "Fields declared as class attributes are validated data; attributes you want on the instance WITHOUT validation or schema exposure are PrivateAttr: caches, lazy connections, internal counters. They're copied on model_copy, excluded from serialization, and declared with a default in PrivateAttr(default=...).",
        "example": "from pydantic import BaseModel, PrivateAttr\nfrom typing import Any\n\nclass Service(BaseModel):\n    base_url: str\n    _client: Any = PrivateAttr(default=None)\n\ns = Service(base_url=\"https://api.example.com\")\ns._client = \"lazy-created\"      # no validation, no serialization",
        "usecase": "Caching expensive lazy resources — HTTP clients, DB handles, memoized lookups — on validated models without polluting the JSON schema or serialized output.",
        "category": "pydantic"
    },
    {
        "id": 37,
        "title": "computed_field for derived attributes",
        "definition": "@computed_field turns a read-only method into a serialized, schema-visible property: a classmethod or @property that computes values from other fields — full_name, total_price, age from birthdate. It shows up in model_dump and JSON schema but is never accepted as input, keeping derived state consistent with stored state.",
        "example": "from pydantic import BaseModel, computed_field\n\nclass Order(BaseModel):\n    price: float\n    qty: int = 1\n\n    @computed_field\n    @property\n    def total(self) -> float:\n        return self.price * self.qty\n\nprint(Order(price=9.5).model_dump())\n# {'price': 9.5, 'qty': 1, 'total': 9.5}",
        "usecase": "Exposing derived values like invoice totals in API responses and schema documentation without storing them or accepting them as user input.",
        "category": "pydantic"
    },
    {
        "id": 38,
        "title": "Self-referencing models with forward refs",
        "definition": "A model referencing itself — a tree node with children: list['Node'] — is declared as a string forward reference. Pydantic resolves it lazily during model building, and a model can rebuild itself with model_rebuild() when needed. The quote marks tell the type system to defer the lookup.",
        "example": "from pydantic import BaseModel\nfrom typing import List\n\nclass Node(BaseModel):\n    value: str\n    children: List['Node'] = []\n\nroot = Node(value=\"a\", children=[Node(value=\"b\")])\nprint(root.children[0].value)   # 'b' — recursion validated",
        "usecase": "Modeling trees and recursive structures — comment threads, org charts, category hierarchies — with full validation at every nesting level.",
        "category": "pydantic"
    },
    {
        "id": 39,
        "title": "Forward references across modules",
        "definition": "When a model references a class defined later in another module, write the name as a string forward ref and let Pydantic resolve it during model building. For circular imports, define the reference lazily via TYPE_CHECKING and rebuild after all modules load — model_rebuild() resolves names that were unresolved at class definition.",
        "example": "from typing import TYPE_CHECKING, List\nfrom pydantic import BaseModel\n\nif TYPE_CHECKING:\n    from .author import Author\n\nclass Post(BaseModel):\n    title: str\n    author: 'Author' = None\n    # resolved at first use / model_rebuild()",
        "usecase": "Splitting large schemas across modules where models reference each other (Post -> Author -> Post) without forcing a circular import structure.",
        "category": "pydantic"
    },
    {
        "id": 40,
        "title": "model_json_schema generates OpenAPI-ready schemas",
        "definition": "model_json_schema() produces a JSON Schema document for the model — types, constraints, descriptions, required fields, nested schemas — that FastAPI and other tools consume for OpenAPI docs and frontend validation. Because Pydantic derives it from the annotations, the docs can never drift from the actual validation.",
        "example": "from pydantic import BaseModel, Field\n\nclass User(BaseModel):\n    name: str = Field(description=\"Display name\")\n    age: int = Field(ge=0)\n\nimport json\nprint(json.dumps(User.model_json_schema(), indent=2))\n# {'properties': {'name': {...}}, 'required': ['name', 'age'], ...}",
        "usecase": "Feeding type-safe schemas to API documentation and client generators — one source of truth for both validation and the docs your consumers read.",
        "category": "pydantic"
    },
    {
        "id": 41,
        "title": "Pydantic dataclasses add validation",
        "definition": "@pydantic.dataclasses.dataclass wraps the stdlib dataclass machinery with Pydantic validation: the same coercion, constraints, validators and serialization apply to a plain dataclass style API. It's the on-ramp for existing dataclass-heavy codebases that want validation without migrating to BaseModel everywhere.",
        "example": "from pydantic.dataclasses import dataclass\n\n@dataclass\nclass User:\n    name: str\n    age: int\n\nu = User(name=\"Ada\", age=\"37\")   # coerced to int\nbad = User(name=1, age=37)         # ValidationError",
        "usecase": "Adding type-safe validation to existing dataclass-based code incrementally — the annotation stays, the runtime checks come for free.",
        "category": "pydantic"
    },
    {
        "id": 42,
        "title": "BaseSettings loads config from everywhere",
        "definition": "pydantic-settings' BaseSettings reads environment variables, .env files, dotenv, vault and secrets into typed, validated settings — with sensible defaults and validation errors on missing required values. Each setting is a typed field, so GITHUB_TOKEN, DATABASE_URL and friends are validated and coerced like any other model.",
        "example": "# .env\n# DATABASE_URL=postgresql://user:pass@db:5432/app\n\nfrom pydantic_settings import BaseSettings, SettingsConfigDict\n\nclass Settings(BaseSettings):\n    model_config = SettingsConfigDict(env_file=\".env\")\n    database_url: str\n    debug: bool = False\n\ns = Settings()\ns.database_url  # loaded from the environment",
        "usecase": "Centralizing environment configuration in one typed object — validated at startup, documented by annotations, loaded from env or .env without boilerplate.",
        "category": "pydantic"
    },
    {
        "id": 43,
        "title": "Discriminated unions by field value",
        "definition": "A discriminated union validates by a single tag field before trying branches: payload = Annotated[Union[Create, Update], Field(discriminator=\"type\")] picks the branch whose tag matches. Instead of trying each branch and taking the first that works, Pydantic routes instantly on the tag value — faster and much more predictable.",
        "example": "from pydantic import BaseModel, Field\nfrom typing import Annotated, Union, Literal\n\nclass Create(BaseModel):\n    type: Literal[\"create\"]\n    name: str\n\nclass Update(BaseModel):\n    type: Literal[\"update\"]\n    patch: dict\n\nEvent = Annotated[Union[Create, Update], Field(discriminator=\"type\")]",
        "usecase": "Modeling polymorphic API payloads — websocket events, webhook variants, message types — routed deterministically on a tag field instead of trial-and-error validation.",
        "category": "pydantic"
    },
    {
        "id": 44,
        "title": "Strict mode turns off coercion",
        "definition": "By default Pydantic is lax: '37' becomes 37, True becomes 1, '2026-01-01' becomes a date. Strict mode rejects all coercion — an int field accepts only a real int. Set strict=True per field, per TypeAdapter, or via ConfigDict(strict=True) when data must arrive exactly as typed.",
        "example": "from pydantic import BaseModel, ConfigDict\n\nclass StrictModel(BaseModel):\n    model_config = ConfigDict(strict=True)\n    count: int\n\nStrictModel(count=5)        # ok\nStrictModel(count=\"5\")      # ValidationError: Input should be a valid integer",
        "usecase": "Trust boundaries where silent coercion hides bugs — protocol parsers, exact-value configs, and tests that should fail loudly when the input type changes.",
        "category": "pydantic"
    },
    {
        "id": 45,
        "title": "Annotated carries constraints with the type",
        "definition": "Annotated[type, Field(...)] embeds constraints directly in the annotation, so the validated type is reusable: UserId = Annotated[int, Field(gt=0)] can be used in a hundred models. This is the modern replacement for conint/constr — the constraint becomes part of the type's identity, visible to editors and to other Annotated compositions.",
        "example": "from pydantic import BaseModel, Field\nfrom typing import Annotated\n\nUserId = Annotated[int, Field(gt=0, description=\"Positive user id\")]\nPositiveInt = Annotated[int, Field(gt=0)]\n\nclass Post(BaseModel):\n    author: UserId\n    views: PositiveInt = 0",
        "usecase": "Defining domain types once — UserId, Email, Slug — and reusing them across every model so constraints stay DRY and consistent project-wide.",
        "category": "pydantic"
    },
    {
        "id": 46,
        "title": "model_fields introspects the schema",
        "definition": "model_fields gives you a dict of FieldInfo objects describing every field — name, annotation, required, default, metadata — letting you introspect a model at runtime to build forms, tables or generic serializers. Combined with model_json_schema it's the reflection layer for writing framework-like code that adapts to any model.",
        "example": "from pydantic import BaseModel\n\nclass User(BaseModel):\n    name: str\n    age: int = 18\n\nfor fname, info in User.model_fields.items():\n    print(fname, info.annotation, info.is_required())\n# name <class 'str'> True\n# age <class 'int'> False",
        "usecase": "Building generic UIs and tooling — dynamic forms, CSV exporters, diff tools — that render any model without hand-writing each field's metadata.",
        "category": "pydantic"
    },
    {
        "id": 47,
        "title": "validate_default catches bad defaults",
        "definition": "Setting ConfigDict(validate_default=True) makes Pydantic validate the default value of each field when the default is used, in addition to validating provided input. A typo in a default — like retries = \"3\" as a string for an int field — is then caught at instantiation instead of silently becoming dead configuration.",
        "example": "from pydantic import BaseModel, ConfigDict\n\nclass Cfg(BaseModel):\n    model_config = ConfigDict(validate_default=True)\n    retries: int = 3\n    name: str = \"svc\"\n\n# a default of \"3\" (string) would now raise instead of passing silently",
        "usecase": "Adding safety to long-lived configuration models where defaults are as critical as inputs — misconfigured defaults fail at startup, not in production.",
        "category": "pydantic"
    },
    {
        "id": 48,
        "title": "Pydantic is fast thanks to Rust",
        "definition": "Pydantic v2 moved validation into pydantic-core, a Rust implementation, making model construction and validation anywhere from 5 to 50 times faster than the pure-Python v1. The Python layer handles schema building and you keep the ergonomics; the hot path — parsing, coercing, error collection — runs in compiled code.",
        "example": "import time\nfrom pydantic import BaseModel\n\nclass Item(BaseModel):\n    name: str\n    price: float\n\nitems = [Item(name=\"x\", price=1.0) for _ in range(100_000)]\n# v2: tens of ms for 100k validated instances\n# v1: often a second or more for the same loop",
        "usecase": "Validating high-throughput payloads — message queues, webhooks, ETL batches — where per-item validation cost directly shapes your pipeline's throughput.",
        "category": "pydantic"
    },
    {
        "id": 49,
        "title": "Validators compose with typing machinery",
        "definition": "Pydantic validators play nicely with the full typing toolbox: Annotated can stack multiple Field entries, Pattern validates with re.compile, and custom Annotated types combine BeforeValidator and AfterValidator transforms from pydantic.functional_validators. You build validation from small, composable pieces instead of one giant method.",
        "example": "from typing import Annotated\nfrom pydantic import BaseModel, BeforeValidator, AfterValidator\n\ndef to_int(v):\n    return int(v)\n\ndef check_positive(v):\n    assert v > 0, \"must be positive\"\n    return v\n\nCount = Annotated[int, BeforeValidator(to_int), AfterValidator(check_positive)]\n\nclass Item(BaseModel):\n    qty: Count\n\nItem(qty=\"5\").qty  # 5 — string normalized then range-checked",
        "usecase": "Reusing transform pipelines across models — normalize, then constrain — so the same input-cleaning logic never gets copy-pasted into per-field methods.",
        "category": "pydantic"
    },
    {
        "id": 50,
        "title": "Upgrade to v2 is mechanical",
        "definition": "The big v1-to-v2 changes: .dict()/.json() become .model_dump()/.model_dump_json(), .parse_obj()/.parse_raw() become .model_validate()/.model_validate_json(), and @validator becomes @field_validator with @classmethod. ConfigDict replaces the class Config, and Optional fields with default None are fine. The migration guide covers each rename one-to-one, so moving is mostly mechanical search-and-replace.",
        "example": "from pydantic import BaseModel\n\nclass User(BaseModel):\n    name: str\n    age: int = 0\n\nu = User(name=\"Ada\")\nu.model_dump()            # v2 (was u.dict())\nUser.model_validate({})   # v2 (was User.parse_obj({}))",
        "usecase": "Modernizing existing v1 codebases — most calls map 1:1 to the v2 names, giving the Rust-speed engine with roughly search-and-replace effort.",
        "category": "pydantic"
    },
]
