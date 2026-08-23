TIPS = [
    {
        "id": 1,
        "title": "Requests does HTTP, plainly",
        "definition": "requests is the friendliest HTTP client in the Python ecosystem, wrapping urllib3 into a tiny, human-readable API. Its get, post, put and delete functions turn raw sockets, headers and bytes into a Response object you can inspect, and nearly every Python tool that talks to a server uses it under the hood.",
        "example": "import requests\nr = requests.get('https://api.github.com')\nprint(r.status_code, r.headers['content-type'])",
        "usecase": "Automation scripts, CI checks, data pipelines and webhooks that need one reliable, readable way to talk to remote servers.",
        "category": "requests"
    },
    {
        "id": 2,
        "title": "params, URL query it right",
        "definition": "Pass a plain dict to params and requests URL-encodes it into the query string for you, handling percent-encoding, repeated keys and None exclusions. List values are repeated as multiple key=value pairs, while None-valued entries are dropped entirely, so URLs stay correct even when the inputs are messy.",
        "example": "r = requests.get('https://api.github.com/search/repositories',\n                 params={'q': 'httpx', 'per_page': 10, 'topic': ['api', 'async']})\nprint(r.url)",
        "usecase": "Building search and filter URLs from user input without string concatenation or hand-rolled encoding bugs.",
        "category": "requests"
    },
    {
        "id": 3,
        "title": "json= for POST bodies",
        "definition": "The json= argument serializes a dict as the request body with Content-Type application/json, and the .json() method parses a response back into Python objects. The pair works together: structured payloads go out cleanly and structured replies come back in one step, with no hand-built content-type headers.",
        "example": "r = requests.post('https://httpbin.org/anything',\n                 json={'name': 'Ada', 'role': 'admin'})\nprint(r.json()['json'])",
        "usecase": "Sending structured payloads to REST APIs, webhooks and LLM provider endpoints, then reading their JSON replies without extra parsing work.",
        "category": "requests"
    },
    {
        "id": 4,
        "title": "headers, speak the protocol",
        "definition": "The headers= parameter sets HTTP headers per request, matched case-insensitively, so user-agent and User-Agent behave identically. Without it the client sends a default python-requests user agent and no Authorization header, which many public APIs reject or throttle, making explicit headers the standard fix.",
        "example": "headers = {'User-Agent': 'my-app/1.0 contact@example.com',\n           'Accept': 'application/vnd.github+json',\n           'Authorization': 'Bearer ghp_xxx'}\nr = requests.get('https://api.github.com/rate_limit', headers=headers)",
        "usecase": "Setting API tokens, content negotiation and friendly user agents that keep integrations out of bot-detection buckets.",
        "category": "requests"
    },
    {
        "id": 5,
        "title": "timeout, always set one",
        "definition": "Without a timeout the default is None, so a hung connection blocks your thread forever. A single float bounds both the connect and read phases, while a tuple like (3.05, 27) bounds them separately, and requests.exceptions.Timeout is raised so code can fail fast and degrade gracefully instead of freezing.",
        "example": "try:\n    r = requests.get('https://slow.example/data', timeout=(3.05, 10))\nexcept requests.exceptions.Timeout:\n    print('server unreachable within limits')",
        "usecase": "Any network call in production where a dead endpoint must surface quickly rather than stalling the whole application.",
        "category": "requests"
    },
    {
        "id": 6,
        "title": "raise_for_status, fail loudly",
        "definition": "requests never raises for 4xx and 5xx by default; it just records the status code. Calling raise_for_status() throws requests.exceptions.HTTPError when the code is 400 or above, turning silent server errors into catchable exceptions so an error page can never be mistaken for real data.",
        "example": "r = requests.get('https://api.example.com/users/1')\ntry:\n    r.raise_for_status()\nexcept requests.exceptions.HTTPError as e:\n    log.error('API rejected request %s', e.response.text)",
        "usecase": "Data pipes and services that must notice 404s, 429s and 500s instead of parsing an error page as legitimate JSON.",
        "category": "requests"
    },
    {
        "id": 7,
        "title": "Session, keep it together",
        "definition": "A Session pools TCP connections, persists cookies and shares default headers across all its calls, so a logged-in flow or a bulk loop runs at a fraction of the latency of standalone requests. Build the session once, set headers and adapters on it, then reuse it for the whole process where resources allow.",
        "example": "s = requests.Session()\ns.headers.update({'User-Agent': 'pipeline/2.1'})\ns.get('https://app.example/login', data={'u': 'ada', 'p': 'secret'})\nprofile = s.get('https://app.example/me').json()\nprint(profile['name'])",
        "usecase": "Sequential API flows that share one auth cookie, plus bulk loops over many URLs that benefit from keep-alive sockets.",
        "category": "requests"
    },
    {
        "id": 8,
        "title": "stream=True for big downloads",
        "definition": "With stream=True the request returns immediately and the body downloads lazily; iter_content(chunk_size) or iter_lines() then pull the response in pieces so hundreds of megabytes never land in RAM at once. The context manager form closes the underlying socket cleanly when the download finishes.",
        "example": "with requests.get('https://mirror.example/big.iso', stream=True) as r:\n    with open('big.iso', 'wb') as f:\n        for chunk in r.iter_content(chunk_size=8192):\n            f.write(chunk)",
        "usecase": "Fetching large media, model weights or data dumps on constrained memory, and processing log streams line by line as they arrive.",
        "category": "requests"
    },
    {
        "id": 9,
        "title": "auth tuple for basic auth",
        "definition": "Passing a (user, password) tuple to auth= builds HTTP Basic credentials, base64-encoding them into the Authorization header exactly as RFC 7617 specifies. For servers that negotiate differently, HTTPDigestAuth handles challenge-response schemes, and any subclass of AuthBase can customize header generation entirely.",
        "example": "from requests.auth import HTTPDigestAuth\n\nr1 = requests.get('https://api.internal.example/', auth=('user', 'pass'))\nr2 = requests.get('https://router.example/status', auth=HTTPDigestAuth('user', 'pass'))",
        "usecase": "Gatekeeping internal tools and vendor APIs that still authenticate with HTTP Basic or Digest credentials.",
        "category": "requests"
    },
    {
        "id": 10,
        "title": "files for multipart uploads",
        "definition": "The files= argument encodes a dict into a multipart/form-data request, generating the boundary, content types and filenames that format requires. Key a field name to a file object and the binary is uploaded unchanged, with an optional tuple overriding the filename and MIME type per file.",
        "example": "with open('photo.jpg', 'rb') as f:\n    r = requests.post('https://upload.example/api/images',\n                      files={'image': ('photo.jpg', f, 'image/jpeg')})\nprint(r.status_code)",
        "usecase": "Submitting images, spreadsheets, PDFs or any binary to upload endpoints and web forms that expect multipart bodies.",
        "category": "requests"
    },
    {
        "id": 11,
        "title": "data= for form bodies",
        "definition": "The data= argument url-encodes a dict into an application/x-www-form-urlencoded body, the format classic HTML forms submit. Unlike json=, it sets no JSON content type and sends literal key=value pairs, which matters for login endpoints and legacy services that read form fields rather than request bodies.",
        "example": "r = requests.post('https://app.example/login',\n                  data={'username': 'ada', 'password': 's3cret'})\nprint(r.status_code, r.url)",
        "usecase": "Logging into form-based sites, submitting HTML form fields, and talking to OAuth password-grant token endpoints.",
        "category": "requests"
    },
    {
        "id": 12,
        "title": "cookies, retrieve and send",
        "definition": "Responses carry a cookie jar at r.cookies that you can read by name, and the cookies= argument sends cookies on a single call without building a Session. Because domains, paths and expiry are honored by the jar, this works for scoped session cookies that plain header injection would mishandle.",
        "example": "sid = requests.get('https://app.example/login', data=login).cookies['sessionid']\nr = requests.get('https://app.example/dashboard', cookies={'sessionid': sid})\nprint(r.json()['user'])",
        "usecase": "Single-shot API calls that need a cookie obtained moments earlier, without the ceremony of a full Session object.",
        "category": "requests"
    },
    {
        "id": 13,
        "title": "redirects, follow or don't",
        "definition": "requests follows 3xx redirects automatically for GET and records every hop in r.history; the final response reflects the landing page. Setting allow_redirects=False returns the redirect response itself so the Location header can be inspected, and POST bodies are typically rewritten to GET on 301 and 302 hops, per browser behavior.",
        "example": "r = requests.get('https://t.co/abc123', allow_redirects=False)\nprint(r.status_code, r.headers.get('Location'))\nfor hop in requests.get('https://t.co/abc123').history:\n    print(hop.url, hop.status_code)",
        "usecase": "Unrolling URL shorteners, auditing landing URLs, and debugging misconfigured redirect chains in your own servers.",
        "category": "requests"
    },
    {
        "id": 14,
        "title": "Retries you actually control",
        "definition": "Real resilience comes from mounting an HTTPAdapter configured with a urllib3 Retry policy on the session. The Retry arguments bound how many connect, read and status failures are retried, and backoff_factor inserts exponentially growing pauses between attempts, so bursty outages and rate limits get absorbed while the client keeps working.",
        "example": "from requests.adapters import HTTPAdapter\nfrom urllib3.util.retry import Retry\n\ns = requests.Session()\npolicy = Retry(total=4, backoff_factor=0.5, status_forcelist=[429, 500, 503])\ns.mount('https://', HTTPAdapter(max_retries=policy))\ndata = s.get('https://api.example.com/items').json()",
        "usecase": "API clients that must survive flaky mobile networks, transient 503s and rate limiting instead of logging an error per blip.",
        "category": "requests"
    },
    {
        "id": 15,
        "title": "verify=False, skip SSL (with care)",
        "definition": "SSL verification is on by default, validating the server certificate against trusted CAs; verify=False disables that check entirely. That removes MITM protection, so it belongs only in throwaway tests against hosts with self-signed certificates — and even then, a custom bundle with verify='/path/ca.pem' is the safer alternative.",
        "example": "# dev-only: trust a self-signed server quickly\nr = requests.get('https://devbox.local/api', verify=False)\n# safer: verify against your own CA bundle\nr2 = requests.get('https://devbox.local/api', verify='dev-ca.pem')",
        "usecase": "Local development against self-signed containers and test rigs — never in production-facing code.",
        "category": "requests"
    },
    {
        "id": 16,
        "title": "proxies, route around the world",
        "definition": "The proxies= dict routes each scheme through a different forward proxy, so HTTP and HTTPS traffic can take separate roads. Alongside it, requests honors standard proxy environment variables while trust_env is enabled, and no_proxy plus localhost addresses normally bypass the proxy to keep internal calls direct.",
        "example": "proxies = {'http': 'http://corp-proxy:8080', 'https': 'http://corp-proxy:8080'}\nr = requests.get('https://news.example/feed', proxies=proxies)\nprint(r.status_code)",
        "usecase": "Working inside corporate gateways, testing from different egress IPs, and routing around IP-based rate limits.",
        "category": "requests"
    },
    {
        "id": 17,
        "title": "encoding, decode it right",
        "definition": "Responses decode bytes with whatever charset the Content-Type header declares; when it is missing, requests falls back to a guessed encoding that can garble text. Setting r.encoding before touching r.text forces the right decoder, and r.apparent_encoding runs statistical detection for servers that do not know themselves.",
        "example": "r = requests.get('https://legacy.example/page')\nr.encoding = 'cp1252'          # charset header was wrong\nprint(r.text[:200])            # decoded correctly now\nprint(r.apparent_encoding)     # detective work if unknown",
        "usecase": "Consuming non-UTF-8 sites and legacy servers that omit or misstate their charset headers.",
        "category": "requests"
    },
    {
        "id": 18,
        "title": "PUT, PATCH, DELETE and beyond",
        "definition": "Beyond get and post, requests exposes put, patch, delete, head and options, each returning the same rich Response type. PUT replaces a full resource, PATCH applies a partial update, DELETE removes one, and HEAD fetches headers without a body — so a single client covers the whole REST verb set.",
        "example": "requests.put('https://api.example.com/items/7', json={'sku': 'A-100', 'qty': 3})\nrequests.patch('https://api.example.com/items/7', json={'qty': 4})\nr = requests.delete('https://api.example.com/items/7')\nprint(r.status_code)",
        "usecase": "Driving full CRUD against REST APIs — creating, replacing, updating and removing resources from Python.",
        "category": "requests"
    },
    {
        "id": 19,
        "title": "async requests with httpx",
        "definition": "httpx reimplements the requests API and adds first-class async: AsyncClient and await make hundreds of concurrent calls cheap without threads, plus HTTP/2 and pluggable transports for testing. Your synchronous code keeps the same shape, so teams migrate gradually instead of rewriting clients twice.",
        "example": "import httpx, asyncio\n\nasync def fetch(url: str) -> str:\n    async with httpx.AsyncClient() as client:\n        r = await client.get(url)\n        return r.text\n\nprint(asyncio.run(fetch('https://python.org')))",
        "usecase": "Fanning out to many APIs at once, high-throughput integrations, and HTTP/2 workloads where requests cannot follow.",
        "category": "requests"
    },
    {
        "id": 20,
        "title": "The response object, inspect it",
        "definition": "The Response object exposes the whole exchange: status_code, reason, headers, url, cookies, history and elapsed describe what happened, while content, text and json() deliver the body in the form you need. The request attribute holds the Request that produced it, so you can log exactly what went out and came back.",
        "example": "r = requests.get('https://api.example.com/items/7', timeout=10)\nprint(r.status_code, r.reason)\nprint('round-trip', round(r.elapsed.total_seconds() * 1000), 'ms')\nprint(r.headers.get('content-type'), '->', r.url)",
        "usecase": "Diagnosing slow or failing integrations — latency, error bodies and final URLs without extra instrumentation.",
        "category": "requests"
    },
    {
        "id": 21,
        "title": "Compressed responses, handled automatically",
        "definition": "requests advertises gzip and deflate in Accept-Encoding automatically and decompresses whichever the server picks, transparently, so content and text are always plain data. With brotli support installed, br-compressed payloads are decoded too, quietly cutting large API downloads to a fraction of their wire size.",
        "example": "r = requests.get('https://api.example.com/huge/log')   # gzip on the wire\nrows = r.json()\nprint('compressed bytes:', r.raw.headers.get('content-length'))\nprint('decoded bytes:   ', len(r.content))",
        "usecase": "Big report endpoints and data exports that save bandwidth and round-trip time without extra application code.",
        "category": "requests"
    },
    {
        "id": 22,
        "title": "Errors as classes, catch them precisely",
        "definition": "Every failure mode is a class in requests.exceptions, so except clauses can catch exactly what is meant: Timeout, ConnectionError, HTTPError, TooManyRedirects, SSLError, all rooted in RequestException. Narrow catches get retried or downgraded while genuinely unexpected errors still propagate to logging and alerting.",
        "example": "import requests.exceptions as exc\n\ntry:\n    r = requests.get('https://api.example.com/items/7', timeout=3)\n    r.raise_for_status()\nexcept exc.Timeout:\n    print('retry later')\nexcept exc.ConnectionError:\n    print('network or DNS failed')\nexcept exc.HTTPError as e:\n    print('API error', e.response.status_code)",
        "usecase": "Resilient clients that tell timeouts apart from hard failures and retry one kind without masking the other.",
        "category": "requests"
    },
    {
        "id": 23,
        "title": "History, the redirect trail",
        "definition": "The history attribute lists every intermediate response that led to the final one, in order, each with its own url, status_code and headers, while the final response describes the landing page. That makes redirect chains fully auditable — the sequence of Location headers reveals every hop and where the journey ends.",
        "example": "r = requests.get('https://redirect.example/orig')\nfor i, hop in enumerate(r.history):\n    print(i, hop.status_code, hop.headers.get('Location'))\nprint('final', r.status_code, r.url)",
        "usecase": "Tracing short-link campaigns, auditing redirect chains on your CDN, and proving where a URL actually lands.",
        "category": "requests"
    },
    {
        "id": 24,
        "title": "Custom user agents, look human",
        "definition": "The default user agent, python-requests/2.x, brands every request as an automation tool, and some gateways block it outright. Sending a browser-style User-Agent header per request, or once on a Session, makes traffic plausible — while paired with sane pacing it keeps integrations out of WAF threat buckets.",
        "example": "headers = {\n    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '\n                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36',\n}\nr = requests.get('https://store.example/product/44', headers=headers)\nprint(r.status_code)",
        "usecase": "Accessing sites whose rules admit browsers but flag default tooling, and complying with APIs that require real UA strings.",
        "category": "requests"
    },
    {
        "id": 25,
        "title": "Test your HTTP code with responses",
        "definition": "The responses library intercepts outbound HTTP and returns recorded stubs, so tests run fast, deterministically and offline. Decorators and context managers register canned responses per method and path, while responses.calls lets tests assert exactly which requests happened and with what payloads.",
        "example": "import requests, responses\n\n@responses.activate\ndef test_fetch_user():\n    responses.get('https://api.example.com/users/7',\n                  json={'name': 'Ada'}, status=200)\n    r = requests.get('https://api.example.com/users/7')\n    assert r.json() == {'name': 'Ada'}\n    assert len(responses.calls) == 1",
        "usecase": "Unit-testing any function that performs HTTP without network flakiness, and pinning down request shapes in CI.",
        "category": "requests"
    },
    {
        "id": 26,
        "title": "Keep-alive, reuse those TCP sockets",
        "definition": "Plain requests calls open a fresh connection each time, but a Session keeps a pool of keep-alive sockets, so repeated calls to the same host skip TCP and TLS handshakes. Across hundreds or thousands of calls that overhead adds up to minutes of saved time, which is why bulk loops should always reuse one Session.",
        "example": "import time\n\nwith requests.Session() as s:\n    t0 = time.perf_counter()\n    for _ in range(200):\n        s.get('https://api.example.com/status')\n    print('200 calls in', round(time.perf_counter() - t0, 2), 's')",
        "usecase": "Bulk health checks, paginated listing loops and batch jobs hammering one API endpoint repeatedly.",
        "category": "requests"
    },
    {
        "id": 27,
        "title": "Werkzeug-style StreamedResponse pattern",
        "definition": "stream=True hands back the response before the body arrives, and iter_lines(), like a Werkzeug streamed response, consumes it line by line as chunks land. That pattern turns server log streams and endless API feeds into Python generators that can be processed, filtered or teed without buffering the whole stream.",
        "example": "import json\n\nwith requests.get('https://stream.example/events', stream=True) as r:\n    for line in r.iter_lines():\n        if not line:\n            continue\n        evt = json.loads(line)\n        if evt['type'] == 'order':\n            print(evt['order_id'])",
        "usecase": "Consuming SSE feeds, log tails and incremental JSON lines one event at a time with bounded memory.",
        "category": "requests"
    },
    {
        "id": 28,
        "title": "Digest auth for legacy systems",
        "definition": "HTTPDigestAuth implements the challenge-response scheme RFC 2617 defines: the server sends a nonce, the client answers with a hashed credential, and no password travels in cleartext. Legacy routers, printers and embedded devices still speak digest-only, so this auth mode keeps them reachable from Python.",
        "example": "from requests.auth import HTTPDigestAuth\n\nr = requests.get('https://192.168.1.1/api/status',\n                 auth=HTTPDigestAuth('admin', 'letmein'),\n                 verify=False)\nprint(r.status_code, r.text[:80])",
        "usecase": "Administering old network hardware and vendor appliances whose authentication predates modern web stacks.",
        "category": "requests"
    },
    {
        "id": 29,
        "title": "Client certs for mTLS",
        "definition": "Passing cert=('client.crt', 'client.key') mounts a TLS client certificate, letting servers demand and verify your identity before any response — mutual TLS. Combined with verify pointing at the issuer chain, this is how payment gateways and enterprise APIs authenticate software rather than people.",
        "example": "r = requests.get('https://bank.example/api/accounts',\n                 cert=('client.crt', 'client.key'),\n                 verify=('ca-bundle.pem',))\nprint(r.status_code)",
        "usecase": "Machine-to-machine authentication with payment APIs, private marketplaces and enterprise SSO mTLS gateways.",
        "category": "requests"
    },
    {
        "id": 30,
        "title": "The zen of requests",
        "definition": "The zen of requests is that normal HTTP should read like prose: one line fetches a URL, and ten lines achieve a full authenticated, resilient download. Timeout, raise_for_status and Session are the three patterns that keep that prose safe under production load, covering almost every real integration.",
        "example": "with requests.Session() as s:\n    s.headers.update({'User-Agent': 'nightly-sync/2.0'})\n    r = s.get('https://api.example.com/reports/weekly',\n              params={'tz': 'UTC'}, timeout=30)\n    r.raise_for_status()\n    rows = r.json()",
        "usecase": "A reference idiom for teams standardizing service clients — readable, time-bounded and loud about failures.",
        "category": "requests"
    },
    {
        "id": 31,
        "title": "params, cleanly",
        "definition": "Pass query strings as a dict via params and requests URL-encodes it for you, percent-escaping values, repeating list items as multiple pairs and dropping None entries. The alternative, f-string concatenation of URLs, silently breaks on spaces, ampersands and unicode — params exists so that never happens.",
        "example": "r = requests.get('https://search.example/api/products',\n                 params={'q': 'data  science', 'page': 2, 'tag': ['ml', 'py']})\nprint(r.url)",
        "usecase": "Avoiding manual string concatenation and its nasty encoding bugs in search and filter URLs.",
        "category": "requests"
    },
    {
        "id": 32,
        "title": "json= posts, data= forms",
        "definition": "json= serializes a dict as an application/json request body, while data= url-encodes it into the x-www-form-urlencoded format HTML forms submit. The server reads the first from the body parser and the second from form fields, so picking correctly is what makes or breaks a POST integration.",
        "example": "requests.post('https://api.example.com/items', json={'name': 'Ada'})\nrequests.post('https://legacy.example/login', data={'user': 'ada'})",
        "usecase": "Choosing the right body type — REST APIs expect JSON, legacy form endpoints expect url-encoded fields.",
        "category": "requests"
    },
    {
        "id": 33,
        "title": "uploading files with files=",
        "definition": "The files= argument builds a multipart/form-data request, generating boundaries and content types so browsers and servers both understand it. Map a field name to a file object, and the bytes upload unchanged; the tuple form adds per-file filenames and MIME types when the receiving API is strict.",
        "example": "import io\n\nr = requests.post('https://upload.example/api/invoices',\n                  files={'report': ('q3.csv', open('q3.csv', 'rb'), 'text/csv'),\n                         'cover': io.BytesIO(b'see attached')})\nprint(r.status_code)",
        "usecase": "Sending images, PDFs, CSVs or any binary to upload endpoints while naming files precisely.",
        "category": "requests"
    },
    {
        "id": 34,
        "title": "stream response bodies",
        "definition": "stream=True avoids reading the whole body into memory; iter_content(chunk_size) pulls it in bounded chunks and iter_lines() yields text lines, so downloads and log feeds flow incrementally. The with-block closes the socket when done, and chunk sizes around 8 KB balance syscalls against memory.",
        "example": "with requests.get('https://mirror.example/data.csv.gz', stream=True) as r:\n    out = open('data.csv.gz', 'wb')\n    for chunk in r.iter_content(chunk_size=8192):\n        out.write(chunk)\n    out.close()",
        "usecase": "Downloading large media and datasets without exhausting memory, even on servers with small heaps.",
        "category": "requests"
    },
    {
        "id": 35,
        "title": "sessions keep state warm",
        "definition": "A Session persists cookies in a jar, reuses keep-alive connections and merges default headers into every call, giving a browser-like continuity to programmatic flows. Login once on a session and following calls carry the session cookie automatically, while connection reuse cuts the latency of repeated requests.",
        "example": "s = requests.Session()\ns.post('https://app.example/login', data={'u': 'ada', 'p': 's3cret'})\ns.get('https://app.example/settings')   # carries the session cookie\nme = s.get('https://app.example/me').json()\nprint(me['email'])",
        "usecase": "Sequential API calls that share auth cookies or keep-alive benefits without re-logging in per request.",
        "category": "requests"
    },
    {
        "id": 36,
        "title": "auth in one line",
        "definition": "Passing a (user, password) tuple handles HTTP Basic auth, encoding credentials per RFC 7617; HTTPDigestAuth covers challenge-response servers instead. Both slot into the same auth= argument, and for OAuth or bearer tokens a custom AuthBase subclass updates the Authorization header exactly how the provider expects.",
        "example": "r1 = requests.get('https://api.example.com', auth=('user', 'secret'))\nfrom requests.auth import HTTPDigestAuth\nr2 = requests.get('https://old-app.example', auth=HTTPDigestAuth('user', 'secret'))",
        "usecase": "Internal tools and vendor APIs protected by HTTP Basic or Digest authentication, in one line.",
        "category": "requests"
    },
    {
        "id": 37,
        "title": "timeout or hang for life",
        "definition": "The default timeout is None, meaning requests will wait forever — one dead endpoint freezes the whole thread and everything downstream of it. A scalar bounds both phases; a tuple like (3.05, 27) separately bounds connect and read, so slow-but-alive servers still finish instead of being cut off.",
        "example": "try:\n    r = requests.get('https://api.example.com/orders',\n                     timeout=(3.05, 27))\nexcept requests.exceptions.Timeout:\n    print('no answer within bounds — failing fast')",
        "usecase": "Any network call where a dead endpoint must fail fast instead of stalling queues, workers or UIs.",
        "category": "requests"
    },
    {
        "id": 38,
        "title": "raise_for_status, then sleep",
        "definition": "4xx and 5xx responses do not raise by default, so a silent 500 can flow into your data as if it were a success. Calling raise_for_status() turns bad status codes into catchable HTTPError exceptions; pairing it with a time.sleep retry loop copes with 429 and 503 bursts gracefully.",
        "example": "import time\n\nfor attempt in range(3):\n    r = requests.get('https://api.example.com/sync')\n    try:\n        r.raise_for_status()\n        break\n    except requests.exceptions.HTTPError:\n        time.sleep(2 ** attempt)\nprint(r.json())",
        "usecase": "Turning silent 404s and 500s into catchable exceptions, with retry backoff for rate-limited endpoints.",
        "category": "requests"
    },
    {
        "id": 39,
        "title": "redirects, follow or not",
        "definition": "requests follows 3xx redirects automatically, and r.history keeps every hop along the way. Setting allow_redirects=False returns the redirect response itself, exposing the Location header, status and headers — exactly what an auditor needs to see where a chain leads before the client takes it.",
        "example": "r = requests.get('https://lnk.example/abc', allow_redirects=False)\nprint(r.status_code, r.headers.get('Location'))\nfor hop in requests.get('https://lnk.example/abc').history:\n    print(hop.url, '->', hop.status_code)",
        "usecase": "Inspecting Location headers, counting hops, and capturing short links without silently following them.",
        "category": "requests"
    },
    {
        "id": 40,
        "title": "retry with urllib3 backoff",
        "definition": "Mounting an HTTPAdapter configured with urllib3's Retry gives automatic retries with exponential backoff; backoff_factor spaces attempts at growing intervals while status_forcelist marks which HTTP codes deserve another try. Only bytes with these adapters retry, so control stays explicit and per scheme.",
        "example": "from requests.adapters import HTTPAdapter\nfrom urllib3.util.retry import Retry\n\npolicy = Retry(total=3, backoff_factor=0.5, status_forcelist=[429, 500, 503])\nwith requests.Session() as s:\n    s.mount('http://', HTTPAdapter(max_retries=policy))\n    s.mount('https://', HTTPAdapter(max_retries=policy))\n    data = s.get('https://api.example.com/jobs').json()",
        "usecase": "Flaky networks and rate-limited APIs that need graceful, self-pacing retries instead of immediate failure.",
        "category": "requests"
    },
    {
        "id": 41,
        "title": "verify=False, only with caution",
        "definition": "SSL verification is on by default; verify=False disables certificate checking entirely, removing protection against interception — fine for throwaway tests against self-signed dev servers, never for production. Prefer verify='/path/to/ca.pem' or the REQUESTS_CA_BUNDLE environment variable when a real certificate only needs a custom trust root.",
        "example": "r = requests.get('https://devbox.local/api', verify=False)  # dev only\nr2 = requests.get('https://devbox.local/api', verify='dev-ca.pem')  # safer",
        "usecase": "Local HTTPS dev servers and certificates you trust but cannot chain — bypass only where the stakes are near zero.",
        "category": "requests"
    },
    {
        "id": 42,
        "title": "proxies without leaks",
        "definition": "Pass proxies as a dict keyed by scheme so HTTP and HTTPS take separate roads; no_proxy and localhost entries bypass the proxy to keep internal traffic direct. Combining proxies with a Session reuses the same routes across all calls, avoiding the classic leak of one unproxied request outing the client.",
        "example": "proxies = {'http': 'http://10.0.0.1:8080',\n           'https': 'http://10.0.0.1:8080',\n           'no_proxy': 'localhost,127.0.0.1,*.internal'}\nwith requests.Session() as s:\n    s.proxies.update(proxies)\n    r = s.get('https://outbound.example/api')",
        "usecase": "Testing behind corporate proxies, rotating egress IPs, or anonymous tunneling without unintended traffic leaks.",
        "category": "requests"
    },
    {
        "id": 43,
        "title": "custom headers for APIs",
        "definition": "The headers= argument sets Authorization, Accept, X-API-Key or anything else the server requires, matched case-insensitively and merged over any session defaults. Headers carrying secrets should come from environment variables or config, never hardcoded — and per-call headers let different endpoints share one client.",
        "example": "import os\n\nheaders = {\n    'Authorization': f'Bearer {os.environ[\"API_TOKEN\"]}',\n    'Accept': 'application/vnd.acme.v2+json',\n    'X-Client': 'etl-prod',\n}\nr = requests.get('https://api.example.com/items', headers=headers)\nprint(r.status_code)",
        "usecase": "Token auth, API versioning and content negotiation where every request must declare its intent.",
        "category": "requests"
    },
    {
        "id": 44,
        "title": "cookies without the session",
        "definition": "The cookies= argument sends cookies on one request, and r.cookies reads whatever the response set, both without building a Session. A dict, a RequestsCookieJar or a stdlib cookiejar all work, which makes single-shot calls to cookie-gated endpoints lightweight instead of ceremony-heavy.",
        "example": "r1 = requests.get('https://app.example/login', data=login)\n\nr2 = requests.get('https://app.example/dashboard',\n                  cookies={'sessionid': r1.cookies['sessionid']},\n                  headers={'X-CSRF': r1.cookies['csrftoken']})\nprint(r2.status_code)",
        "usecase": "A single call that needs a known cookie — carried from a previous response — without maintaining a Session.",
        "category": "requests"
    },
    {
        "id": 45,
        "title": "compressed responses for free",
        "definition": "requests sends Accept-Encoding automatically and decompresses gzip or deflate responses transparently, so r.text and r.json() see plain data while the wire carries a fraction of the bytes. Adding optional brotli support extends that to br-encoded payloads, shrinking sizable API downloads further at zero code cost.",
        "example": "r = requests.get('https://api.example.com/reports/export')\nrows = r.json()\nprint('len(decoded):', len(r.content))\nprint('wire size:   ', r.raw.headers.get('content-length'))",
        "usecase": "Saving bandwidth on sizable API payloads and exports without any extra code — compression handled silently.",
        "category": "requests"
    },
    {
        "id": 46,
        "title": "status, headers, and body parts",
        "definition": "r.status_code, r.headers, r.url, r.history and r.request expose every facet of the exchange: what was sent, how it was answered, and through which chain. Headers arrive as a case-insensitive dict and the request attribute echoes the exact bytes that went out — a full audit from one object.",
        "example": "r = requests.get('https://api.example.com/users/7')\nprint(r.status_code, r.reason)\nprint('requested:', r.request.method, r.request.url)\nprint('headers:' , dict(r.headers))\nfor hop in r.history:\n    print(hop.url, hop.status_code)",
        "usecase": "Debugging redirect chains and reconstructing exactly what was sent when a server misbehaves.",
        "category": "requests"
    },
    {
        "id": 47,
        "title": "prepared requests for replay",
        "definition": "A PreparedRequest fixes every detail of an HTTP call — URL, headers, body, cookies — in advance, ready to be sent repeatedly by a Session. Preparing once and sending many times enables exact replays, request signing before transmission, and logging the precise bytes that leave the process.",
        "example": "from requests import Request, Session\n\nprepped = Request('GET', 'https://api.example.com/items',\n                  params={'page': 1},\n                  headers={'Accept': 'application/json'}).prepare()\n\nwith Session() as s:\n    for attempt in range(3):\n        resp = s.send(prepped)\n        if resp.ok:\n            break",
        "usecase": "Signing or signing-and-replaying identical requests, and retry loops that must resend byte-for-byte the same call.",
        "category": "requests"
    },
    {
        "id": 48,
        "title": "encoding and app/json bodies",
        "definition": "r.encoding controls how bytes become text, nullable to whatever header the server declared; .json() parses structured bodies directly into Python values. When servers mislabel charsets, setting r.encoding before reading r.text fixes mojibake, and r.apparent_encoding guesses the real charset for undocumented payloads.",
        "example": "r = requests.get('https://api.example.com/users/7')\nr.encoding = 'utf-8'                      # force what the header got wrong\nprint(r.text)\npayload = r.json()                        # or skip text entirely\nprint(payload['name'], payload['email'])",
        "usecase": "Mixed-encoding APIs and messy text payloads that need explicit decoding before parsing.",
        "category": "requests"
    },
    {
        "id": 49,
        "title": "httpx for modern async",
        "definition": "httpx keeps the requests API but adds first-class async: AsyncClient with await, HTTP/2, pluggable transports for offline testing, and cleaner timeout handling. Code migrates mostly by swapping imports, so legacy sync clients gain modern concurrency in one dependency change.",
        "example": "import httpx, asyncio\n\nasync def fetch_all(urls):\n    async with httpx.AsyncClient(http2=True, timeout=10.0) as client:\n        resp = await client.get(urls[0])\n        return resp.json()\n\nprint(asyncio.run(fetch_all(['https://api.example.com/status'])))",
        "usecase": "Async clients, HTTP/2, and more configurable encodings than requests offers — with a familiar API to ease migration.",
        "category": "requests"
    },
    {
        "id": 50,
        "title": "mocking HTTP with responses",
        "definition": "The responses library intercepts outbound HTTP and returns registered stubs, so code that calls requests is testable without sockets or flaky connectivity. Decorators and context managers scope the stubs, assertions inspect recorded calls, and canned bodies with real status codes make failure paths reproducible.",
        "example": "import requests, responses\n\n@responses.activate\ndef test_retry_on_503():\n    responses.add(responses.GET, 'https://api.example.com', status=503)\n    responses.add(responses.GET, 'https://api.example.com', status=200,\n                  json={'ok': True})\n    r = requests.get('https://api.example.com')\n    assert r.json() == {'ok': True}\n    assert len(responses.calls) == 2",
        "usecase": "Fast, deterministic tests for code that depends on external services — failures and edge cases included.",
        "category": "requests"
    }
]
