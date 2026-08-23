"use client";

import { useEffect, useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { API_URL } from "@/lib/api";
import { setUserMeta } from "@/lib/db";
import { checkAchievements } from "@/lib/achievements";
import AchievementToast from "@/components/AchievementToast";
import { TerminalIcon, PlayIcon } from "@/components/icons";
import CodeEditor from "@/components/CodeEditor";

const EXAMPLES = [
  {
    name: "Fibonacci",
    code: 'def fib(n):\n    a, b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a\n\nprint([fib(i) for i in range(10)])',
  },
  {
    name: "Counter",
    code: 'from collections import Counter\n\ntext = "the quick brown fox jumps over the lazy dog"\nfor word, count in Counter(text.split()).most_common(3):\n    print(f"{word:5} {count}")',
  },
  {
    name: "FizzBuzz",
    code: 'for i in range(1, 21):\n    out = ""\n    if i % 3 == 0: out += "Fizz"\n    if i % 5 == 0: out += "Buzz"\n    print(out or i)',
  },
  {
    name: "Classes",
    code: 'class Dog:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\n\n    def bark(self):\n        return f"{self.name} says Woof!"\n\nrex = Dog("Rex", 5)\nprint(rex.bark())\nprint(f"Age: {rex.age}")',
  },
  {
    name: "Comprehensions",
    code: 'squares = [x**2 for x in range(10)]\nevens  = [x for x in squares if x % 2 == 0]\n\nprint("Squares:", squares)\nprint("Evens: ", evens)\n\nmatrix = [[1,2,3],[4,5,6],[7,8,9]]\nflat   = [n for row in matrix for n in row]\nprint("Flat:  ", flat)',
  },
  {
    name: "Exceptions",
    code: 'def safe_div(a, b):\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return "Cannot divide by zero"\n\nprint(safe_div(10, 3))\nprint(safe_div(1, 0))\nprint(safe_div(0, 5))',
  },
];

interface RunResult {
  stdout: string;
  stderr: string;
  returncode: number;
  ms?: number;
}

export default function PlaygroundPage() {
  const [code, setCode] = useState("");
  const [result, setResult] = useState<RunResult | null>(null);
  const [running, setRunning] = useState(false);
  const [toast, setToast] = useState<string | null>(null);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem("pyscroll-code");
    requestAnimationFrame(() => {
      if (saved) setCode(saved);
      setLoaded(true);
    });
  }, []);

  const run = useCallback(async () => {
    if (!code.trim() || running) return;
    setRunning(true);
    setResult(null);
    const t0 = performance.now();
    try {
      const res = await fetch(`${API_URL}/api/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });
      const data = (await res.json()) as RunResult;
      setResult({ ...data, stderr: formatStderr(data) });
      localStorage.setItem("pyscroll-code", code);
      if (data.returncode === 0) {
        setUserMeta((m) => ({ playground_runs: m.playground_runs + 1 })).catch(() => {});
        checkAchievements()
          .then((fresh) => {
            if (fresh.length > 0) setToast(fresh[0]);
          })
          .catch(() => {});
      }
    } catch {
      setResult({
        stdout: "",
        stderr: "Could not reach the backend. Is it running on port 8000?",
        returncode: -1,
      });
    } finally {
      setRunning(false);
      const ms = Math.round(performance.now() - t0);
      setResult((prev) => (prev ? { ...prev, ms } : prev));
    }
  }, [code, running]);

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
        e.preventDefault();
        run();
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [run]);

  function formatStderr(data: RunResult): string {
    if (data.returncode === 0) return "";
    const stamp = data.returncode === -1 ? "timed out" : `exit code ${data.returncode}`;
    return data.stderr.includes("[exit code") ? data.stderr : `${data.stderr.trim()}\n\n[${stamp}]`;
  }

  return (
    <main className="mx-auto flex h-full max-w-3xl flex-col bg-bg">
      <div className="min-h-0 flex-1 overflow-y-auto">
        {/* Top bar — examples + run */}
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="sticky top-0 z-20 flex items-center gap-2 border-b border-line/40 bg-bg/90 px-3 py-2 backdrop-blur-md"
        >
          <div className="no-scrollbar flex min-w-0 flex-1 gap-1.5 overflow-x-auto">
            {EXAMPLES.map((ex) => (
              <button
                key={ex.name}
                onClick={() => setCode(ex.code)}
                className="shrink-0 rounded-lg border border-line/40 bg-bgsoft/50 px-2.5 py-1 font-mono text-[11px] text-muted/70 transition-all hover:border-accent/40 hover:text-fg hover:bg-accentsoft/30"
              >
                {ex.name}
              </button>
            ))}
            <button
              onClick={() => setCode("")}
              className="shrink-0 rounded-lg border border-red-500/25 bg-red-500/10 px-2.5 py-1 font-mono text-[11px] text-red-400/80 transition-all hover:bg-red-500/20"
            >
              clear
            </button>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            <span className="hidden text-[10px] text-muted/40 sm:inline">
              <kbd className="rounded border border-line/50 bg-bgsoft/60 px-1.5 py-0.5 font-mono text-[9px]">
                {typeof navigator !== "undefined" && navigator.platform?.includes("Mac") ? "⌘" : "Ctrl"}
              </kbd>
              <span className="mx-0.5">+</span>
              <kbd className="rounded border border-line/50 bg-bgsoft/60 px-1.5 py-0.5 font-mono text-[9px]">↵</kbd>
            </span>
            <motion.button
              onClick={run}
              disabled={!code.trim() || running}
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.97 }}
              className="flex items-center gap-1.5 rounded-lg bg-accent px-3.5 py-1.5 text-[13px] font-medium text-white transition-all disabled:opacity-30 disabled:cursor-not-allowed hover:opacity-90"
            >
              <PlayIcon className="h-3.5 w-3.5" />
              {running ? "Running…" : "Run"}
            </motion.button>
          </div>
        </motion.div>

        {/* Editor */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.05, duration: 0.35 }}
          className="p-3"
        >
          {loaded && (
            <CodeEditor
              value={code}
              onChange={setCode}
              placeholder="# write some python…"
              className="min-h-[20rem] max-h-[50vh]"
            />
          )}
        </motion.div>

        {/* Output */}
        <AnimatePresence>
          {result && (
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              transition={{ duration: 0.3 }}
              className="mx-3 mb-4 overflow-hidden rounded-2xl border border-line/40"
            >
              {/* Terminal header */}
              <div className="flex items-center justify-between border-b border-line/40 bg-[#0a150f] px-4 py-2">
                <div className="flex items-center gap-2">
                  <div className="flex gap-1.5">
                    <span className="h-2.5 w-2.5 rounded-full bg-red-500/70" />
                    <span className="h-2.5 w-2.5 rounded-full bg-yellow-500/70" />
                    <span className="h-2.5 w-2.5 rounded-full bg-green-500/70" />
                  </div>
                  <span className="ml-2 font-mono text-[10px] uppercase tracking-wider text-muted/50">
                    output
                  </span>
                </div>
                <div className="flex items-center gap-3 font-mono text-[10px] text-muted/50">
                  {result.ms != null && <span>{(result.ms / 1000).toFixed(3)}s</span>}
                  <span
                    className={`rounded-full px-2 py-0.5 text-[9px] font-medium ${
                      result.returncode === 0
                        ? "bg-emerald-500/15 text-emerald-400"
                        : "bg-red-500/15 text-red-400"
                    }`}
                  >
                    {result.returncode === 0 ? "OK" : result.returncode === -1 ? "TIMEOUT" : `EXIT ${result.returncode}`}
                  </span>
                </div>
              </div>

              {/* Terminal body */}
              <div className="max-h-64 overflow-y-auto bg-[#060d0a] p-4">
                <pre className="whitespace-pre-wrap break-words font-mono text-[13px] leading-[1.5rem] text-emerald-200/80">
                  {result.stdout && <span>{result.stdout}</span>}
                  {result.stderr && (
                    <span className="text-red-400">{result.stderr}</span>
                  )}
                  {!result.stdout && !result.stderr && (
                    <span className="text-muted/40 italic">(no output)</span>
                  )}
                </pre>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <AchievementToast unlockId={toast} onDone={() => setToast(null)} />
    </main>
  );
}
