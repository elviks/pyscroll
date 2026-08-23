TIPS = [
    {
        "id": 1,
        "title": "Scrapy, the scraping framework",
        "definition": "Scrapy is a full scraping framework rather than a request wrapper: it manages request scheduling, concurrency, retries, deduplication, parsing via selectors, item validation and structured export — all in one asynchronous engine. A project template organizes spiders, items, pipelines and settings from the start.",
        "example": "scrapy startproject shop\ncd shop\nscrapy genspider products example.com",
        "usecase": "Production-grade crawling at scale — a structured pipeline with built-in politeness beats a pile of handwritten request scripts.",
        "category": "scrapy"
    },
    {
        "id": 2,
        "title": "A spider in ten lines",
        "definition": "A spider is a class with three essentials: a name, a list of start_urls and a parse callback. Scrapy requests the start URLs, hands each response to parse, and whatever parse yields — items, requests — is streamed onwards automatically. The minimal spider is almost self-explanatory.",
        "example": "import scrapy\n\nclass QuotesSpider(scrapy.Spider):\n    name = 'quotes'\n    start_urls = ['https://quotes.toscrape.com']\n\n    def parse(self, response):\n        for q in response.css('div.quote'):\n            yield {'text': q.css('span.text::text').get()}",
        "usecase": "The hello world of scraping — extract structured records from a page in one class, run it with scrapy crawl.",
        "category": "scrapy"
    },
    {
        "id": 3,
        "title": "CSS selectors, your first tool",
        "definition": "response.css() runs CSS selectors on the page — the same selectors you use in DevTools — and returns a SelectorList. ::text grabs the text content and ::attr(href) an attribute; .get() returns the first match, .getall() every match. Most extraction starts here.",
        "example": "titles = response.css('h2.title::text').getall()\nlinks = response.css('a.product::attr(href)').getall()",
        "usecase": "Extracting titles, links and prices from structured HTML — the everyday act of scraping, fast and declarative.",
        "category": "scrapy"
    },
    {
        "id": 4,
        "title": "XPath strikes deep",
        "definition": "XPath reaches nodes by document structure — absolute paths, predicates on attributes, parents, text nodes — with power CSS can't match. Combined with the same .get()/.getall() accessors, it handles positions, sibling relationships and markup quirks that CSS selectors can't express.",
        "example": "response.xpath('//div[@class=\"product\"]/span/text()').getall()\nresponse.xpath('//a[contains(@href, \"item\")]/@href').get()",
        "usecase": "Locating elements by attributes or position, or navigating parents and siblings — beyond what CSS alone can reach.",
        "category": "scrapy"
    },
    {
        "id": 5,
        "title": "yield, the scraper's return",
        "definition": "In Scrapy you yield items (and follow-up requests) rather than returning them. Yielding streams results to the pipeline one at a time, keeps memory flat on huge pages, and lets one parse method emit many items — returning a list would hand them all at once and break the pattern.",
        "example": "def parse(self, response):\n    for row in response.css('tr.item'):\n        yield {'sku': row.css('td::text').getall()}\n    next_page = response.css('a.next::attr(href)').get()\n    if next_page:\n        yield response.follow(next_page, self.parse)",
        "usecase": "Streaming many items per page — and chaining the next page — without buffering an entire site in memory at once.",
        "category": "scrapy"
    },
    {
        "id": 6,
        "title": "Follow links with response.follow",
        "definition": "response.follow(url) builds a new request relative to the current page, and yielding it queues it: Scrapy fetches the page and calls the callback you specify. Passing a single callback loops it over every page, so pagination — 1, then 2, then 3 — is three lines, not a loop.",
        "example": "def parse(self, response):\n    ... # extract items\n    next_url = response.css('a.next::attr(href)').get()\n    if next_url:\n        yield response.follow(next_url, callback=self.parse)",
        "usecase": "Pagination and crawl chaining — yield the next link from each page and Scrapy keeps the train moving.",
        "category": "scrapy"
    },
    {
        "id": 7,
        "title": "CrawlSpider, rules for the whole site",
        "definition": "CrawlSpider automates link-following with rules: each Rule pairs a LinkExtractor (what URLs to follow) with a callback (what to do with matches). It recurses through allowed paths automatically, visiting every matching page while skipping everything else — the framework's whole-site mode.",
        "example": "from scrapy.spiders import CrawlSpider, Rule\nfrom scrapy.linkextractors import LinkExtractor\n\nclass Site(CrawlSpider):\n    name = 'site'\n    rules = [Rule(LinkExtractor(allow=r'/product/'),\n                  callback='parse_item')]",
        "usecase": "Whole-domain crawls — declare what to follow, what to parse and what to skip, and let the spider cover the site.",
        "category": "scrapy"
    },
    {
        "id": 8,
        "title": "Item, the schema of a scraper",
        "definition": "Items declare a scraper's fields explicitly — each one a scrapy.Field, often with metadata — instead of relying on loose dicts. Pipelines, loaders and exporters can then rely on a stable shape, and typos in field names surface early rather than silently producing broken records.",
        "example": "import scrapy\n\nclass Product(scrapy.Item):\n    url = scrapy.Field()\n    name = scrapy.Field()\n    price = scrapy.Field()",
        "usecase": "Typed records that pipelines and exporters rely on — validation and readability without raw, shape-shifting dicts.",
        "category": "scrapy"
    },
    {
        "id": 9,
        "title": "pipelines, the processing line",
        "definition": "Every yielded item travels through a chain of pipeline classes, each implementing process_item. Each stage cleans, validates, dedupes or stores a field — like an assembly line — and can drop items by raising DropItem. Spiders stay thin while data quality lives in the pipeline.",
        "example": "class CleanPrices:\n    def process_item(self, item, spider):\n        item['price'] = float(item['price'].replace('$', '').strip())\n        return item",
        "usecase": "Cleaning, validating and persisting scraped data in one organized chain — with each concern in its own pipeline class.",
        "category": "scrapy"
    },
    {
        "id": 10,
        "title": "Scrapy shell, test before you code",
        "definition": "scrapy shell fetches a live URL and drops you into an interactive session with the response loaded as response. You experiment with CSS and XPath selectors against the real page — iterating until the extraction works, then copying exactly what worked into the spider.",
        "example": "scrapy shell https://quotes.toscrape.com\n>>> response.css('div.quote span.text::text').getall()",
        "usecase": "Iterating on selectors against real HTML before writing the spider — the fastest debugging loop in scraping.",
        "category": "scrapy"
    },
    {
        "id": 11,
        "title": "Scrape JSON responses too",
        "definition": "Many modern sites fetch their data as JSON from endpoints behind the UI — and Scrapy handles those natively: response.json() parses the body into Python data structures in one call. Listings, search results, infinite-scroll feeds and API data become items directly.",
        "example": "data = response.json()\nfor rec in data.get('results', []):\n    yield {'id': rec['id'], 'title': rec['title']}",
        "usecase": "APIs and JS-driven sites that expose data behind the UI — grab the JSON endpoint directly instead of scraping rendered HTML.",
        "category": "scrapy"
    },
    {
        "id": 12,
        "title": "Robots and politeness settings",
        "definition": "Scrapy bundles the basics of respectful crawling as settings: ROBOTSTXT_OBEY consults robots.txt before each request, DOWNLOAD_DELAY spaces requests in time, and CONCURRENT_REQUESTS caps in-flight load. Set them and the framework polices your pace automatically.",
        "example": "ROBOTSTXT_OBEY = True\nDOWNLOAD_DELAY = 1.0\nCONCURRENT_REQUESTS = 16",
        "usecase": "Being a good citizen — respecting robots, spacing hits and bounding concurrency so servers aren't hammered and you aren't blocked.",
        "category": "scrapy"
    },
    {
        "id": 13,
        "title": "AUTOTHROTTLE adjusts speed by itself",
        "definition": "AUTOTHROTTLE_ENABLED makes Scrapy adapt its request rate to each server's response times: fast, responsive sites get crawled quickly; slow or throttled ones get paced back automatically. It tunes politeness per-host without manual delay hunting in settings.",
        "example": "AUTOTHROTTLE_ENABLED = True\nAUTOTHROTTLE_START_DELAY = 5.0\nAUTOTHROTTLE_MAX_DELAY = 60.0",
        "usecase": "Slow or rate-limited websites are paced naturally — no hand-tuning delays per site when crawling many domains.",
        "category": "scrapy"
    },
    {
        "id": 14,
        "title": "Request meta, your data satchel",
        "definition": "meta attaches arbitrary data to a request, and the callback reads it back via response.meta — surviving the round trip intact. It is how context travels from a listing page to a detail-page callback: the SKU the link came from, the page depth, the partial record so far.",
        "example": "yield scrapy.Request(\n    url, callback=self.parse_item,\n    meta={'sku': sku, 'list_title': title})",
        "usecase": "Carrying context between parse stages — listing-to-detail flows are the canonical use for request meta.",
        "category": "scrapy"
    },
    {
        "id": 15,
        "title": "Errback, handle failures gracefully",
        "definition": "An errback runs when a request fails — connection refused, timeout, 4xx/5xx — receiving a Twisted Failure instead of the spider dying. Log, count, schedule a retry, or skip cleanly and let the crawl continue; one crawl shouldn't end because one URL is dead.",
        "example": "yield scrapy.Request(url, callback=self.parse, errback=self.on_error)\n\ndef on_error(self, failure):\n    self.logger.error('Failed %s: %s', failure.request.url,\n                      failure.getErrorMessage())",
        "usecase": "Dead links, blocked requests and timeouts — capture the failure, decide the response, and keep the rest of the crawl running.",
        "category": "scrapy"
    },
    {
        "id": 16,
        "title": "Middleware, hook into the pipeline",
        "definition": "Downloader middlewares sit between the engine and the network, intercepting every request and response. A middleware can rewrite headers, swap proxies, implement retries or log traffic — the standard place for cross-cutting concerns like user-agent rotation that don't belong in spiders.",
        "example": "class UAMiddleware:\n    def process_request(self, request, spider):\n        request.headers['User-Agent'] = 'MyCrawler/1.0'\n        return None   # let the request continue",
        "usecase": "Rotating user agents, changing proxies, injecting headers or adding retry logic — globally, once — instead of in every spider.",
        "category": "scrapy"
    },
    {
        "id": 17,
        "title": "Export to JSON/CSV, zero code",
        "definition": "Scrapy exports items without any pipeline: scrapy crawl -o results.json writes JSON, -o results.csv writes CSV, and the FEEDS setting adds format control and incremental appends. Finished crawls land on disk in a consumable format with zero export code.",
        "example": "scrapy crawl quotes -o quotes.json\nscrapy crawl quotes -o quotes.csv\n# or, in settings:\n# FEEDS = {'items.jsonl': {'format': 'jsonlines'}}",
        "usecase": "Delivering scrape output as JSON, CSV or JSON Lines — one flag on the crawl command, no serialization code required.",
        "category": "scrapy"
    },
    {
        "id": 18,
        "title": "Scrapy behind a login (sessions)",
        "definition": "Logging in is an HTTP form post: send the credentials with a FormRequest — copies of the page's form fields, or composed manually — and the session cookie comes back in the next response, carried automatically. Authenticated areas then parse like any other page.",
        "example": "def parse(self, response):\n    yield scrapy.FormRequest.from_response(\n        response,\n        formdata={'username': USER, 'password': PWD},\n        callback=self.after_login)",
        "usecase": "Accessing member-only content and authenticated sections — submit the login form first, then scrape like normal.",
        "category": "scrapy"
    },
    {
        "id": 19,
        "title": "Handle JavaScript-heavy sites",
        "definition": "Pages rendered only by client-side JavaScript need a real browser engine; pairing Scrapy with Splash or Selenium runs the page in a headless browser and hands the rendered HTML back. It's heavier and slower than pure HTTP scraping — the right tool only for genuinely JS-only content.",
        "example": "from scrapy_splash import SplashRequest\n\nyield SplashRequest(url, callback=self.parse, args={'wait': 2})",
        "usecase": "SPAs, infinite-scroll feeds and content that exists only after scripts run — render first, scrape the result.",
        "category": "scrapy"
    },
    {
        "id": 20,
        "title": "Cookies and session persistence",
        "definition": "COOKIES_ENABLED keeps a per-spider cookie jar that persists across requests, so sessions, CSRF tokens and shopping carts survive redirects and page hops. For stateless scraping it can be switched off to trim requests and shrink the fingerprint a site can see.",
        "example": "COOKIES_ENABLED = True      # persist a session\n# or\nCOOKIES_ENABLED = False     # stateless, minimal footprint",
        "usecase": "Sites that rely on cookies for sessions, carts or CSRF tokens — enabled by default so those flows just work.",
        "category": "scrapy"
    },
    {
        "id": 21,
        "title": "DEPTH_LIMIT stops deep crawls",
        "definition": "DEPTH_LIMIT caps how many link-hops from the start URLs a spider will descend. On a CrawlSpider that would otherwise wander the whole linked universe, a depth limit confines the crawl to the first two or three levels — exactly the slice of the site you actually wanted.",
        "example": "DEPTH_LIMIT = 2    # start page + one more level",
        "usecase": "Confining site-wide crawls to the top levels — structure first, everything below stays untouched.",
        "category": "scrapy"
    },
    {
        "id": 22,
        "title": "Item loaders, structured extraction",
        "definition": "ItemLoader assembles an item field-by-field: add_css and add_xpath append values from selectors, and processors filter them — MapCompose chains functions like strip, clean and float in sequence. Extraction and normalization happen per field in one place, instead of scattered in the spider.",
        "example": "from scrapy.loader import ItemLoader\nfrom itemloaders.processors import MapCompose\n\nloader = ItemLoader(item=Product(), response=response)\nloader.add_css('price', '.price::text',\n               MapCompose(str.strip, float))",
        "usecase": "Processing each field consistently — cleaning and typing at extraction time, especially on sites with inconsistent markup.",
        "category": "scrapy"
    },
    {
        "id": 23,
        "title": "Stats, know thy crawl",
        "definition": "Every run produces a statistics report: pages crawled, items scraped, requests made, errors caught — shown at the end of each crawl and queryable via the crawler's stats object. A quick glance answers whether a crawl actually fetched what you wanted or silently half-failed.",
        "example": "scrapy crawl quotes -L CRITICAL 2>&1 | tail -40\n# item_scraped_count: 100   response_received_count: 12",
        "usecase": "Monitoring crawl health — seeing at a glance whether pages were scraped and items flowed, before trusting the output.",
        "category": "scrapy"
    },
    {
        "id": 24,
        "title": "Download images with middleware",
        "definition": "ImagesPipeline automates asset fetching: list image URLs in an item field, yield the URLs as media requests, and the pipeline downloads, validates and even resizes them into the item. Product catalogs and photo sites get their images saved without writing a byte of file code.",
        "example": "class DownloadImages(ImagesPipeline):\n    def get_media_requests(self, item, info):\n        yield scrapy.Request(item['image_url'])",
        "usecase": "Automatically fetching product images or assets from scraped pages — deduplicated, validated and stored for you.",
        "category": "scrapy"
    },
    {
        "id": 25,
        "title": "Per-spider settings",
        "definition": "custom_settings on a spider class overrides project-wide settings for that spider only. A fast spider and a polite spider coexist in one project, each with its own delays, concurrency and pipelines — configuration scoped where the behavior actually differs.",
        "example": "class DailyCheck(scrapy.Spider):\n    name = 'daily'\n    custom_settings = {\n        'DOWNLOAD_DELAY': 2.0,\n        'COOKIES_ENABLED': True,\n        'CONCURRENT_REQUESTS': 4,\n    }",
        "usecase": "Different workloads in one project — heavy crawls and light checks each tuned independently, without global rewrite.",
        "category": "scrapy"
    },
    {
        "id": 26,
        "title": "Sitemaps, the express lane",
        "definition": "SitemapSpider reads a site's sitemap.xml, walks its URLs and hands each to a callback — no link discovery, no page-by-page crawling. When a site publishes its map, this is the fastest, politest way to enumerate every page it considers canonical.",
        "example": "class Blog(SitemapSpider):\n    name = 'blog'\n    sitemap_urls = ['https://site.com/sitemap.xml']\n\n    def parse(self, response):\n        yield {'url': response.url,\n               'title': response.css('h1::text').get()}",
        "usecase": "Respecting sites that publish sitemaps — crawl by the map, hitting every intended page in one structured pass.",
        "category": "scrapy"
    },
    {
        "id": 27,
        "title": "Robust error handling in callbacks",
        "definition": "Flaky networks fail requests unpredictably, so robust spiders pair errbacks with the retry middleware: transient HTTP codes are retried a few times with backoff while permanent failures are routed to an error handler. Resilience becomes configuration plus one callback, not scattered try/excepts.",
        "example": "RETRY_ENABLED = True\nRETRY_TIMES = 3\nRETRY_HTTP_CODES = [500, 502, 503, 504]\n\n# spider:\nyield scrapy.Request(url, callback=self.parse, errback=self.on_error)",
        "usecase": "Surviving temporary server outages mid-crawl instead of losing data — retry transient failures, log the rest.",
        "category": "scrapy"
    },
    {
        "id": 28,
        "title": "Scrapy selectors support regex",
        "definition": "Selector.re() and re_first() extract text matching a regular expression directly from selector text — xpath('//span/text()').re(r'pattern'). When structured attributes are inconsistent but the data follows a shape — SKUs, order numbers, prices — regex pulls them out cleanly.",
        "example": "skus = response.css('span.sku::text').re(r'[A-Z]{2}\\d{4}')\nprice = response.xpath('//div[contains(@class, \"price\")]/text()').re_first(r'\\$\\s*([\\d.]+)', 1)",
        "usecase": "Pulling SKUs, IDs or embedded numbers that follow a pattern — extraction by shape, not by element boundaries.",
        "category": "scrapy"
    },
    {
        "id": 29,
        "title": "dont_filter and duplicate handling",
        "definition": "Scrapy fingerprints every URL and skips repeats by default — which is right for crawls, wrong for re-fetching. Setting dont_filter=True explicitly bypasses the dedup filter for cases where the same URL genuinely needs to be requested again. Use it deliberately, not by default.",
        "example": "yield scrapy.Request(url, callback=self.parse, dont_filter=True)",
        "usecase": "Re-scraping a volatile page, or intentionally visiting identical query strings, without the dedup filter blocking them.",
        "category": "scrapy"
    },
    {
        "id": 30,
        "title": "The Scrapy docs are your friend",
        "definition": "Scrapy documents every aspect exhaustively: settings reference, extension API, spider contracts, item loaders and middleware tutorials. Before re-inventing a feature, one doc search usually uncovers it — and the shell's built-in help mirrors key APIs for quick consultation.",
        "example": "scrapy settings --get DOWNLOAD_DELAY\n# docs.scrapy.org sections: Topics, API Reference, Settings",
        "usecase": "Learning one documented feature properly beats a battery of half-known workarounds — the docs answer most design questions early.",
        "category": "scrapy"
    },
    {
        "id": 31,
        "title": "parse first, scrape second",
        "definition": "Keep spiders focused on extraction and move parsing, validation and transformation into item pipelines or separate helper modules. Spiders stay thin and testable; parsing logic can be unit-tested without crawling; and pipeline failures skip a single item instead of aborting the whole run.",
        "example": "# spider yields raw cells, untouched:\nyield {'price': raw_price_cell, 'url': url}\n\n# pipeline parses to Python types and validates:\nitem['price'] = float(item['price'].strip().lstrip('$'))",
        "usecase": "Testing parsing independently of crawling, and gracefully skipping bad rows — clean separation of concerns makes both easy.",
        "category": "scrapy"
    },
    {
        "id": 32,
        "title": "reuse request headers across a site",
        "definition": "Overriding start_requests lets you attach default headers — Accept-Language, custom UA, auth tokens — to every request the spider makes. Requests inherit the base headers unless they override them, so one definition configures the whole crawl instead of touching each Request call.",
        "example": "def start_requests(self):\n    for u in self.start_urls:\n        yield scrapy.Request(\n            u,\n            headers={'Accept-Language': 'en',\n                     'User-Agent': 'ShopCrawler/1.0'})",
        "usecase": "Sites that return different content per locale or user-agent — set rich defaults once and every page inherits them.",
        "category": "scrapy"
    },
    {
        "id": 33,
        "title": "matching URLs with spider rules",
        "definition": "In a CrawlSpider, each Rule combines a LinkExtractor — a pattern for which hrefs to follow — with a callback for pages that match. Rules are checked in order, the first match wins, and the response goes to its callback; predictable, pattern-following sites fold into a few clean lines.",
        "example": "rules = [\n    Rule(LinkExtractor(allow=r'/product/\\d+'),\n         callback='parse_item'),\n    Rule(LinkExtractor(allow=r'/category/.+'),\n         follow=True),   # keep following, no parsing\n]",
        "usecase": "E-commerce catalogs and any site with predictable, paginated listing URLs — express the crawl as rules instead of code.",
        "category": "scrapy"
    },
    {
        "id": 34,
        "title": "yield facts, not pages",
        "definition": "Yield scraped data as dicts or Item instances rather than returning them — yielding streams one record at a time into the pipeline, keeping memory flat and letting later stages start before the crawl finishes. Return ends the callback; yield feeds the machine.",
        "example": "def parse(self, response):\n    for row in response.css('tr.product'):\n        yield {\n            'title': row.css('h3::text').get(),\n            'price': row.css('.price::text').get(),\n        }",
        "usecase": "Feeding pipelines batch-by-batch instead of buffering an entire site in memory — the correct Scrapy idiom for any volume.",
        "category": "scrapy"
    },
    {
        "id": 35,
        "title": "robots, delay, and rate",
        "definition": "Three settings encode politeness: ROBOTSTXT_OBEY consults robots.txt before each request, DOWNLOAD_DELAY spaces requests in time, and CONCURRENT_REQUESTS bounds how many are in flight at once. Together they turn a scatter-gun scraper into a considerate one — out of the box.",
        "example": "settings = {\n    'ROBOTSTXT_OBEY': True,\n    'DOWNLOAD_DELAY': 1.0,\n    'CONCURRENT_REQUESTS': 16,\n}",
        "usecase": "Staying polite, avoiding bans and keeping crawlers production-safe — the settings exist precisely so you remember to set them.",
        "category": "scrapy"
    },
    {
        "id": 36,
        "title": "pagination via follow styles",
        "definition": "The classic pagination pattern: parse the current page for items, find the next link, and yield a follow-up request for it — repeat until the link disappears. Explicit follows also coexist peacefully with auto-throttle and request timing, which pace the sequence for you.",
        "example": "def parse(self, response):\n    for item in response.css('.thing'):\n        yield self.item_from(response, item)\n    next_url = response.css('a.next::attr(href)').get()\n    if next_url:\n        yield response.follow(next_url, callback=self.parse)",
        "usecase": "Handling discovery when page numbers aren't in a clean URL pattern — follow the click path the site itself offers.",
        "category": "scrapy"
    },
    {
        "id": 37,
        "title": "feed exports, no code",
        "definition": "The FEEDS setting (or the -o flag) writes every scraped item to files in JSON, CSV, JSON Lines or XML — with append/overwrite modes and per-format wrappers. One-off crawls that just need results on disk gain an exporter with zero pipeline code.",
        "example": "# command line:\nscrapy crawl quotes -o results.json\n# or in settings:\nFEEDS = {'results.jsonl': {'format': 'jsonlines'}}",
        "usecase": "Quick crawls that just need results on disk for later analysis — structured export without writing a serializer.",
        "category": "scrapy"
    },
    {
        "id": 38,
        "title": "debugging with scrapy shell",
        "definition": "scrapy shell fetches a URL and hands you the response in an interactive session, so CSS and XPath selectors can be tried against the real HTML before committing them to code. The shell also exposes helpers like fetch, view and your spider's settings for full investigation.",
        "example": "scrapy shell 'https://example.com/item/42'\n>>> response.css('h1::text').get()\n>>> view(response)    # open in a browser",
        "usecase": "Trying selectors against live pages and inspecting exactly what a callback will receive — before writing the spider.",
        "category": "scrapy"
    },
    {
        "id": 39,
        "title": "request meta passes data along",
        "definition": "meta is a dict attached to a request that survives the round trip and is readable in the callback as response.meta — even across redirects and retries. It is the sanctioned way to thread context between parse stages, such as carrying the listing data into a detail-page callback.",
        "example": "def parse_listing(self, response):\n    for link in response.css('a.item::attr(href)').getall():\n        yield scrapy.Request(\n            response.urljoin(link),\n            callback=self.parse_item,\n            meta={'list_shown': True, 'rank': 7})",
        "usecase": "Passing page numbers, source URLs or partial data between parse stages — context that follows the request wherever it goes.",
        "category": "scrapy"
    },
    {
        "id": 40,
        "title": "pipelining for cleaning",
        "definition": "ITEM_PIPELINES lists pipeline classes with priority numbers; items traverse them in ascending order, each process_item cleaning, validating, enriching or storing a stage. Concern separation means the spider extracts, one pipeline dedupes, another cleans prices, another writes to the database.",
        "example": "ITEM_PIPELINES = {\n    'shop.pipelines.DropDuplicates': 200,\n    'shop.pipelines.CleanFields': 300,\n    'shop.pipelines.StoreItem': 800,\n}",
        "usecase": "Separating concerns so spiders stay thin and data quality stays high — each small processor is testable on its own.",
        "category": "scrapy"
    },
    {
        "id": 41,
        "title": "middleware for the gray areas",
        "definition": "Downloader middlewares intercept every request and response as they cross the network boundary, letting you inject behavior globally: rotate user agents, cycle proxies, add retry logic or rewrite cookies. Sites that fingerprint by UA or IP get handled in one place, not in each spider.",
        "example": "class RotateUserAgent:\n    def process_request(self, request, spider):\n        request.headers['User-Agent'] = next(USER_AGENTS)\n        return None",
        "usecase": "Sites that rate-limit or fingerprint by user agent, IP or cookie trail — one middleware covers every spider at once.",
        "category": "scrapy"
    },
    {
        "id": 42,
        "title": "collect stats without printing",
        "definition": "The crawler's stats object records named counters throughout a run — inc_value, set_value, max_value — with built-ins already tracking pages, items and errors. Custom counters live alongside them and land in the final report, giving crawl health a number instead of a log dump.",
        "example": "def parse(self, response):\n    self.crawler.stats.inc_value('items_seen')\n    self.crawler.stats.set_value('last_url', response.url)",
        "usecase": "Monitoring crawl health — and detecting the silent failure of a common pattern — through the report's stats.",
        "category": "scrapy"
    },
    {
        "id": 43,
        "title": "item loaders for messy data",
        "definition": "ItemLoaders normalize fields at extraction time: add_css/add_xpath feed raw values through input processors (MapCompose chains strip, clean, float), and output processors produce the final field. Messy sites with inconsistent markup get their cleaning centralized per field.",
        "example": "loader = ItemLoader(item=Product(), selector=response)\nloader.add_xpath('price', './/span[contains(@class, \"price\")]/text()',\n                 MapCompose(str.strip, float))\nitem = loader.load_item()",
        "usecase": "Sites with inconsistent markup or prices needing currency symbols stripped — normalization lives at extraction, not downstream.",
        "category": "scrapy"
    },
    {
        "id": 44,
        "title": "sitemap-driven discovery",
        "definition": "SitemapSpider reads the sitemap.xml URLs and dispatches each one to a callback, with sitemap_rules pairing URL patterns to handlers. No crawling between pages — just the canonical list of pages the site itself declares, requested in order.",
        "example": "class BlogSpider(SitemapSpider):\n    name = 'blog'\n    sitemap_urls = ['https://site.com/sitemap.xml']\n    sitemap_rules = [('/posts/', 'parse_post')]",
        "usecase": "The fastest, politest enumeration of a site — when sitemaps exist, why discover pages by following links?",
        "category": "scrapy"
    },
    {
        "id": 45,
        "title": "retry and error budgets",
        "definition": "The retry middleware re-requests transient failures automatically — configurable via RETRY_TIMES and RETRY_HTTP_CODES — so a 503 blip doesn't lose a page. Temporary 'too busy' answers get a second chance while permanent errors pass through to logging or errbacks.",
        "example": "RETRY_TIMES = 3\nRETRY_HTTP_CODES = [500, 502, 503, 504, 429]\nRETRY_PRIORITY_ADJUST = -1",
        "usecase": "Handling flaky hosts gracefully — retry overload signals a few times, but never hammer a permanently-failing URL.",
        "category": "scrapy"
    },
    {
        "id": 46,
        "title": "don't filter, dodge duplicates",
        "definition": "Scrapy fingerprints URLs and never requests the same one twice — right for crawls, wrong when you truly must revisit. dont_filter=True bypasses the dedup filter for that specific request: re-scraping a volatile page, or deliberately re-hitting identical query strings.",
        "example": "yield scrapy.Request(url, callback=self.parse, dont_filter=True)",
        "usecase": "Refetching a changing page each pass or explicitly crawling the same URL many times — opt out of dedup deliberately.",
        "category": "scrapy"
    },
    {
        "id": 47,
        "title": "shadows with nested selectors",
        "definition": "Nested traversal: select a container with CSS or XPath, then query within it with relative selectors, avoiding brittle long paths from document top. Cards, rows and offers with repeated structure get parsed per block — robust when page layout shifts around them.",
        "example": "for card in response.css('div.offer'):\n    title = card.css('h3::text').get()\n    price = card.css('.price::text').get()",
        "usecase": "Lists of cards, rows or offers where the structure repeats — isolate the block, then extract within it.",
        "category": "scrapy"
    },
    {
        "id": 48,
        "title": "crawl once, update often",
        "definition": "Long-running scrapers pair a full crawl with frequent lighter passes: store a fingerprint of known records and re-fetch only what changed. Hashing key fields and comparing to the stored state makes price trackers and changelog watchers cheap instead of re-scraping everything daily.",
        "example": "stored = load_state()          # {url: content_hash}\nfor url, page in fetched.items():\n    h = md5(page_text)\n    if stored.get(url) != h:\n        emit_change(url)        # only diffs go out\n        stored[url] = h\nsave_state(stored)",
        "usecase": "Price trackers, changelog watchers and sites that change daily — fetch only the delta, keep state between runs.",
        "category": "scrapy"
    },
    {
        "id": 49,
        "title": "asynchronous pagination control",
        "definition": "Pagination is naturally async: yielding a follow-up request queues it without blocking, and Scrapy interleaves the backlog — several pages in flight at once, deduplicated against repeats. Order and depth emerge from the queue discipline, which is why 'yield next' beats nested loops for crawls.",
        "example": "def parse(self, response):\n    ... # extract items\n    for url in response.css('a.page::attr(href)').getall():\n        yield response.follow(url, callback=self.parse)",
        "usecase": "Deep category trees and multi-branch crawls where concurrency pipelines the queue — wait-free, self-regulating.",
        "category": "scrapy"
    },
    {
        "id": 50,
        "title": "turning off cookie greed",
        "definition": "COOKIES_ENABLED=False stops Scrapy from storing or sending cookies, giving every request a stateless, fresh identity. For sites that don't need sessions it shrinks the request footprint, reduces what a site can fingerprint about you, and removes cross-request session state entirely.",
        "example": "COOKIES_ENABLED = False    # stateless requests",
        "usecase": "Uncluttering requests, shrinking footprints and reducing bot-detection surface — enable cookies only where sessions matter.",
        "category": "scrapy"
    }
]
