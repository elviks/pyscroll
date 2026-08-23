TIPS = [
    {
        "id": 1,
        "title": "FastAPI from zero",
        "definition": "A FastAPI() instance with a few typed path operations and uvicorn gives you a fully documented API in minutes. Every route you declare shows up in an automatically generated OpenAPI docs page, complete with schemas and a try-it-yourself UI. From a blank file to a documented, tested endpoint is usually under ten lines.",
        "example": "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get(\"/\")\ndef root():\n    return {\"hello\": \"world\"}\n# run: uvicorn main:app --reload   →  docs at /docs",
        "usecase": "Microservices, internal tools and LLM backends that need speed plus automatic, interactive documentation at /docs — with zero setup beyond installing FastAPI and uvicorn.",
        "category": "fastapi"
    },
    {
        "id": 2,
        "title": "Type hints are validation",
        "definition": "FastAPI reads your type annotations — int, str, list[str], models — and turns them into automatic validation and coercion for query, path and body parameters. Declare the contract in the signature, and invalid input is rejected with a 422 before your function body ever runs.",
        "example": "@app.get(\"/items/\")\ndef items(category: str, page: int = 1, tags: list[str] | None = None):\n    ...\n\n# /items/?category=books&page=0  → 422 (page must be >= 1 if ge=1 set)\n# /items/?category=books&page=2  → works",
        "usecase": "Every route's contract lives in its signature — malformed input dies with a clean 422 at the boundary instead of crashing deep inside handler code.",
        "category": "fastapi"
    },
    {
        "id": 3,
        "title": "Request bodies with Pydantic",
        "definition": "Declare a Pydantic model as a route parameter and FastAPI parses the JSON body into it, validating every field against its type and constraints. Wrong types or missing required fields produce a descriptive 422 automatically. The same model doubles as documentation and as the schema for your client-side types.",
        "example": "from pydantic import BaseModel\n\nclass Order(BaseModel):\n    sku: str\n    qty: int\n\n@app.post(\"/orders/\")\ndef create(order: Order):\n    return {\"order\": order, \"cost\": order.qty * get_price(order.sku)}\n# POST {\"sku\": \"A1\", \"qty\": 3}  → ok\n# POST {\"sku\": \"A1\", \"qty\": \"x\"}  → 422",
        "usecase": "Typed payloads for every POST — the schema is simultaneously the validation logic, the interactive docs, and the contract your frontend or mobile app codes against.",
        "category": "fastapi"
    },
    {
        "id": 4,
        "title": "Response models filter output",
        "definition": "response_model declares the shape of the JSON the endpoint returns, and FastAPI filters and validates the actual response against it. Internal fields — passwords, tokens, private keys — never leak even if the handler returns a fat ORM object, because only declared fields pass through.",
        "example": "from pydantic import BaseModel\n\nclass UserOut(BaseModel):\n    id: int\n    name: str\n\n@app.get(\"/users/{uid}\", response_model=UserOut)\ndef get_user(uid: int):\n    return {\"id\": uid, \"name\": \"Ada\", \"password_hash\": \"...\"}\n# client only ever sees {\"id\": ..., \"name\": ...}",
        "usecase": "Returning ORM objects or internal dicts straight from handlers while guaranteeing the response contains exactly what clients need — nothing sensitive, nothing extra.",
        "category": "fastapi"
    },
    {
        "id": 5,
        "title": "Dependencies keep handlers thin",
        "definition": "Depends() resolves a callable — auth checks, database sessions, config — and caches its result for the lifetime of the request. A dependency can also raise HTTPException, which turns a shared check into a reusable gate with one line per route. Handlers shrink to the work that is actually specific to them.",
        "example": "from fastapi import Depends, Header, HTTPException\n\ndef require_key(api_key: str = Header()):\n    if api_key != \"secret\":\n        raise HTTPException(status_code=401)\n\n@app.get(\"/private\", dependencies=[Depends(require_key)])\ndef private():\n    return {\"ok\": True}",
        "usecase": "Auth, DB sessions, rate limiters and request context live in one place instead of being copy-pasted into every route — and the same dependency composes across endpoints.",
        "category": "fastapi"
    },
    {
        "id": 6,
        "title": "Query constraints in the type",
        "definition": "Annotated[str, Query(...)] embeds validation directly into the parameter type: min_length, max_length, pattern, ge/le, multiple_of and more. The constraint shows up in the OpenAPI docs and is enforced with a 422 long before your code runs. The type stays the single source of truth for a route's contract.",
        "example": "from typing import Annotated\nfrom fastapi import Query\n\n@app.get(\"/search/\")\ndef search(q: Annotated[str, Query(min_length=2, max_length=100)],\n           page: Annotated[int, Query(ge=1)] = 1):\n    ...",
        "usecase": "Defensive APIs — nonsense ranges and oversized strings die with a 422, not a 500, and every user of the API sees the constraints in the docs.",
        "category": "fastapi"
    },
    {
        "id": 7,
        "title": "HTTPException for clean errors",
        "definition": "Raising HTTPException(status_code, detail) produces a structured JSON error response with the right status code — 404, 403, 409 — instead of a generic 500. Clients can branch on the code and surface a human message from detail.",
        "example": "from fastapi import HTTPException\n\nif not order:\n    raise HTTPException(status_code=404, detail=\"Order not found\")\nif order.owner != current_user:\n    raise HTTPException(status_code=403, detail=\"Not your order\")",
        "usecase": "Explicit 404s, 403s and 409s that frontends parse and display — rather than opaque 500s that mask whether a resource was missing, forbidden or in conflict.",
        "category": "fastapi"
    },
    {
        "id": 8,
        "title": "Custom exception handlers",
        "definition": "@app.exception_handler(SomeError) intercepts a given exception type and converts it into whatever JSON response you choose. It is the place to map domain errors — negative balances, invalid dates, DuplicateError — to clean API errors with precise status codes and messages.",
        "example": "from fastapi import JSONResponse\n\nclass InsufficientFunds(Exception):\n    pass\n\n@app.exception_handler(InsufficientFunds)\nasync def on_funds(request, exc):\n    return JSONResponse(status_code=409, content={\"error\": \"Insufficient funds\"})",
        "usecase": "Throwing a domain exception deep in business logic and having it rendered as a proper API error at the edge — one handler per error type, no try/except noise in every route.",
        "category": "fastapi"
    },
    {
        "id": 9,
        "title": "Uploads with UploadFile",
        "definition": "A route parameter typed UploadFile streams the incoming file to memory (or disk) with metadata like filename and content_type — no manual multipart parsing. Reading is async, so large files stream without blocking the event loop or blowing up memory.",
        "example": "from fastapi import UploadFile, File\n\n@app.post(\"/upload/\")\nasync def upload(file: UploadFile):\n    contents = await file.read()\n    return {\"name\": file.filename, \"bytes\": len(contents)}",
        "usecase": "Image avatars, CSV imports and resume uploads — streaming keeps memory low even for large files, and the filename/content-type arrive validated and ready.",
        "category": "fastapi"
    },
    {
        "id": 10,
        "title": "BackgroundTasks after response",
        "definition": "BackgroundTasks runs a job only after the response is sent to the client. The client gets its 200 immediately while slow side effects — sending an email, resizing an image, hitting a webhook — execute afterward. It is an easy, reliable win for fire-and-forget work that doesn't need a queue yet.",
        "example": "from fastapi import BackgroundTasks\n\ndef send_welcome(email: str):\n    ...  # slow network call\n\n@app.post(\"/signup/\", status_code=201)\nasync def signup(data: Signup, tasks: BackgroundTasks):\n    tasks.add_task(send_welcome, data.email)\n    return {\"ok\": True}   # client not blocked by the email",
        "usecase": "Sending welcome emails, generating thumbnails, notifying webhooks — the client gets its response instantly and the heavy lifting finishes after the fact.",
        "category": "fastapi"
    },
    {
        "id": 11,
        "title": "Auth as a dependency",
        "definition": "A get_current_user dependency reads the token, verifies it, and returns the user — every protected route declares user=Depends(get_current_user) and gets the user injected, or a 401/403 if auth fails. One implementation powers all protected endpoints, and it's trivially testable.",
        "example": "from fastapi import Depends, Header, HTTPException\n\ndef get_current_user(authorization: str = Header()):\n    payload = verify_token(authorization)\n    if not payload:\n        raise HTTPException(status_code=401, detail=\"Invalid token\")\n    return load_user(payload[\"sub\"])\n\n@app.get(\"/me\")\ndef me(user=Depends(get_current_user)):\n    return {\"email\": user.email}",
        "usecase": "JWT, OAuth2 or API-key flows where every protected endpoint shares exactly one auth implementation — and the auth logic is testable in isolation.",
        "category": "fastapi"
    },
    {
        "id": 12,
        "title": "CORS in a few lines",
        "definition": "CORSMiddleware tells browsers which origins may call your API. Without it, a frontend on localhost:3000 hitting an API on localhost:8000 is blocked by the browser, not the server. Adding the middleware with the right origins makes cross-origin requests work while keeping the allow-list explicit.",
        "example": "from fastapi.middleware.cors import CORSMiddleware\n\napp.add_middleware(\n    CORSMiddleware,\n    allow_origins=[\"http://localhost:3000\", \"https://app.example.com\"],\n    allow_methods=[\"*\"],\n    allow_headers=[\"*\"],\n)",
        "usecase": "A Next.js frontend on :3000 talking to the API on :8000 — plus real domains in production — all configured in one middleware block instead of an afternoon of header debugging.",
        "category": "fastapi"
    },
    {
        "id": 13,
        "title": "Config from .env with pydantic-settings",
        "definition": "A BaseSettings subclass reads environment variables — or a .env file — into typed attributes with defaults, validating them like any Pydantic model. One settings object centralizes every key, URL and flag, and per-environment values come from the environment rather than code edits.",
        "example": "from pydantic_settings import BaseSettings\n\nclass Settings(BaseSettings):\n    app_name: str = \"pyapi\"\n    database_url: str = \"sqlite:///dev.db\"\n    openai_key: str = \"\"\n\nsettings = Settings()   # reads real env, falls back to defaults",
        "usecase": "Keys, URLs and feature flags differ per environment — one typed settings object answers everywhere, and a forgotten env var fails fast with a clear validation error instead of a mystery crash.",
        "category": "fastapi"
    },
    {
        "id": 14,
        "title": "One DB session per request",
        "definition": "A dependency that yields a session makes FastAPI open it when the route starts, commit on success and close on finish — including automatic rollback on errors via a guard. Handlers just ask for the session and use it, and you never leak a connection or forget session.close().",
        "example": "async def get_session():\n    async with SessionLocal() as session:\n        try:\n            yield session\n            await session.commit()\n        except Exception:\n            await session.rollback()\n            raise\n\n@app.get(\"/posts/\")\nasync def posts(session: AsyncSession = Depends(get_session)):\n    return await session.execute(select(Post)).scalars().all()",
        "usecase": "Every handler gets a clean transaction with automatic commit/rollback — the boilerplate lives in the dependency once, not in each of the fifty routes touching the database.",
        "category": "fastapi"
    },
    {
        "id": 15,
        "title": "async def vs def endpoints",
        "definition": "def endpoints run in a worker thread pool, which keeps the event loop free even if they block; async def endpoints run directly on the loop. Pick def for CPU work or blocking libraries (requests, sync sqlite) and async def for I/O code you can genuinely await — mixing them is normal and correct.",
        "example": "@app.get(\"/crunch\")\ndef heavy():            # runs in a threadpool → loop stays free\n    return perform_cpu_work()\n\n@app.get(\"/fetch\")\nasync def fetch_page():  # awaits → no thread blocked\n    return await httpx.get(\"https://...\")",
        "usecase": "Blending blocking sqlite/requests with httpx/aiohttp in one app without stalling concurrent requests — the framework picks the right execution model per endpoint.",
        "category": "fastapi"
    },
    {
        "id": 16,
        "title": "Stream responses to clients",
        "definition": "StreamingResponse wraps a generator or async generator and sends its chunks to the client as they are produced, keeping the connection open. It turns a slow, batch-computed payload into an early, incremental one — ideal for LLM answers, CSV exports and log tails.",
        "example": "@app.get(\"/stream\")\ndef stream():\n    def gen():\n        for i in range(5):\n            yield f\"chunk {i}...\"\n    return StreamingResponse(gen(), media_type=\"text/plain\")",
        "usecase": "Chat UIs showing tokens as they arrive instead of waiting for a full reply, and exporting huge CSVs without buffering the entire file in memory first.",
        "category": "fastapi"
    },
    {
        "id": 17,
        "title": "lifespan for setup/teardown",
        "definition": "The lifespan async context manager runs once per process — before and after the application serves requests. Database pools, HTTP clients and config refresh belong there, so they are warmed exactly once instead of per request or lazily on first use.",
        "example": "from contextlib import asynccontextmanager\n\n@asynccontextmanager\nasync def lifespan(app):\n    await db.connect()   # startup\n    yield\n    await db.disconnect()   # shutdown\n\napp = FastAPI(lifespan=lifespan)",
        "usecase": "Connecting to a database, warming an HTTP client pool and refreshing configuration exactly once per process — and cleaning up cleanly on graceful shutdown.",
        "category": "fastapi"
    },
    {
        "id": 18,
        "title": "APIRouter keeps it organized",
        "definition": "Routes live on an APIRouter with a prefix and a tag, and the router is mounted onto the app with include_router. As the API grows, routers per domain — users, billing, reports — keep hundreds of endpoints navigable in code and grouped in the docs.",
        "example": "from fastapi import APIRouter\n\nrouter = APIRouter(prefix=\"/items\", tags=[\"items\"])\n\n@router.get(\"/\")\ndef list_items(): ...\n\n@router.post(\"/\")\ndef create_item(): ...\n\napp.include_router(router)",
        "usecase": "Fifty routes in one file become fifty routes across clean domain modules — prefixes, tags and versions stay consistent and the docs reflect the structure.",
        "category": "fastapi"
    },
    {
        "id": 19,
        "title": "limit/offset pagination",
        "definition": "The simplest API pagination: accept limit (page size) and offset (how many to skip) as query params, slice the collection, and return the items plus a pointer to the next batch. It is stateless, cache-friendly and easy for clients to reason about.",
        "example": "@app.get(\"/posts/\")\ndef posts(limit: int = 20, offset: int = 0):\n    items = all_posts[offset:offset + limit]\n    return {\"items\": items, \"next_offset\": offset + len(items)}",
        "usecase": "Feeds and search results stay snappy — clients fetch fixed-size pages instead of dragging the whole table over the wire on every request.",
        "category": "fastapi"
    },
    {
        "id": 20,
        "title": "Middleware wraps all routes",
        "definition": "@app.middleware(\"http\") registers a function that runs before and after every request, for every route. It receives the request, calls next_get_response, and can modify the response on the way out — the right home for security headers, request IDs and timing.",
        "example": "import time\nfrom fastapi import Request\n\n@app.middleware(\"http\")\nasync def instrument(request: Request, call_next):\n    start = time.perf_counter()\n    response = await call_next(request)\n    response.headers[\"X-Processed-In\"] = f\"{time.perf_counter() - start:.1f}\"\n    return response",
        "usecase": "Adding security headers, request IDs for log correlation, response compression or Prometheus timing globally — written once, applied to every route automatically.",
        "category": "fastapi"
    },
    {
        "id": 21,
        "title": "TestClient for API tests",
        "definition": "starlette's TestClient rides on httpx and lets you call your app's endpoints in-process, asserting status codes, JSON bodies and headers without spinning up a server. It runs the full request/response machinery, so contract tests in CI catch broken APIs instantly.",
        "example": "from fastapi.testclient import TestClient\nfrom main import app\n\nclient = TestClient(app)\n\ndef test_get_item():\n    resp = client.get(\"/items/1\")\n    assert resp.status_code == 200\n    assert resp.json()[\"name\"] == \"Widget\"",
        "usecase": "Contract tests for every endpoint in CI — rename a field or change a status code and a test fails immediately, before any client does.",
        "category": "fastapi"
    },
    {
        "id": 22,
        "title": "WebSockets for live updates",
        "definition": "@app.websocket() endpoints keep a persistent bidirectional socket open with a client. After accept(), the handler loops receiving and sending messages in real time — the standard mechanism for push-style features where polling would be wasteful.",
        "example": "@app.websocket(\"/ws\")\nasync def ws(websocket):\n    await websocket.accept()\n    while True:\n        msg = await websocket.receive_text()\n        await websocket.send_text(f\"echo: {msg}\")",
        "usecase": "Chat rooms, live cursor positions, progress bars and stock tickers — data pushes to clients instead of clients polling the API every second.",
        "category": "fastapi"
    },
    {
        "id": 23,
        "title": "Custom field validation",
        "definition": "A @field_validator runs on a field after type checks and lets you transform or reject the value — normalize an email to lowercase, uppercase a SKU, or raise a ValueError for impossible data. The API edge gets clean, consistent values before handlers ever see them.",
        "example": "from pydantic import BaseModel, field_validator\n\nclass Item(BaseModel):\n    sku: str\n\n    @field_validator(\"sku\")\n    @classmethod\n    def upper_sku(cls, v: str) -> str:\n        return v.strip().upper()",
        "usecase": "Normalizing emails, phone numbers and SKUs at the API boundary so every downstream handler and database row sees data in one canonical form.",
        "category": "fastapi"
    },
    {
        "id": 24,
        "title": "Docs need summaries too",
        "definition": "summary, description and tags metadata make the auto-generated OpenAPI docs usable by humans. Without them the docs list endpoints but not what they're for; with them, teammates and consumers scroll a grouped, described, self-explanatory API reference.",
        "example": "from fastapi import FastAPI\n\n@app.get(\n    \"/health\",\n    summary=\"Service health\",\n    description=\"Checks database and cache connectivity.\",\n    tags=[\"ops\"],\n)\ndef health():\n    ...",
        "usecase": "Onboarding teammates on /docs — grouped, described endpoints beat annotated guesswork, and the docs double as the living API contract.",
        "category": "fastapi"
    },
    {
        "id": 25,
        "title": "Standardize 422 errors",
        "definition": "By default FastAPI returns Pydantic's validation errors in a nested, verbose shape. An override of RequestValidationError lets you reshape them into a flat, consistent format your clients can rely on — the same keys everywhere, from any endpoint.",
        "example": "from fastapi.exceptions import RequestValidationError\nfrom fastapi import JSONResponse, Request\n\n@app.exception_handler(RequestValidationError)\nasync def on_validation(request: Request, exc: RequestValidationError):\n    return JSONResponse(status_code=422, content={\n        \"kind\": \"validation_error\",\n        \"errors\": [{\"field\": e[\"loc\"][-1], \"msg\": e[\"msg\"]} for e in exc.errors()],\n    })",
        "usecase": "Mobile and web clients parsing your error shape — consistent validation keys and messages instead of Pydantic's default nesting that changes with versions.",
        "category": "fastapi"
    }
]
