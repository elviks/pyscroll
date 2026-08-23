TIPS = [
    {
        "id": 1,
        "title": "Swap two variables",
        "definition": "Python lets you exchange the values of two variables in a single line, no temporary variable required. It works through tuple unpacking: the right side of the assignment builds a tuple from the current values, and the left side unpacks it straight back into the variables in reverse order. It is one of the most instantly recognizable and elegant Python idioms.",
        "example": "a = 5\nb = 10\na, b = b, a      # a becomes 10, b becomes 5\nprint(a, b)      # 10 5",
        "usecase": "Real code swaps values everywhere: rotating buffer positions, exchanging columns of a data grid, or implementing sorting steps that swap adjacent items during a pass.",
        "category": "idioms"
    },
    {
        "id": 2,
        "title": "F-strings are your friend",
        "definition": "F-strings (formatted string literals) are the modern and fastest way to build strings that include variables or expressions. You prefix the string with f and wrap any expression in curly braces — Python evaluates it inline and formats the result. They read naturally, run quickly, and support format specifiers for precision, padding and alignment.",
        "example": "name = \"Ada\"\nage = 36\nprint(f\"Hello, {name}! You are {age} years old.\")\nload = 73.456\nprint(f\"CPU load: {load:.1f}%\")   # CPU load: 73.5%",
        "usecase": "Logging user activity, composing API error messages, or rendering live monitoring stats — anywhere you used to juggle % formatting or .format() chaining.",
        "category": "strings"
    },
    {
        "id": 3,
        "title": "enumerate() instead of range(len())",
        "definition": "When you loop over a sequence you usually need the items together with their positions. enumerate() hands you exactly that pairing, eliminating index bookkeeping and the clunky range(len()) pattern. The optional start parameter lets you number from 1 instead of 0, which is often exactly what users want to see.",
        "example": "tasks = [\"write report\", \"review PR\", \"deploy\"]\nfor i, task in enumerate(tasks, start=1):\n    print(f\"{i}. {task}\")",
        "usecase": "Numbering rows for a CSV export or a CLI checklist, or attaching positions to leaderboard entries so ties keep a stable, human-visible order.",
        "category": "iterables"
    },
    {
        "id": 4,
        "title": "List comprehensions",
        "definition": "A list comprehension builds a new list from an iterable in a single compact expression. The syntax reads almost like English — 'take x for every x in that sequence, if it passes this condition'. A handy rule of thumb: if you find yourself writing a for loop that only appends to a list, a comprehension is almost always cleaner and faster.",
        "example": "nums = [1, 2, 3, 4, 5, 6]\nsquares = [x * x for x in nums if x % 2 == 0]\nprint(squares)   # [4, 16, 36]",
        "usecase": "Sanitizing user input in bulk — stripping whitespace from every field of a form, or filtering a scraped contact list down to valid email addresses before saving.",
        "category": "idioms"
    },
    {
        "id": 5,
        "title": "The walrus operator",
        "definition": "The walrus operator (:=), introduced in Python 3.8, assigns a value to a name and returns that value in the same expression. It shines wherever you need a computed result both in a condition and in the code that follows, so you never compute it twice. Use it sparingly — readable code beats clever code.",
        "example": "with open(\"data.bin\", \"rb\") as f:\n    while chunk := f.read(1024):\n        process(chunk)",
        "usecase": "Reading a file in chunks, parsing a value once and reusing it inside the loop body, or checking a memoized lookup result and returning it in the same breath.",
        "category": "syntax"
    },
    {
        "id": 6,
        "title": "dict.get() never raises",
        "definition": "dict.get() is the safe way to look up a key: instead of raising KeyError when the key is missing, it returns the default you supply — or None if you do not supply one. That single method eliminates an entire category of crash-before-you-handle-it bugs in configuration and data processing code.",
        "example": "settings = {\"theme\": \"dark\", \"sound\": True}\ntheme = settings.get(\"theme\", \"light\")   # \"dark\"\nfont = settings.get(\"font\", \"sans\")      # \"sans\" — key absent",
        "usecase": "Reading optional settings from a config dict where every missing key should silently fall back to a sensible default rather than crash the application at startup.",
        "category": "dicts"
    },
    {
        "id": 7,
        "title": "setdefault for nested dicts",
        "definition": "setdefault(key, default) returns the value for a key if it exists and inserts the default otherwise. This makes it the perfect tool for building nested structures like dicts of lists or dicts of dicts, without pre-creating every key by hand before filling it.",
        "example": "by_first_letter = {}\nfor word in [\"apple\", \"avocado\", \"banana\"]:\n    by_first_letter.setdefault(word[0], []).append(word)\n# {'a': ['apple', 'avocado'], 'b': ['banana']}",
        "usecase": "Grouping transactions by day, words by first letter, or log entries by error code — any index you build from a stream of records where you meet each key for the first time.",
        "category": "dicts"
    },
    {
        "id": 8,
        "title": "Sort with a key",
        "definition": "sorted() and list.sort() accept a key function that computes a value for each item; sorting happens on those computed values while the items themselves stay untouched. With a lambda it becomes one line to sort by an attribute, a dict field, or any derived quantity — ascending or descending with reverse=True.",
        "example": "users = [{\"name\": \"Ana\", \"age\": 30}, {\"name\": \"Bob\", \"age\": 25}]\nusers.sort(key=lambda u: u[\"age\"], reverse=True)\nprint(users)   # oldest first",
        "usecase": "Ranking a leaderboard by score, ordering files by size before a disk cleanup, or sorting orders by timestamp for a chronological timeline render.",
        "category": "sorting"
    },
    {
        "id": 9,
        "title": "zip() pairs lists",
        "definition": "zip() pairs up elements from two or more sequences position by position, producing tuples: first elements together, then the seconds, and so on. It stops at the shortest input, so mismatched lengths never crash your code. It is the standard tool for walking parallel data side by side.",
        "example": "names = [\"Ana\", \"Bo\", \"Cy\"]\nscores = [88, 92, 79]\nfor name, score in zip(names, scores):\n    print(f\"{name}: {score}\")",
        "usecase": "Merging column headers with row values to emit CSV lines, pairing product IDs with their prices, or zipping two sensor channels together before plotting.",
        "category": "iterables"
    },
    {
        "id": 10,
        "title": "*args and **kwargs",
        "definition": "*args collects whatever extra positional arguments a function receives into a tuple named args; **kwargs collects the extra keyword arguments into a dict. Together they let functions accept an open-ended set of arguments and forward them elsewhere — the foundation of decorators, wrappers and plugin systems.",
        "example": "def log(level, *args, **kwargs):\n    print(level, args, kwargs)\n\nlog(\"INFO\", \"user\", \"logged in\", user_id=42)\n# INFO ('user', 'logged in') {'user_id': 42}",
        "usecase": "Writing a decorator that forwards any arguments to the wrapped function, or a logging wrapper that accepts the same parameters as the underlying library without knowing its signature.",
        "category": "functions"
    },
    {
        "id": 11,
        "title": "Default args are evaluated once",
        "definition": "Default argument values in Python are evaluated once, at function definition time — not once per call. If the default is mutable (a list or dict), every call shares the same object, and mutations leak between calls. The fix is the None-sentinel pattern: default to None and build a fresh container inside the function body.",
        "example": "def add_item(item, cache=None):\n    if cache is None:\n        cache = []\n    cache.append(item)\n    return cache",
        "usecase": "Accumulator functions, handlers collecting state across requests, or anything that builds a fresh list per call — the classic bug surfaces intermittently in production and nowhere in the tests.",
        "category": "gotchas"
    },
    {
        "id": 12,
        "title": "String methods you forget",
        "definition": "The str type ships a complete toolbox for everyday text work: strip() removes surrounding whitespace, split() breaks text on a separator, join() merges a sequence into a string, and replace(), startswith() and endswith() cover most of the rest. For common tasks these built-ins are faster and far clearer than reaching for regex.",
        "example": "csv_line = \" alice, bob , carol \"\nnames = [n.strip() for n in csv_line.split(\",\")]\nprint(\",\".join(names))   # \"alice,bob,carol\"",
        "usecase": "Cleaning user-entered text before storing it, parsing comma-separated log lines into fields, or joining path segments into one filesystem path.",
        "category": "strings"
    },
    {
        "id": 13,
        "title": "Ternary expressions",
        "definition": "The ternary expression (x if condition else y) is Python's inline if/else that returns a value. It is perfect for short either-or choices where a full if/else block would add noise. Keep it readable: reserve the ternary for simple branches and short expressions.",
        "example": "n = 7\nlabel = \"even\" if n % 2 == 0 else \"odd\"\nprint(label)   # \"odd\"",
        "usecase": "Picking a display label, toggling a flag, or choosing between two message templates from a single quick condition — without the ceremony of a multi-line if/else.",
        "category": "idioms"
    },
    {
        "id": 14,
        "title": "any() and all()",
        "definition": "any() returns True when at least one item in an iterable is truthy; all() returns True only when every item is. Both short-circuit — they stop evaluating as soon as the outcome is decided — which keeps them fast even on huge sequences. The common pattern hands them a generator of boolean checks.",
        "example": "scores = [55, 72, 88, 41]\nall_passed = all(s >= 50 for s in scores)     # False\ndid_any_fail = any(s < 50 for s in scores)    # True",
        "usecase": "Validating that every field of a form is filled, checking whether any task in a batch job failed, or running a health check over a list of services before reporting 'healthy'.",
        "category": "builtins"
    },
    {
        "id": 15,
        "title": "Comprehensions over dicts and sets",
        "definition": "The comprehension syntax that builds lists also builds dicts and sets — just change the braces and the expression. Use a key: value expression inside curly braces for a dict, or a plain expression for a set. Both support the same mapping, filtering and unpacking tricks as list comprehensions.",
        "example": "nums = [1, 2, 3, 4]\nsquared = {x: x * x for x in nums}            # {1: 1, 2: 4, 3: 9, 4: 16}\nevens = {x for x in nums if x % 2 == 0}      # {2, 4}",
        "usecase": "Building a lookup table mapping IDs to display names straight from a database result, or deduplicating IDs collected across several data sources in one expression.",
        "category": "idioms"
    },
    {
        "id": 16,
        "title": "is vs ==",
        "definition": "The == operator compares values; the is operator compares object identity — whether two names refer to the very same object. For None, True and False, use is, because those singletons have exactly one canonical object. Comparing numbers with is is a trap: small ints are cached and happen to work, but larger ones don't.",
        "example": "x = None\nif x is None:      # idiomatic, always correct\n    handle_missing()\n# if x == None:    # works, but frowned upon",
        "usecase": "Checking whether an API field is missing (x is None) instead of risking a misleading comparison — especially with JSON payloads where null decodes to None and must not be confused with False or 0.",
        "category": "gotchas"
    },
    {
        "id": 17,
        "title": "Truthiness",
        "definition": "Every Python object has a truth value: empty collections — lists, dicts, sets, strings — as well as 0, None and False are falsy; everything else is truthy. That means conditions test emptiness and presence directly, without comparing lengths or writing explicit boolean conversions. The code reads like English.",
        "example": "cart = []\nif cart:            # falsy → skip checkout\n    process(cart)\nif value is not None:\n    render(value)",
        "usecase": "Checking whether a shopping cart has items before checkout, or whether a search returned any results before rendering a results page — no len() calls in the condition.",
        "category": "idioms"
    },
    {
        "id": 18,
        "title": "Unpacking with *",
        "definition": "The * operator plays two roles in unpacking: in assignments it captures 'everything between the named parts' into a list (first, *middle, last), and in function calls it spreads a sequence into positional arguments (func(*args)). The ** variant spreads a dict into keyword arguments.",
        "example": "nums = [1, 2, 3, 4, 5]\nfirst, *middle, last = nums\nprint(first, middle, last)   # 1 [2, 3, 4] 5\nprint(*middle)               # 2 3 4",
        "usecase": "Splitting a CSV row into its header cell and the remaining columns, or passing a variable-length list of arguments straight into a function call without indexing.",
        "category": "syntax"
    },
    {
        "id": 19,
        "title": "dict unpacking merge",
        "definition": "Dicts merge with {**a, **b}, where later dicts win on duplicate keys; since Python 3.9 the | operator does exactly the same thing, and |= merges in place. Merging is shallow — nested containers are shared, not copied — so it is safest for flat configuration data.",
        "example": "defaults = {'retries': 3, 'timeout': 30, 'cache': True}\noverrides = {'timeout': 10}\nconfig = {**defaults, **overrides}\n# {'retries': 3, 'timeout': 10, 'cache': True}",
        "usecase": "Applying user overrides on top of default configuration before a service starts — the classic merge that must never mutate the defaults dict.",
        "category": "dicts"
    },
    {
        "id": 20,
        "title": "Generators save memory",
        "definition": "A generator produces values one at a time as you iterate, instead of materializing the entire sequence in memory. Parenthesized generator expressions and yield-based generator functions both hand values back lazily. For huge or infinite data, that is often the difference between a fast pipeline and a machine that swaps to disk.",
        "example": "squares = (x * x for x in range(10_000_000))\nprint(sum(squares))   # no 10-million-element list exists",
        "usecase": "Streaming millions of log lines or API pages through a processing pipeline without ever loading them all at once — memory stays flat while the data keeps flowing.",
        "category": "performance"
    },
    {
        "id": 21,
        "title": "yield makes iterators",
        "definition": "Any function that contains yield turns into a generator: calling it creates a generator object, and each next() or loop iteration resumes the function until the next yield. Execution is lazy and stateful — local variables persist between yields. This is how Python implements infinite sequences and on-demand pipelines idiomatically.",
        "example": "def fibonacci():\n    a, b = 0, 1\n    while True:\n        yield a\n        a, b = b, a + b\n\nfor n in fibonacci():\n    if n > 100:\n        break\n    print(n)",
        "usecase": "Pagination loops that fetch one page of results at a time as the consumer asks, or sensor streams where buffering an unbounded amount of data is simply not an option.",
        "category": "functions"
    },
    {
        "id": 22,
        "title": "The with statement",
        "definition": "The with statement binds a resource and guarantees its cleanup — files close, locks release, sessions end — even when the body raises an exception. It works with any object implementing the context manager protocol, from files and sockets to threading locks and database connections.",
        "example": "with open(\"data.txt\") as f:\n    content = f.read()\n# the file is guaranteed closed here, no matter what happened above",
        "usecase": "Managing files, database connections or threading.Lock so resources never leak when a mid-operation error throws — the difference between healthy services and file-descriptor exhaustion.",
        "category": "syntax"
    },
    {
        "id": 23,
        "title": "Don't build lists by hand",
        "definition": "list(iterable) materializes any iterable into a list in one call, and set(), tuple() and dict() do the same for their types. There is almost never a reason to append in a loop to build a collection from something iterable — the constructors handle strings, ranges, file lines, dict keys and generator output.",
        "example": "chars = list('hello')           # ['h', 'e', 'l', 'l', 'o']\nlines = list(open('data.txt'))   # one string per line",
        "usecase": "Turning a file's lines into a list for random access, or converting a set of unique tags into an ordered list for display — no manual loops, no append calls.",
        "category": "builtins"
    },
    {
        "id": 24,
        "title": "functools.lru_cache",
        "definition": "functools.lru_cache memoizes a pure function: results are keyed by arguments and reused on repeat calls, trading a little memory for enormous speedups. maxsize caps the cache (None means unbounded). The function must be pure and its arguments hashable — that is the only contract.",
        "example": "from functools import lru_cache\n\n@lru_cache(maxsize=128)\ndef fib(n):\n    return n if n < 2 else fib(n - 1) + fib(n - 2)\n\nprint(fib(100))   # fast after first warm-up",
        "usecase": "Caching expensive database lookups keyed by ID, or memoizing heavy math inside a request handler that keeps receiving the same arguments across users.",
        "category": "performance"
    },
    {
        "id": 25,
        "title": "collections.Counter",
        "definition": "collections.Counter is a dict subclass that counts hashable items: counting happens automatically on construction, and most_common(), arithmetic between counters, and update() make frequency analysis a few lines instead of a loop with setdefault.",
        "example": "from collections import Counter\n\ntext = \"the cat and the dog and the bird\"\ncounts = Counter(text.split())\nprint(counts.most_common(2))   # [('the', 3), ('and', 2)]",
        "usecase": "Word-frequency analysis, counting error types in application logs, or ranking tags by popularity for a tag cloud — the one-liner replacement for manual counting dicts.",
        "category": "stdlib"
    },
    {
        "id": 26,
        "title": "defaultdict",
        "definition": "defaultdict is a dict that calls a factory function whenever you access a missing key, creating and inserting the default on the spot. Missing-key lookups never raise KeyError, which makes grouping and counting code dramatically shorter and safer.",
        "example": "from collections import defaultdict\n\norders_by_city = defaultdict(list)\norders_by_city[\"paris\"].append(123)   # the list is created automatically",
        "usecase": "Grouping orders by customer ID, counting inventory per SKU, or mapping departments to employees — without pre-creating every key or wrapping every append in a check.",
        "category": "stdlib"
    },
    {
        "id": 27,
        "title": "Type hints",
        "definition": "Type hints annotate argument and return types so tools — mypy, pyright, IDEs — can check your code before it runs. They are optional at runtime, but they document intent, catch whole classes of bugs, and make large-scale refactors dramatically safer.",
        "example": "def add(a: int, b: int) -> int:\n    return a + b",
        "usecase": "Large codebases and teams where mypy/pyright catch type mismatches at CI time instead of exploding in production, and where signatures double as documentation.",
        "category": "typing"
    },
    {
        "id": 28,
        "title": "functools.partial",
        "definition": "functools.partial locks in some arguments of an existing function and returns a new callable with the rest still open. The bound arguments are stored with the partial, so it can be passed around anywhere the full signature doesn't fit — no wrapper functions required.",
        "example": "from functools import partial\n\ndef power(base, exp):\n    return base ** exp\n\nsquare = partial(power, exp=2)\nprint(square(5))   # 25",
        "usecase": "Pre-binding arguments for multiprocessing.Pool workers or callbacks that accept exactly one argument, and configuring library calls once at startup for reuse throughout the app.",
        "category": "stdlib"
    },
    {
        "id": 29,
        "title": "Avoid bare except",
        "definition": "A bare except: catches every exception — including KeyboardInterrupt and SystemExit — and silently disguises real bugs as 'handled'. Catch specific exception types instead, and where a broad handler is genuinely needed, catch Exception and re-raise what you can't deal with.",
        "example": "raw = input(\"enter a number: \")\ntry:\n    n = int(raw)\nexcept ValueError:\n    print(\"that is not a number\")",
        "usecase": "Parsing user input where only ValueError should be handled — so genuine bugs like a missing import or a broken function surface loudly instead of being swallowed.",
        "category": "gotchas"
    },
    {
        "id": 30,
        "title": "raise from",
        "definition": "raise X from Y attaches the original exception to the new one as its __cause__, so the traceback shows the full chain of failure. When you wrap a low-level error into a higher-level one — for example a database error into an API error — the original cause stays visible for debugging.",
        "example": "try:\n    connect_db()\nexcept ConnectionError as e:\n    raise RuntimeError(\"database unavailable\") from e",
        "usecase": "Wrapping database or network errors into service-level errors in API code, so callers see a meaningful message and engineers still get the original traceback in production logs.",
        "category": "exceptions"
    },
    {
        "id": 31,
        "title": "String methods vs re",
        "definition": "For simple text checks — prefixes, suffixes, substrings, character whitelists — string methods like startswith, endswith, find and in are faster and far more readable than regular expressions. Reach for the re module only when you genuinely need patterns: alternations, captures or repetition.",
        "example": "if filename.startswith(\"report_\") and filename.endswith(\".csv\"):\n    process_report(filename)",
        "usecase": "Filtering uploaded filenames by prefix and extension, routing by URL prefix in a handler, or validating file types in a batch job — all without a regex in sight.",
        "category": "strings"
    },
    {
        "id": 32,
        "title": "Global keyword",
        "definition": "Assignment inside a function creates a local variable by default. The global statement declares that a name lives at module level, so assignments target it instead. Global mutable state is easy to overuse — a class or closure is usually better — but for a simple counter or flag in a small script it is exactly right.",
        "example": "count = 0\n\ndef bump():\n    global count\n    count += 1",
        "usecase": "A simple module-wide counter or feature flag in a small script; as soon as the program grows, replace it with a class attribute or a closure to keep state contained.",
        "category": "gotchas"
    },
    {
        "id": 33,
        "title": "Nonlocal for closures",
        "definition": "In nested functions, nonlocal lets an inner function rebind a name from an enclosing scope — the 'closure state' pattern. Unlike global, it stays scoped to the outer function, so each call to the outer function produces its own independent state.",
        "example": "def make_counter():\n    n = 0\n    def count():\n        nonlocal n\n        n += 1\n        return n\n    return count\n\nc = make_counter()\nprint(c(), c())   # 1 2",
        "usecase": "Writing counters, debouncers, or stateful decorators built from nested functions instead of small classes — one closure instead of a class definition.",
        "category": "functions"
    },
    {
        "id": 34,
        "title": "str.translate for fast cleaning",
        "definition": "str.translate() with a table built by str.maketrans() removes or maps characters in a single C-speed pass. For stripping punctuation or mapping characters, it outruns regex-based cleaning by a wide margin on large texts — the standard tool for bulk character filtering.",
        "example": "table = str.maketrans(\"\", \"\", \"!?.,\")\nclean = \"Hello, world!\".translate(table)   # \"Hello world\"",
        "usecase": "Sanitizing millions of chat messages or product reviews by stripping punctuation before frequency analysis — the kind of cleanup that must run in seconds, not minutes.",
        "category": "performance"
    },
    {
        "id": 35,
        "title": "Ellipsis as placeholder",
        "definition": "The ellipsis literal ... is a valid expression anywhere, which makes it a natural placeholder body for functions and classes you intend to implement later. The module imports and runs — the functions just do nothing yet — and reviewers immediately see what's outstanding.",
        "example": "def send_email(to, subject, body): ...\ndef apply_discount(price): ...",
        "usecase": "Stubbing out function bodies during a heavy refactor so the module still imports cleanly and the test suite keeps running, showing exactly what remains to be implemented.",
        "category": "syntax"
    },
    {
        "id": 36,
        "title": "Negative indexing",
        "definition": "Negative indices count backwards from the end of a sequence: items[-1] is the last element, items[-2] the second-to-last. Combined with slicing, this is the standard way to reach the tail of lists, strings and tuples without computing lengths.",
        "example": "history = [\"v1\", \"v2\", \"v3\"]\nlatest = history[-1]     # \"v3\"\nsecond = history[-2]     # \"v2\"",
        "usecase": "Grabbing the newest log entry, the latest order recorded in a list, or the most recent reading from a sensor buffer — no len()-1 arithmetic anywhere.",
        "category": "sequences"
    },
    {
        "id": 37,
        "title": "Slicing basics",
        "definition": "Slicing selects a range of a sequence with [start:stop:step] and always returns a new object, leaving the original untouched. Start and stop are optional, and a negative step reverses direction — which makes items[::-1] the canonical one-liner for reversal.",
        "example": "items = [0, 1, 2, 3, 4, 5]\nitems[1:4]    # [1, 2, 3]\nitems[::2]    # [0, 2, 4]\nitems[::-1]   # [5, 4, 3, 2, 1, 0]",
        "usecase": "Paging query results as rows[start:stop], reversing chat history for newest-first display, or previewing the first sentence of an article.",
        "category": "sequences"
    },
    {
        "id": 38,
        "title": "min/max with key",
        "definition": "min and max accept an optional key function, comparing items by a computed value instead of by the items directly. They return the winning item itself — no sorting, no extraction dance, just the extreme element of the collection.",
        "example": "products = [{\"name\": \"A\", \"price\": 12}, {\"name\": \"B\", \"price\": 9}]\ncheapest = min(products, key=lambda p: p[\"price\"])\n# {\"name\": \"B\", \"price\": 9}",
        "usecase": "Finding the most expensive item in a cart, the hottest city in a climate dataset, or the largest file in a directory scan — without sorting the whole collection.",
        "category": "builtins"
    },
    {
        "id": 39,
        "title": "itertools is gold",
        "definition": "itertools is the standard library's toolbox of lazy iterable combinators: chain flattens sequences, groupby clusters consecutive equal items, product enumerates combinations, and permutations, cycle and islice cover the rest. Everything is lazy, so the combinators scale to arbitrarily large inputs.",
        "example": "from itertools import chain, product\nflat = list(chain([1, 2], [3, 4]))       # [1, 2, 3, 4]\npairs = list(product(\"ab\", [1, 2]))     # [('a', 1), ('a', 2), ('b', 1), ('b', 2)]",
        "usecase": "Flattening nested query results, generating test-case combinations for parametrized suites, or grouping sorted rows into report sections.",
        "category": "stdlib"
    },
    {
        "id": 40,
        "title": "Check membership with in",
        "definition": "The in operator checks membership; its cost depends entirely on the container. Sets and dicts give O(1) hash lookups; lists and tuples scan linearly. Choosing set membership over list scanning in a hot loop is often the single biggest performance win available with one line of code.",
        "example": "allowed = {\"admin\", \"editor\", \"viewer\"}\nif role in allowed:        # O(1) hash lookup\n    grant_access(role)\n# if role in [\"admin\", ...]:   # O(n) linear scan",
        "usecase": "Permission checks, duplicate filters or validation inside loops processing millions of rows — swap the list for a set and the whole loop accelerates by orders of magnitude.",
        "category": "performance"
    },
    {
        "id": 41,
        "title": "Never name a file 'test.py' at root",
        "definition": "A local file that shadows a standard-library module name — test.py, math.py, json.py — hijacks imports in confusing ways: 'import test' may resolve to your file in one environment and the stdlib in another. Name modules after their purpose and you never fight Python's resolution order.",
        "example": "import test  # ambiguous: your file or the stdlib?",
        "usecase": "Naming real modules meaningfully so collisions with the standard library never bite a growing codebase, a CI environment, or a notebook that runs elsewhere.",
        "category": "gotchas"
    },
    {
        "id": 42,
        "title": "Print debugging with repr",
        "definition": "repr() renders a string as it would appear in code — with quotes and visible escapes — while str() shows the human-friendly form. When debugging what a value actually contains, print(repr(x)) reveals trailing whitespace, embedded newlines and encoding artifacts that print() hides from you.",
        "example": "value = \"hello\\nworld \"\nprint(value)        # newline rendered, trailing space invisible\nprint(repr(value))  # 'hello\\nworld '",
        "usecase": "Diagnosing why a string comparison fails, or spotting stray whitespace and newlines in parsed CSV or JSON payloads that look identical on screen.",
        "category": "debugging"
    },
    {
        "id": 43,
        "title": "The debugger is your friend",
        "definition": "breakpoint() drops you into an interactive debugger (pdb by default) at exactly that line of code. From there you can step through statements, inspect locals, evaluate expressions and continue — the built-in alternative to sprinkle-then-remove print statements.",
        "example": "def process(data):\n    total = sum(data)\n    breakpoint()      # pdb prompt opens here\n    return total / len(data)",
        "usecase": "Stepping through a gnarly bug in a loop, inspecting variables at the exact moment they go wrong, and fixing the problem in one focused session.",
        "category": "debugging"
    },
    {
        "id": 44,
        "title": "Docstrings document",
        "definition": "A docstring — the first statement of a function, class or module — becomes __doc__, is shown by help(), and is read by IDEs, linters and documentation tools like Sphinx. It is the contract your code ships with, so it should describe intent, not restate the implementation.",
        "example": "def square(x):\n    \"\"\"Return the square of x.\"\"\"\n    return x * x\n\nhelp(square)",
        "usecase": "Making libraries self-documenting so future maintainers — and you in six months — understand intent without reading the implementation line by line.",
        "category": "style"
    },
    {
        "id": 45,
        "title": "Naming with underscores",
        "definition": "Underscore prefixes signal intent at a glance: ALL_CAPS names constants, _single_leading signals 'private' attributes, __double triggers name mangling inside classes, and a bare _ marks throwaway values. None of it is enforced — all of it is convention that readers rely on.",
        "example": "MAX_RETRIES = 3            # constant\n_connection = None          # module-internal\nfor _ in range(5):          # loop value unused\n    step()",
        "usecase": "Keeping large codebases readable, signalling which attributes libraries treat as internal, and making it obvious when a loop index is never used.",
        "category": "style"
    },
    {
        "id": 46,
        "title": "Sorted vs sort",
        "definition": "sorted() returns a new list and leaves the original untouched; list.sort() sorts in place and returns None. The classic bug — items = items.sort() — silently leaves items as None, and the pipeline keeps running with empty hands. When in doubt, prefer sorted().",
        "example": "ordered = sorted(items)   # new list, items untouched\nitems.sort()              # in place, returns None\n# NEVER: items = items.sort()  →  items becomes None",
        "usecase": "Sorting data for display while keeping the original order for further processing — without the None-assignment trap that corrupts state quietly.",
        "category": "gotchas"
    },
    {
        "id": 47,
        "title": "Dictionary order is insertion order",
        "definition": "Since Python 3.7, dicts preserve insertion order, so iteration is stable and deterministic: keys come back exactly as they were added. That stability is relied upon by JSON output ordering, UI registration and cache implementations everywhere.",
        "example": "d = {\"b\": 2, \"a\": 1}\nprint(list(d))     # ['b', 'a'] — insertion order\nd[\"c\"] = 3\nprint(list(d))     # ['b', 'a', 'c']",
        "usecase": "Rendering UI elements in the order they were registered, or emitting JSON files that diff cleanly between two versions of a service.",
        "category": "dicts"
    },
    {
        "id": 48,
        "title": "Map is meh, comprehensions rule",
        "definition": "map() applies a function to every item of an iterable, but comprehensions usually win on both speed and readability — especially when the function is a lambda. Reserve map for the rare case where a built-in function already exists and the intent is crystal clear.",
        "example": "nums = [1, 2, 3, 4]\ndoubled = list(map(lambda x: x * 2, nums))\ndoubled = [x * 2 for x in nums]      # clearer, often faster",
        "usecase": "Transforming data lists in ETL pipelines where readability matters more than cleverness — and where future editors shouldn't need to decode a lambda.",
        "category": "style"
    },
    {
        "id": 49,
        "title": "functools.reduce is rare",
        "definition": "reduce folds a sequence into a single value by repeatedly applying a two-argument function. In modern Python, sum(), max() and friends cover the common folds more clearly; reduce earns its keep only for genuinely custom combining logic.",
        "example": "from functools import reduce\ntotal = reduce(lambda a, b: a + b, [1, 2, 3, 4], 0)   # 10\n# simpler: total = sum([1, 2, 3, 4])",
        "usecase": "Building an OR-chain of conditions or computing a product with a non-trivial combining rule — the cases where sum() and friends aren't enough.",
        "category": "stdlib"
    },
    {
        "id": 50,
        "title": "Context of __main__",
        "definition": "A module executed as a script runs its top-level code; an imported module only defines names. The if __name__ == '__main__': guard keeps script-only logic — CLI parsing, main() — from firing on import, so the same file works both as a tool and as a library.",
        "example": "def main():\n    print(\"running as a script\")\n\nif __name__ == \"__main__\":\n    main()",
        "usecase": "The standard entry-point pattern: scripts that work as CLI tools when run directly, and stay import-safe for unit tests and reuse from other modules.",
        "category": "syntax"
    },
    {
        "id": 51,
        "title": "Shallow vs deep copy",
        "definition": "Copying a container is shallow by default: the outer object is new, but inner objects are shared with the original. copy.deepcopy() recursively duplicates everything, producing a fully independent structure. Which you need depends on whether mutating nested values is safe.",
        "example": "import copy\n\noriginal = {\"opts\": [1, 2]}\nshallow = original.copy()          # shares the [1, 2] list\ndeep = copy.deepcopy(original)\nshallow[\"opts\"].append(3)\nprint(original[\"opts\"])           # [1, 2, 3] — mutated through the copy!",
        "usecase": "Snapshotting a config dict before mutating it without corrupting the original defaults, or cloning a working structure so experiments never touch real data.",
        "category": "gotchas"
    },
    {
        "id": 52,
        "title": "Format specifiers",
        "definition": "The mini-language after the colon in f-strings and .format() controls precision, padding, alignment, sign and thousands separators. f\"{amount:.2f}\" rounds to two decimals; width specifiers align table columns without manual string surgery.",
        "example": "price = 12.5\nprint(f\"{price:.2f}\")     # 12.50\nprint(f\"{price:>8.1f}\")   # right-aligned, width 8: \"    12.5\"\nprint(f\"{123456:,}\")      # 123,456",
        "usecase": "Printing money amounts, aligning columns in report output, or zero-padding IDs and timestamps for filename generation.",
        "category": "strings"
    },
    {
        "id": 53,
        "title": "The else clause on loops",
        "definition": "A for or while loop's else clause runs only if the loop finished without break — the classic 'search failed' hook. It eliminates flag variables like found = False that you had to check after the loop.",
        "example": "for user in blocked_list:\n    if user == candidate:\n        break\nelse:\n    send_invite(candidate)   # never found → invite",
        "usecase": "Flagging when validation passes for every row of a batch, or searching an item across pages and acting only when it never appears.",
        "category": "syntax"
    },
    {
        "id": 54,
        "title": "dataclasses for data containers",
        "definition": "@dataclass generates __init__, __repr__, __eq__ and friends from your field annotations, so plain data containers stop needing boilerplate. Per-field options — defaults, factory functions, excluded-from-init flags — keep the class declarative and readable.",
        "example": "from dataclasses import dataclass\n\n@dataclass\nclass Order:\n    order_id: int\n    total: float\n    paid: bool = False",
        "usecase": "Modeling records like orders, users or coordinates across an app, with construction, printing, equality and comparison that just work out of the box.",
        "category": "stdlib"
    },
    {
        "id": 55,
        "title": "The match statement",
        "definition": "Structural pattern matching (Python 3.10+) dispatches on the shape of data with literal patterns, guards and extraction. It reads declaratively compared with chains of if/elif on types and structure — like a switch statement that can also unpack.",
        "example": "def handle(cmd):\n    match cmd.split():\n        case [\"quit\"]:\n            sys.exit(0)\n        case [\"open\", path]:\n            open_file(path)\n        case _:\n            print(\"unknown command\")",
        "usecase": "Parsing CLI commands, routing message types in a server, or destructuring API responses into named fields with one readable statement.",
        "category": "syntax"
    },
    {
        "id": 56,
        "title": "JSON built in",
        "definition": "The standard json module turns JSON text into Python structures (loads) and back (dumps) with zero external dependencies. It handles nesting, unicode and formatting options like indent, and it is the backbone of config files and web APIs in pure Python.",
        "example": "import json\n\ndata = json.loads('{\"name\": \"Ada\", \"age\": 36}')\nprint(data[\"age\"])\nwith open(\"out.json\", \"w\") as f:\n    json.dump(data, f, indent=2)",
        "usecase": "Reading config files, caching API responses to disk between runs, or exchanging data between services without pulling in a third-party library.",
        "category": "stdlib"
    },
    {
        "id": 57,
        "title": "pathlib over os.path",
        "definition": "pathlib's Path objects make filesystem work readable: paths compose with the / operator, and methods like read_text(), write_text(), glob() and mkdir(exist_ok=True) remove the fiddly string handling of os.path. Path code is also portable across operating systems.",
        "example": "from pathlib import Path\n\nreports = Path(\"reports\") / \"2026\" / \"aug\"\nfiles = list(reports.glob(\"*.csv\"))\nprint(reports.suffix, reports.stem)",
        "usecase": "Walking project directories, building backup filenames from dates, or writing portable path handling that works on Windows and Linux alike.",
        "category": "stdlib"
    },
    {
        "id": 58,
        "title": "Argument unpacking for calls",
        "definition": "In a function call, * spreads a sequence into positional arguments and ** spreads a dict into keyword arguments. Combined with *args/**kwargs parameters, this forms a complete forwarding system: parse arguments once at the boundary, pass everything through untouched.",
        "example": "def fetch(path, retries=3, timeout=10):\n    ...\n\nparams = {\"retries\": 1, \"timeout\": 5}\nfetch(\"/api/v1\", **params)",
        "usecase": "Forwarding dynamic arguments to third-party functions, or reusing parsed CLI options across several calls without enumerating each parameter by name.",
        "category": "syntax"
    },
    {
        "id": 59,
        "title": "Comparing floats",
        "definition": "Binary floats cannot represent most decimal fractions exactly, so 0.1 + 0.2 is not 0.3. Never test floats for equality directly; compare within a tolerance or use math.isclose(), which handles both absolute and relative error sensibly.",
        "example": "import math\n\na, b = 0.1 + 0.2, 0.3\nprint(a == b)             # False\nprint(math.isclose(a, b)) # True",
        "usecase": "Budget calculations, sensor thresholds or geometry code where a few ulps of rounding error must not decide pass/fail behind your back.",
        "category": "gotchas"
    },
    {
        "id": 60,
        "title": "Type hints with Optional",
        "definition": "For nullable values, Python 3.10+ lets you write str | None — a union type — replacing Optional[str]. It reads naturally, works as a runtime annotation, and expresses 'this value may be absent' in a single token that type checkers understand fully.",
        "example": "def find_user(name: str | None) -> dict | None:\n    if not name:\n        return None\n    return lookup(name)",
        "usecase": "Modelling nullable fields from databases or APIs in typed codebases, so every 'could be missing' path is explicit at the type level and checked by mypy.",
        "category": "typing"
    },
    {
        "id": 61,
        "title": "__init__ vs __new__",
        "definition": "__new__ creates the bare instance and must return it; __init__ then customizes that instance. For ordinary classes you only write __init__ — __new__ is for advanced cases like immutable types, singletons or metaclass plumbing.",
        "example": "class Point:\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y\n\np = Point(1, 2)\nprint(p.x)   # 1",
        "usecase": "Customizing instances on construction as every class does — override only __init__ and let the default __new__ handle creation, unless you're doing something genuinely advanced.",
        "category": "oop"
    },
    {
        "id": 62,
        "title": "__str__ vs __repr__",
        "definition": "__repr__ targets developers: it should be unambiguous and ideally eval-able back into an object. __str__ targets users: readable, pretty output. print() and f-strings use __str__; the interactive prompt and most logging use __repr__.",
        "example": "class Money:\n    def __init__(self, amount):\n        self.amount = amount\n    def __repr__(self):\n        return f\"Money({self.amount})\"\n    def __str__(self):\n        return f\"${self.amount:.2f}\"\n\nm = Money(12.5)\nprint(repr(m))   # Money(12.5)\nprint(str(m))    # $12.50",
        "usecase": "Logging objects faithfully in production trails (repr) while keeping user-facing output clean and human-friendly (str) — one class, two audiences.",
        "category": "oop"
    },
    {
        "id": 63,
        "title": "property() for computed attributes",
        "definition": "The @property decorator exposes a method as an attribute, optionally paired with @setter and @deleter for validation. Callers can't tell the difference between a stored field and a computed one — an implementation detail you can change later without breaking the API.",
        "example": "class Thermometer:\n    def __init__(self, celsius):\n        self._celsius = celsius\n\n    @property\n    def fahrenheit(self):\n        return self._celsius * 9 / 5 + 32\n\nt = Thermometer(100)\nprint(t.fahrenheit)   # 212.0 — attribute-like, no parentheses",
        "usecase": "Exposing stored degrees Celsius as Fahrenheit without callers knowing the conversion exists — and migrating from stored to computed fields without breaking API consumers.",
        "category": "oop"
    },
    {
        "id": 64,
        "title": "classmethod vs staticmethod",
        "definition": "classmethod receives the class itself as its first argument (cls), enabling factory constructors and subclass-aware behavior; staticmethod receives nothing and is just a namespaced helper. Both live on the class and are called without an instance.",
        "example": "class Date:\n    @classmethod\n    def today(cls):\n        return cls(2026, 8, 20)\n\n    @staticmethod\n    def is_leap(year):\n        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)",
        "usecase": "Factory constructors like Date.today() that stay correct for subclasses, and utility helpers that belong in a class's namespace but need no instance state.",
        "category": "oop"
    },
    {
        "id": 65,
        "title": "dataclasses.field with init=False",
        "definition": "dataclasses.field(init=False) creates an attribute that is not part of the constructor — it gets computed or stamped after construction instead. With default_factory you can auto-generate values like timestamps and IDs at instance creation time.",
        "example": "from dataclasses import dataclass, field\nfrom datetime import datetime\n\n@dataclass\nclass Order:\n    customer: str\n    created_at: datetime = field(default_factory=datetime.now, init=False)\n\no = Order(\"Ana\")\nprint(o.created_at)   # stamped automatically",
        "usecase": "Auto-stamping records with timestamps, UUIDs or derived balances without forcing callers to pass them — keeping constructors minimal and data consistent.",
        "category": "oop"
    },
    {
        "id": 66,
        "title": "__slots__ saves memory",
        "definition": "__slots__ declares the exact attribute names an instance may carry, replacing the per-instance __dict__ with a compact tuple of slots. Instances get smaller and attribute access gets faster — at the cost of forbidding any new attributes.",
        "example": "class Point:\n    __slots__ = (\"x\", \"y\")\n    def __init__(self, x, y):\n        self.x = x\n        self.y = y",
        "usecase": "Millions of small records in a memory-bound processing job, where the per-instance dict overhead adds gigabytes — slots shrink the memory footprint sharply.",
        "category": "oop"
    },
    {
        "id": 67,
        "title": "The GIL explained",
        "definition": "The Global Interpreter Lock lets only one thread run Python bytecode at a time — CPU-bound threads never get true parallelism. Threads still shine for I/O: while one thread waits on a socket or file, the lock releases and others run. Number crunching belongs in processes or compiled libraries.",
        "example": "# CPU-bound work: use multiprocessing or numpy\n# I/O-bound work: threads and async are fine\nimport threading\n\ndef fetch_all(urls):\n    with ThreadPoolExecutor(8) as pool:\n        return list(pool.map(download, urls))",
        "usecase": "Choosing multiprocessing for number crunching but threads for network requests, file I/O and sleeps — the GIL governs bytecode, not waiting.",
        "category": "concurrency"
    },
    {
        "id": 68,
        "title": "ThreadPoolExecutor",
        "definition": "concurrent.futures.ThreadPoolExecutor runs a function across a pool of threads, collecting results in input order via map(), or as they finish via submit() with as_completed(). It is the highest-level tool for parallel I/O in the standard library.",
        "example": "from concurrent.futures import ThreadPoolExecutor\n\nwith ThreadPoolExecutor(max_workers=8) as pool:\n    pages = list(pool.map(fetch_page, urls))",
        "usecase": "Downloading hundreds of URLs or querying a rate-limited API — overlapping the I/O waits instead of serializing them and paying full latency N times.",
        "category": "concurrency"
    },
    {
        "id": 69,
        "title": "queue.Queue for thread safety",
        "definition": "queue.Queue is a thread-safe FIFO: put() appends, get() removes, both with optional blocking and timeouts, safe without any manual locking. It is the standard bridge between threads that produce work and threads that consume it.",
        "example": "from queue import Queue\nfrom threading import Thread\n\nq = Queue()\n\ndef consumer():\n    while True:\n        item = q.get()\n        if item is None:\n            break\n        save(item)\n\nThread(target=consumer, daemon=True).start()\nfor item in scrape_all():\n    q.put(item)\nq.put(None)   # signal shutdown",
        "usecase": "Producer/consumer pipelines: collector threads enqueue scraped results, saver threads dequeue and write to disk at their own pace — no races, no locks.",
        "category": "concurrency"
    },
    {
        "id": 70,
        "title": "async/await basics",
        "definition": "async def marks a coroutine, and await suspends it instead of blocking while an I/O operation completes. An event loop runs many coroutines cooperatively on one thread — concurrency without threads, ideal for thousands of simultaneous network operations.",
        "example": "import asyncio\n\nasync def main():\n    print(\"start\")\n    await asyncio.sleep(1)   # suspends, does NOT block\n    print(\"done\")\n\nasyncio.run(main())",
        "usecase": "Web servers and clients juggling thousands of concurrent I/O operations on a single thread — sockets, downloads and API calls overlap without thread overhead.",
        "category": "concurrency"
    },
    {
        "id": 71,
        "title": "asyncio.gather parallel tasks",
        "definition": "asyncio.gather() schedules several coroutines on the same loop and awaits all of their results at once, failing fast if any of them raises. It is the one-liner for 'run these in parallel and collect the outputs'.",
        "example": "import asyncio\n\nasync def main():\n    results = await asyncio.gather(\n        fetch_users(),\n        fetch_orders(),\n        fetch_stock(),\n    )",
        "usecase": "Fetching several independent APIs simultaneously and combining the responses — total latency drops from the sum of the requests to roughly the slowest one.",
        "category": "concurrency"
    },
    {
        "id": 72,
        "title": "pytest basics",
        "definition": "pytest discovers test_* functions automatically, runs them, and reports each assert as a readable pass/fail. No test classes, no boilerplate — plain functions with plain asserts. Fixtures, parametrization and plugins then come as opt-in features.",
        "example": "def add(a, b):\n    return a + b\n\ndef test_add():\n    assert add(2, 3) == 5",
        "usecase": "Catching regressions in any project — pytest is the de facto standard runner, from tiny scripts to enormous monorepos, in CI and locally alike.",
        "category": "testing"
    },
    {
        "id": 73,
        "title": "pytest.mark.parametrize",
        "definition": "@pytest.mark.parametrize feeds a list of inputs into the same test body, generating a separate pass/fail row per case. Edge cases — empty strings, zeros, negatives — get real coverage without copying or looping the test function.",
        "example": "import pytest\n\n@pytest.mark.parametrize(\"a,b,expected\", [(1, 2, 3), (0, 0, 0), (-1, 1, 0)])\ndef test_add(a, b, expected):\n    assert add(a, b) == expected",
        "usecase": "Testing edge cases like empty strings, zeros and negatives without duplicating test functions — a failing row points straight at the offending input.",
        "category": "testing"
    },
    {
        "id": 74,
        "title": "pytest fixtures",
        "definition": "Fixtures are setup/teardown factories: a function marked @pytest.fixture can yield resources, run cleanup afterward, and is injected into any test that names it as a parameter. Sharing is automatic — each test receives exactly the resource it asks for.",
        "example": "import pytest\n\n@pytest.fixture\ndef db():\n    conn = connect(\":memory:\")\n    yield conn\n    conn.close()\n\ndef test_query(db):\n    assert db.run(\"SELECT 1\") == 1",
        "usecase": "Sharing a fresh database, API client or temp directory across tests without import-time side effects, repeated setup code, or leaked connections.",
        "category": "testing"
    },
    {
        "id": 75,
        "title": "Mocking external calls",
        "definition": "unittest.mock replaces slow, flaky or external dependencies with controllable stand-ins. patch() swaps an object for a mock during the with block, and assertions like assert_called_once verify behavior without ever contacting the real service.",
        "example": "from unittest.mock import patch\n\nwith patch(\"app.send_email\") as mock_send:\n    notify(\"bob@example.com\")\n    mock_send.assert_called_once()",
        "usecase": "Testing an order flow that emails customers — verify the email happens without sending real mail, keeping tests fast, deterministic and offline.",
        "category": "testing"
    },
    {
        "id": 76,
        "title": "venv isolates dependencies",
        "definition": "python3 -m venv creates an isolated environment with its own site-packages; activated shells install into it and imports resolve inside it. Two projects needing different versions of the same library can coexist without touching system Python.",
        "example": "python3 -m venv .venv\nsource .venv/bin/activate\npip install requests",
        "usecase": "Running two projects that need different versions of the same library without breaking either — the baseline practice for any real Python project.",
        "category": "packaging"
    },
    {
        "id": 77,
        "title": "__init__.py makes a package",
        "definition": "An __init__.py file marks a directory as a package, making it importable. It can also re-export the public API and set __all__, giving the package a clean, deliberate surface instead of forcing users to reach into internals.",
        "example": "# mypkg/__init__.py\nfrom .core import main, helpers\n__all__ = [\"main\", \"helpers\"]",
        "usecase": "Structuring a project into importable modules so 'from mypkg import main' works cleanly and the public API is one short file to read.",
        "category": "packaging"
    },
    {
        "id": 78,
        "title": "pip freeze pins versions",
        "definition": "pip freeze lists every installed package with its exact version, forming a snapshot you can replay with pip install -r. It is the classic lockfile for reproducible environments — modern teams may layer pip-tools or similar on top for controlled upgrades.",
        "example": "pip freeze > requirements.txt\npip install -r requirements.txt",
        "usecase": "Reproducing a deployment or CI environment exactly as it was during development — the same versions in, the same behavior out.",
        "category": "packaging"
    },
    {
        "id": 79,
        "title": "pip install -e .",
        "definition": "An editable (development) install links your source directory into the environment instead of copying it. Edits to the code take effect immediately — no reinstalling after every change — which keeps the develop-edit-test loop instant.",
        "example": "pip install -e .\n# after editing source: restart the app, changes apply",
        "usecase": "Developing a library while running its test suite — source changes are live immediately, so the feedback loop stays short and installations don't drift.",
        "category": "packaging"
    },
    {
        "id": 80,
        "title": "secrets for security",
        "definition": "The secrets module generates cryptographically strong random values — tokens, URLs, bytes — drawing on the operating system's entropy. The random module is for games and sampling, not secrets: its outputs are predictable once its state is known.",
        "example": "import secrets\n\ntoken = secrets.token_urlsafe(32)      # URL-safe API key\nchoice = secrets.choice([\"red\", \"green\", \"blue\"])",
        "usecase": "Password resets, API keys and session tokens, where predictability is a vulnerability — one module call instead of a homegrown random generator.",
        "category": "security"
    },
    {
        "id": 81,
        "title": "hashlib fingerprints",
        "definition": "hashlib computes one-way hashes — sha256, md5, blake2 and others — over bytes. A hash cannot be reversed, which makes it perfect for checksums and password digests; it is not encryption and never meant to be. Always hash after validating input, and add salt for passwords.",
        "example": "import hashlib\n\ndigest = hashlib.sha256(b\"secret\").hexdigest()\nprint(digest)   # 2bb80d53... — 64 hex characters",
        "usecase": "Verifying a downloaded file matches its published checksum, or storing salted SHA-256 digests instead of plaintext passwords in a user database.",
        "category": "security"
    },
    {
        "id": 82,
        "title": "Never build SQL with +",
        "definition": "String-concatenated SQL is injection-prone: user input can break out of its quotes and execute against your database. Parameterized queries pass values separately from the statement, so input can never become part of the SQL grammar.",
        "example": "cursor.execute(\n    \"SELECT * FROM users WHERE id = ?\", (user_id,)\n)",
        "usecase": "Any app that accepts user input and queries a database — login forms, search pages, filters. This one habit neutralizes an entire attack class.",
        "category": "security"
    },
    {
        "id": 83,
        "title": "eval() is dangerous",
        "definition": "eval() and exec() compile and run arbitrary code strings. On untrusted input — web forms, API payloads, uploaded files — that is remote code execution. ast.literal_eval parses only true literals (lists, dicts, numbers, strings) and is the safe alternative for config-like data.",
        "example": "import ast\n\n# NEVER: eval(request.json[\"expr\"])\nvalue = ast.literal_eval(\"[1, 2, 3]\")   # [1, 2, 3]",
        "usecase": "Parsing trusted literal data like '[1, 2, 3]' from a config file with ast.literal_eval — never eval — when a full parser would be overkill.",
        "category": "security"
    },
    {
        "id": 84,
        "title": "logging beats print",
        "definition": "The logging module adds levels (DEBUG through CRITICAL), timestamps, lazy %-style formatting and routing to console, files or sinks. The same call works in development and production — you tune verbosity with configuration, not by editing code.",
        "example": "import logging\n\nlogging.basicConfig(level=logging.INFO)\nlogging.info(\"user %s logged in\", user.name)\nlogging.error(\"request failed: %s\", exc)",
        "usecase": "Production debugging: debug logs stay quiet by default, errors route to a file or metric sink, and verbosity changes per deployment without code edits.",
        "category": "tooling"
    },
    {
        "id": 85,
        "title": "timeit measures code",
        "definition": "timeit measures tiny code snippets reliably: it runs the code many times and reports stable statistics, cancelling timer noise. The discipline it enables is simple — measure before you optimize, never guess which version is faster.",
        "example": "python3 -m timeit -s \"data = list(range(1000))\" \"sum(data)\"\npython3 -m timeit -s \"data = list(range(10000))\" \"functools.reduce(lambda a, b: a + b, data, 0)\"",
        "usecase": "Deciding between two implementations empirically instead of guessing — the check that keeps well-intentioned 'optimizations' from making things slower.",
        "category": "tooling"
    },
    {
        "id": 86,
        "title": "python -m runs modules",
        "definition": "python -m <module> runs a module as a script using the current interpreter's sys.path — the same machinery pip, venv and unittest are meant to be invoked with. It guarantees the tool runs in the interpreter you think it runs in.",
        "example": "python -m pip install requests\npython -m unittest discover\npython -m venv .venv",
        "usecase": "Running tools with the interpreter's environment so imports and paths match exactly — avoiding the 'wrong python' bug in CI pipelines and automation scripts.",
        "category": "tooling"
    },
    {
        "id": 87,
        "title": "Formatters keep code uniform",
        "definition": "Formatters like black or ruff format code mechanically, ending style debates: one config, one style, enforced in CI. Consistent formatting shrinks diffs, speeds up review, and keeps blame history honest.",
        "example": "ruff format .\nruff check .",
        "usecase": "CI gates on formatting so every PR looks identical in style and reviewers can focus on logic instead of whitespace debates.",
        "category": "tooling"
    },
    {
        "id": 88,
        "title": "enum for fixed options",
        "definition": "Enum gives constants an identity: each member is a distinct object with a name, value and readable repr; comparison, iteration and membership all work naturally. Ad-hoc strings fail quietly — enums turn typos into clear errors.",
        "example": "from enum import Enum\n\nclass Status(Enum):\n    ACTIVE = \"active\"\n    BANNED = \"banned\"\n\nprint(Status.BANNED.name)    # BANNED\nprint(Status.BANNED.value)   # banned",
        "usecase": "Modelling user status, order stages or payment methods with type-safe, self-documenting values — no magic strings scattered through the codebase.",
        "category": "stdlib"
    },
    {
        "id": 89,
        "title": "namedtuple for labels",
        "definition": "namedtuple builds a tiny immutable record: tuple behavior with attribute access. It gives results names — p.x instead of p[0] — with zero class boilerplate, and stays unpackable and iterable like any other tuple.",
        "example": "from collections import namedtuple\n\nPoint = namedtuple(\"Point\", [\"x\", \"y\"])\np = Point(1, 2)\nprint(p.x, p.y)   # 1 2\nx, y = p          # still unpackable",
        "usecase": "Returning coordinate pairs or (name, score) rows from a parser and reading .x/.y or .name/.score instead of positional indexing.",
        "category": "stdlib"
    },
    {
        "id": 90,
        "title": "bisect finds fast",
        "definition": "bisect performs binary search on sorted lists in O(log n): bisect_left finds where a value is or belongs, and insort inserts while keeping order. Together they power fast lookups and inserts on sorted data — no numpy or hand-rolled search needed.",
        "example": "import bisect\n\nscores = [40, 55, 72, 88]\npos = bisect.bisect_left(scores, 60)   # 2\nbisect.insort(scores, 60)\nprint(scores)   # [40, 55, 60, 72, 88]",
        "usecase": "Inserting into a ranked list while keeping it sorted, or mapping a score to a grade bracket — O(log n) even at millions of entries.",
        "category": "stdlib"
    },
    {
        "id": 91,
        "title": "heapq priority queues",
        "definition": "heapq implements priority queues: the smallest item always sits at index 0, and push and pop cost O(log n) instead of a full sort after every change. It is the standard-library answer to 'process next-by-priority' logic.",
        "example": "import heapq\n\nqueue = []\nheapq.heappush(queue, (3, \"low\"))\nheapq.heappush(queue, (1, \"urgent\"))\nheapq.heappush(queue, (2, \"normal\"))\nprint(heapq.heappop(queue))   # (1, 'urgent')",
        "usecase": "Processing support tickets by severity or scheduling jobs by deadline — priority ordering without sorting the whole list after every insertion.",
        "category": "stdlib"
    },
    {
        "id": 92,
        "title": "deque for fast ends",
        "definition": "collections.deque is a double-ended queue: appending and popping from either end costs O(1), while list.pop(0) shifts the whole list at O(n). With maxlen, a deque keeps a bounded rolling window by dropping the oldest item automatically.",
        "example": "from collections import deque\n\nq = deque([1, 2, 3], maxlen=3)\nq.append(4)\nprint(q)   # deque([2, 3, 4], maxlen=3) — oldest dropped",
        "usecase": "Undo histories, sliding-window averages over sensor readings, or streaming buffers that must never grow past a bounded size.",
        "category": "stdlib"
    },
    {
        "id": 93,
        "title": "statistics module",
        "definition": "The statistics module computes mean, median, mode, stdev and friends from plain Python data — no dependencies. Unlike numpy, it works on anything iterable and returns exact Python numbers for the small-to-medium datasets of everyday code.",
        "example": "import statistics\n\nlatencies = [120, 98, 210, 105, 99]\nprint(statistics.mean(latencies))    # 126.4\nprint(statistics.median(latencies))  # 105",
        "usecase": "Dashboard summaries — average latency and median revenue in an analytics panel — without importing numpy to summarize a handful of values.",
        "category": "stdlib"
    },
    {
        "id": 94,
        "title": "Protocol structural typing",
        "definition": "typing.Protocol declares an interface by shape: any object with the required attributes or methods satisfies it, with no inheritance needed. Type checkers then verify duck typing statically, so 'anything with .read()' arguments are checked without runtime cost.",
        "example": "from typing import Protocol\n\nclass Speaker(Protocol):\n    def speak(self) -> str: ...\n\ndef greet(speaker: Speaker):\n    print(speaker.speak())\n\nclass Dog:\n    def speak(self) -> str:\n        return \"woof\"\n\ngreet(Dog())   # passes the Protocol without subclassing",
        "usecase": "Typing duck-typed APIs like 'anything with .read()' or file-like objects in library code, where forcing subclassing would create needless coupling.",
        "category": "typing"
    },
    {
        "id": 95,
        "title": "TypedDict for dicts",
        "definition": "TypedDict documents the exact keys and value types of a dict — typically a JSON payload. Type checkers then flag missing keys and wrong value types as if the dict were a structured record, while the runtime stays a plain dict.",
        "example": "from typing import TypedDict\n\nclass Product(TypedDict):\n    name: str\n    price: float\n\ndef total(p: Product) -> float:\n    return p[\"price\"]   # mypy flags p[\"pricy\"]",
        "usecase": "Modelling raw JSON responses from third-party APIs that you can't or shouldn't convert to dataclasses, while keeping every access checked.",
        "category": "typing"
    },
    {
        "id": 96,
        "title": "Literal narrows values",
        "definition": "typing.Literal pins a parameter to specific literal values at type-check time: Literal['fast', 'safe'] admits exactly those two strings. Typos and unsupported modes become static errors instead of silent runtime surprises.",
        "example": "from typing import Literal\n\ndef set_mode(mode: Literal[\"fast\", \"safe\"]) -> None:\n    ...\n\nset_mode(\"fast\")      # ok\nset_mode(\"faster\")    # type error: not a valid mode",
        "usecase": "APIs where only a few strings are valid — modes, sort orders, encodings — turning invalid input into an editor red squiggle before it ever ships.",
        "category": "typing"
    },
    {
        "id": 97,
        "title": "isinstance beats type()",
        "definition": "isinstance checks against a type including its subclasses; type(x) == T is exact. The subclass view is almost always what you mean — and isinstance is also the canonical way to branch on types honestly, e.g. catching bool when handling int.",
        "example": "class Animal: ...\nclass Dog(Animal): ...\n\nd = Dog()\nprint(isinstance(d, Animal))   # True — subclass included\nprint(type(d) == Animal)       # False — exact only",
        "usecase": "Branching on categories of objects — like treating bool together with int because bool subclasses int — where exact comparisons silently miss subclasses.",
        "category": "gotchas"
    },
    {
        "id": 98,
        "title": "@contextmanager",
        "definition": "contextlib.contextmanager turns a generator function into a context manager: everything before yield is setup, everything after is cleanup, and exceptions unwind through it correctly. One small function instead of a full context-manager class.",
        "example": "from contextlib import contextmanager\nimport time\n\n@contextmanager\ndef timed(label):\n    t0 = time.perf_counter()\n    yield\n    print(f\"{label}: {time.perf_counter() - t0:.3f}s\")\n\nwith timed(\"query\"):\n    run_query()",
        "usecase": "Wrapping code blocks with timers, log contexts or temporary state — the with-statement ergonomics without writing a class with __enter__ and __exit__.",
        "category": "functions"
    },
    {
        "id": 99,
        "title": "from __future__ import annotations",
        "definition": "This future import defers annotation evaluation: hints are stored as strings and never executed at import time. Forward references to not-yet-defined classes just work, circular imports between modules stop exploding, and it also quiets the runtime with modern slot syntax.",
        "example": "from __future__ import annotations\n\nclass Tree:\n    def children(self) -> list[Tree]: ...   # Tree not yet defined!",
        "usecase": "Referencing a class before its definition or across module cycles, and keeping modern hint syntax running on older Python versions in multi-version codebases.",
        "category": "typing"
    },
    {
        "id": 100,
        "title": "Chained comparisons",
        "definition": "Python chains comparisons naturally: a < b < c means a < b and b < c, with the middle operand evaluated once. It reads like mathematics and covers <=, ==, is and friends mixed freely in one expression.",
        "example": "score = 87\nif 0 <= score <= 100:\n    print(\"valid score\")\n\nif min_val < x <= max_val:\n    print(\"within bounds\")",
        "usecase": "Validating ranges in one glance — form boundaries, percentage checks, pagination limits — instead of nested and-conditions or library calls.",
        "category": "idioms"
    },
    {
        "id": 101,
        "title": "Small ints are cached",
        "definition": "CPython caches integers from -5 to 256 as singletons, so is happens to return True for them. Larger ints are freshly created per operation, so identity checks break — rely on == for all numbers and treat the caching as trivia, not a tool.",
        "example": "a, b = 256, 256\nprint(a is b)      # True — cached range\nc, d = 257, 257\nprint(c is d)      # False — fresh objects, never rely on this",
        "usecase": "The gotcha behind mysterious identity comparisons in debugging sessions — always compare numbers with == and never assume is works for ints.",
        "category": "gotchas"
    },
    {
        "id": 102,
        "title": "[x] * n shares references",
        "definition": "Multiplying a list repeats the same inner object references n times — one element, N aliases. Mutating any one of them mutates them all, which reads as the infamous 'one cell changed the whole grid' bug. Build independent containers with a comprehension instead.",
        "example": "grid = [[]] * 3\ngrid[0].append(\"x\")\nprint(grid)   # [['x'], ['x'], ['x']] — all three changed!\n\ngrid = [[] for _ in range(3)]\ngrid[0].append(\"x\")\nprint(grid)   # [['x'], [], []]",
        "usecase": "Building 2D grids, rows of cells, or per-thread buffers — the classic bug where apparently empty structures share hidden state.",
        "category": "gotchas"
    },
    {
        "id": 103,
        "title": "dict.fromkeys seeds keys",
        "definition": "dict.fromkeys(iterable, value) creates a dict with one key per item and a shared default value — a one-call way to seed known keys. The default is shared by reference, so for mutable values use {k: expr for k in keys} instead.",
        "example": "attendance = dict.fromkeys([\"alice\", \"bob\"], False)\nattendance[\"alice\"] = True\nprint(attendance)   # {'alice': True, 'bob': False}",
        "usecase": "Initializing attendance, checkbox or permission state for a known set of keys — while remembering list-valued defaults need a comprehension, not fromkeys.",
        "category": "dicts"
    },
    {
        "id": 104,
        "title": "operator.itemgetter",
        "definition": "operator.itemgetter returns a callable that reads a given index, key or attribute — a ready-made key function for sorting. Sorting by multiple items at once (itemgetter(1, 0)) does stable multi-column ordering without nested lambdas.",
        "example": "from operator import itemgetter\n\nrows = [(2, \"b\"), (1, \"a\"), (2, \"a\")]\nrows.sort(key=itemgetter(0, 1))\nprint(rows)   # [(1, 'a'), (2, 'a'), (2, 'b')]",
        "usecase": "Spreadsheet-style multi-column sorting where the second key breaks ties — or choosing sort keys without lambdas in hot paths.",
        "category": "sorting"
    },
    {
        "id": 105,
        "title": "itertools.islice",
        "definition": "itertools.islice slices an iterator lazily — it never materializes the underlying stream. Taking the first N items of a huge or infinite generator costs O(N), making previews and 'top of stream' logic cheap.",
        "example": "from itertools import islice\n\ndef counting():\n    n = 0\n    while True:\n        yield n\n        n += 1\n\nprint(list(islice(counting(), 5)))   # [0, 1, 2, 3, 4]",
        "usecase": "Browsing a large paginated iterator, previewing an endless feed, or capping a memory-hungry pipeline to the first N records.",
        "category": "performance"
    },
    {
        "id": 106,
        "title": "sys.getsizeof reality check",
        "definition": "sys.getsizeof returns the raw size of one object — and the numbers are often surprising: containers report only their own struct, not nested contents, and a Python int is not 4 bytes. Use it as a sanity probe for memory budgets, not a precise profiler.",
        "example": "import sys\n\nprint(sys.getsizeof([1, 2, 3]))      # ~88 bytes\nprint(sys.getsizeof({1, 2, 3}))      # ~216 bytes\nprint(sys.getsizeof(\"a\" * 1000))    # ~1049 bytes",
        "usecase": "Deciding between lists, sets and dicts for millions of rows in a memory-bound pipeline — the probe that shows where the bytes actually went.",
        "category": "performance"
    },
    {
        "id": 107,
        "title": "Sort once, group by key",
        "definition": "itertools.groupby clusters consecutive equal items — so group by the same key you sorted with and the groups come out clean. Sort with a key function, group with that identical key function, and aggregation reports write themselves.",
        "example": "from itertools import groupby\n\nusers = [{\"city\": \"berlin\", \"n\": 2}, {\"city\": \"berlin\", \"n\": 1}, {\"city\": \"paris\", \"n\": 3}]\nusers.sort(key=lambda u: u[\"city\"])\nfor city, group in groupby(users, key=lambda u: u[\"city\"]):\n    print(city, sum(u[\"n\"] for u in group))",
        "usecase": "Aggregation reports — users per city, sales per region — built by sorting once and grouping, without nested dict gymnastics or repeated scans.",
        "category": "performance"
    },
    {
        "id": 108,
        "title": "Sets dedupe in O(1)",
        "definition": "A set can hold at most one copy of each hashable item, and membership checks are O(1) — so set() is both the dedupe tool and the fast-membership container. Order is lost in the process; wrap with sorted() when order matters.",
        "example": "user_ids = [3, 1, 3, 2, 1]\nunique = set(user_ids)           # {1, 2, 3}\nordered = sorted(set(user_ids))  # [1, 2, 3]",
        "usecase": "Merging mailing lists or IDs from multiple sources without O(n²) pairwise checks — dedupe first, restore order with sorted() for stable output.",
        "category": "performance"
    },
    {
        "id": 109,
        "title": "Localize hot loop lookups",
        "definition": "In a tight loop, every name lookup walks the scope chain. Binding a function to a local variable (append = list.append) turns global lookups into fast local ones — a micro-optimization that matters only in profiled hot paths with millions of iterations.",
        "example": "append = result.append\nfor x in data:\n    append(x * 2)",
        "usecase": "Millions of iterations in data transforms or parsers — apply only after profiling identifies the loop as hot, never as a blanket styling habit.",
        "category": "performance"
    },
    {
        "id": 110,
        "title": "functools.wraps keeps identity",
        "definition": "A decorator replaces a function with its wrapper, and without care the metadata — __name__, __doc__, __qualname__ — becomes the wrapper's. @functools.wraps copies the original's metadata onto the wrapper so introspection, help() and error messages keep working.",
        "example": "from functools import wraps\n\ndef logged(fn):\n    @wraps(fn)\n    def inner(*args, **kwargs):\n        print(f\"calling {fn.__name__}\")\n        return fn(*args, **kwargs)\n    return inner\n\n@logged\ndef hello(): ...\n\nprint(hello.__name__)   # 'hello', not 'inner'",
        "usecase": "Frameworks that inspect decorated functions — Flask routes, pytest items, CLI commands — break when wraps is missing; help(), docs and errors all point to the original name.",
        "category": "functions"
    },
    {
        "id": 111,
        "title": "assert for invariants",
        "definition": "assert checks things that MUST be true for your code to be correct — internal invariants, not user input. Under python -O it compiles away entirely, so it can never guard security or validation; it is a development-time and test-time tool.",
        "example": "def process(items, total):\n    assert len(items) == total, \"length mismatch\"\n    ...",
        "usecase": "Catching violated invariants during development and test runs — while real input validation lives in proper checks that survive -O and production.",
        "category": "testing"
    },
    {
        "id": 112,
        "title": "try/except/else/finally",
        "definition": "Python's full exception grammar: try runs the risky code, except handles the failure, else runs only when no exception occurred, and finally always runs. The else block cleanly separates 'it worked' from 'it failed and I handled it'.",
        "example": "try:\n    save_order(order)\nexcept DBError as e:\n    log.error(\"save failed: %s\", e)\nelse:\n    log.info(\"order saved\")\nfinally:\n    conn.close()",
        "usecase": "Transactions where cleanup (finally), success handling (else) and error handling (except) each get a dedicated, readable block instead of tangled nesting.",
        "category": "exceptions"
    },
    {
        "id": 113,
        "title": "Exception groups",
        "definition": "ExceptionGroup (Python 3.11+) bundles multiple exceptions into one object, and except* unzips a group by type so each handler claims its share while the rest re-raise. Parallel work that fails in several ways stops hiding all but the first failure.",
        "example": "try:\n    await asyncio.gather(task_a(), task_b(), task_c())\nexcept* TimeoutError:\n    log(\"some tasks timed out\")\nexcept* ValueError:\n    log(\"some tasks got bad input\")",
        "usecase": "Parallel tasks — asyncio.gather, task groups — where each may fail differently; exception groups report every failure instead of only the first, so no detail is lost.",
        "category": "exceptions"
    },
    {
        "id": 114,
        "title": "bytes vs str",
        "definition": "bytes are raw sequences of integers from 0 to 255; str is decoded text. The two never mix implicitly — b'a' + 'b' raises TypeError — so every conversion requires an explicit encoding, usually UTF-8. Knowing which one you hold, and in which encoding, prevents half the text bugs in Python.",
        "example": "raw = b\"\\xe2\\x82\\xac\"          # UTF-8 bytes for €\ntext = raw.decode(\"utf-8\")     # '€'\nback = text.encode(\"utf-8\")    # b'\\xe2\\x82\\xac' identical again",
        "usecase": "Anything touching sockets, binary file reads or external libraries — explicitly decoding at the boundary is what keeps CSV, JSON and log text from becoming mojibake.",
        "category": "gotchas"
    },
    {
        "id": 115,
        "title": "datetime with timezone",
        "definition": "Naive datetimes carry no timezone and compare inconsistently across zones. timezone-aware datetimes with timezone.utc describe an unambiguous instant; convert to local zones only for display. UTC storage removes the 'which 3pm?' ambiguity entirely.",
        "example": "from datetime import datetime, timezone, timedelta\n\nnow = datetime.now(timezone.utc)                         # aware\nparis = now.astimezone(timezone(timedelta(hours=1)))\nprint(now, paris)",
        "usecase": "Multi-user apps where 'when did that happen?' must mean the same instant for users in Tokyo, London and New York — store UTC, display local.",
        "category": "stdlib"
    },
    {
        "id": 116,
        "title": "glob patterns for files",
        "definition": "glob patterns (*, ?, [seq]) find files by name pattern without manual directory walking. pathlib's Path.glob() returns Path objects and supports recursive ** patterns — the standard way to collect files for a batch job.",
        "example": "from pathlib import Path\n\nfor log in Path(\"logs\").glob(\"access_2026-*.log\"):\n    print(log)\n\nall_py = list(Path(\"src\").rglob(\"*.py\"))   # recursive",
        "usecase": "Collecting all log files for a date range or every image before a resize batch job — pattern-driven discovery instead of manual os.listdir crawling.",
        "category": "tooling"
    },
    {
        "id": 117,
        "title": "tempfile for scratch work",
        "definition": "tempfile creates scratch files and directories with random names in the system temp area — and cleans them up safely. TemporaryDirectory as a context manager removes the whole tree on exit, even when the block raises.",
        "example": "import tempfile\nfrom pathlib import Path\n\nwith tempfile.TemporaryDirectory() as d:\n    tmp = Path(d) / \"out.csv\"\n    tmp.write_text(\"a,b\\n1,2\")\n    # ... do the work ...\n# directory is gone here",
        "usecase": "Compressing archives to disk or running sandboxed report jobs that must leave no junk behind — and never collide with concurrent runs.",
        "category": "stdlib"
    },
    {
        "id": 118,
        "title": "argparse for CLIs",
        "definition": "argparse turns a single parser declaration into full CLI behavior: flags, options, defaults, type conversion and a generated --help. It takes care of the boring parts of every script — parsing and validating command-line input reliably.",
        "example": "import argparse\n\np = argparse.ArgumentParser(description=\"report generator\")\np.add_argument(\"--verbose\", action=\"store_true\")\np.add_argument(\"--out\", default=\"report.txt\")\nargs = p.parse_args()\nprint(args.out, args.verbose)",
        "usecase": "Shipping scripts that others run in CI — flags like --dry-run and --out come free, with help text, defaults and error handling included.",
        "category": "tooling"
    },
    {
        "id": 119,
        "title": "urllib vs requests",
        "definition": "urllib is the standard library's HTTP client — always available, no installs, but verbose. requests (or httpx) offers the pleasant API on top. In locked-down environments where pip isn't allowed, urllib still works; for real applications, prefer requests or httpx.",
        "example": "import json\nimport urllib.request\n\nwith urllib.request.urlopen(\"https://api.example.com/v1\") as r:\n    data = json.loads(r.read())\nprint(data)",
        "usecase": "Quick checks in restricted environments where pip installs aren't possible — while production applications reach for requests/httpx and their friendlier APIs.",
        "category": "stdlib"
    },
    {
        "id": 120,
        "title": "math.inf and nan",
        "definition": "float('inf') and math.nan represent 'larger than anything' and 'not a number'. Infinity seeds maxima/minima comparisons without magic numbers like -9999; NaN tracks missing data in computations — as long as you remember the rule that NaN never equals itself.",
        "example": "best = float(\"-inf\")\nfor score in scores:\n    if score > best:\n        best = score\nprint(best)\n\nif x != x:           # the only way NaN detects itself\n    print(\"x is NaN\")",
        "usecase": "Finding maxima without fake sentinel values, or representing 'no timeout' as math.inf in configs where an actual zero would mean something real.",
        "category": "builtins"
    }
]
