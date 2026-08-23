export interface FeedCategory {
  id: string;
  label: string;
  blurb: string;
}

export const FEED_CATEGORIES: FeedCategory[] = [
  { id: "python", label: "Python core", blurb: "idioms · stdlib · gotchas" },
  { id: "django", label: "Django", blurb: "batteries-included web framework" },
  { id: "fastapi", label: "FastAPI", blurb: "modern async APIs" },
  { id: "flask", label: "Flask", blurb: "micro-framework" },
  { id: "pytorch", label: "PyTorch", blurb: "deep learning" },
  { id: "tensorflow", label: "TensorFlow", blurb: "ML at scale" },
  { id: "scikit-learn", label: "scikit-learn", blurb: "classic machine learning" },
  { id: "pandas", label: "pandas", blurb: "data wrangling" },
  { id: "numpy", label: "NumPy", blurb: "numeric arrays & math" },
  { id: "scrapy", label: "Scrapy", blurb: "web scraping done right" },
  { id: "requests", label: "Requests / httpx", blurb: "HTTP clients" },
  { id: "sqlalchemy", label: "SQLAlchemy", blurb: "SQL toolkit & ORM" },
  { id: "pytest", label: "pytest", blurb: "testing framework" },
  { id: "asyncio", label: "asyncio", blurb: "async/await runtime" },
  { id: "celery", label: "Celery", blurb: "distributed task queue" },
  { id: "airflow", label: "Airflow", blurb: "pipeline orchestration" },
  { id: "pydantic", label: "Pydantic", blurb: "validation & settings" },
  { id: "streamlit", label: "Streamlit", blurb: "data apps in minutes" },
];

const CORE_PYTHON_CATEGORIES = [
  "idioms",
  "strings",
  "iterables",
  "syntax",
  "dicts",
  "sorting",
  "functions",
  "gotchas",
  "builtins",
  "performance",
  "stdlib",
  "typing",
  "exceptions",
  "sequences",
  "debugging",
  "style",
  "oop",
  "concurrency",
  "testing",
  "packaging",
  "security",
  "tooling",
];

const CORE_PYTHON_SET = new Set(CORE_PYTHON_CATEGORIES);

export function feedCategoryOf(category: string): string {
  return CORE_PYTHON_SET.has(category) ? "python" : category;
}

export function feedLabel(id: string): string {
  return FEED_CATEGORIES.find((c) => c.id === id)?.label ?? id;
}