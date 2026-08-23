import type { Tip } from "@/lib/types";

export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function fetchTips(): Promise<Tip[]> {
  try {
    const res = await fetch(`${API_URL}/api/tips`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = (await res.json()) as { tips: Tip[] };
    if (Array.isArray(data.tips) && data.tips.length > 0) return data.tips;
    throw new Error("empty tips payload");
  } catch {
    return FALLBACK_TIPS;
  }
}

export const FALLBACK_TIPS: Tip[] = [
  {
    id: 1,
    title: "Swap two variables",
    definition: "Tuple unpacking lets you exchange two values in a single line — no temp variable needed.",
    example: "a, b = b, a",
    usecase: "Shuffling pairs in card games or rotating buffer indices without touching a temp variable.",
    category: "idioms",
  },
  {
    id: 2,
    title: "F-strings are your friend",
    definition: "F-strings interpolate expressions straight into string literals — the fastest, cleanest way to format text.",
    example: 'name = "Ada"\nprint(f"Hello, {name}! You have {len(name)} letters.")',
    usecase: "Logging user activity, composing API error messages, or printing live stats like f\"{cpu:.1f}% used\".",
    category: "strings",
  },
  {
    id: 3,
    title: "The walrus operator",
    definition: "The walrus (:=) assigns a value and returns it in the same expression, avoiding duplicated work.",
    example: "while chunk := f.read(1024):\n    process(chunk)",
    usecase: "Reading a file in chunks or parsing user input once so the check and the body share the result.",
    category: "syntax",
  },
  {
    id: 4,
    title: "dict.get() never raises",
    definition: "dict.get(key, default) returns a fallback instead of raising KeyError when a key is missing.",
    example: 'value = data.get("key", "fallback")',
    usecase: "Reading config files where optional settings should silently fall back to sensible defaults.",
    category: "dicts",
  },
  {
    id: 5,
    title: "List comprehensions",
    definition: "A comprehension builds a new list from an iterable, combining mapping and filtering in one readable expression.",
    example: "squares = [x * x for x in range(10) if x % 2 == 0]",
    usecase: "Sanitizing user input en masse or extracting valid emails from a scraped contact list.",
    category: "idioms",
  },
  {
    id: 6,
    title: "enumerate() instead of range(len())",
    definition: "enumerate pairs each item with its index as you iterate, so you never juggle indexes by hand.",
    example: "for i, item in enumerate(items, start=1):\n    print(i, item)",
    usecase: "Turning a list of records into a numbered table for a CSV export or a CLI checklist.",
    category: "iterables",
  },
  {
    id: 7,
    title: "Sort with a key",
    definition: "The key parameter tells sorted() how to order items by a computed value without mutating them.",
    example: 'users.sort(key=lambda u: u["age"], reverse=True)',
    usecase: "Ranking leaderboards by score, sorting files by size, or ordering purchases by date.",
    category: "sorting",
  },
  {
    id: 8,
    title: "zip() pairs lists",
    definition: "zip merges multiple sequences into tuples, side by side, until the shortest one runs out.",
    example: "for name, score in zip(names, scores):\n    print(name, score)",
    usecase: "Joining column headers with row values to build CSV rows or pairing product IDs with prices.",
    category: "iterables",
  },
  {
    id: 9,
    title: "Generators save memory",
    definition: "A generator yields items one at a time instead of materializing an entire sequence in memory.",
    example: "nums = (x * x for x in range(10_000_000))\nprint(sum(nums))",
    usecase: "Streaming millions of log lines or API pages without ever loading them all at once.",
    category: "performance",
  },
  {
    id: 10,
    title: "functools.lru_cache",
    definition: "The lru_cache decorator memoizes a function's results, trading memory for huge speedups.",
    example: "@lru_cache(maxsize=None)\ndef fib(n):\n    return n if n < 2 else fib(n - 1) + fib(n - 2)",
    usecase: "Caching expensive database lookups or repeated math computations with identical arguments.",
    category: "performance",
  },
];