"use client";

import React, { useRef, useCallback, useMemo, useEffect } from "react";

const TOKEN_SOURCE =
  "(?<comment>#[^\\n]*)|(?<string>\"\"\"[\\s\\S]*?\"\"\"|'''[\\s\\S]*?'''|\"(?:\\\\.|[^\"\\\\\\n])*\"|'(?:\\\\.|[^'\\\\\\n])*')|(?<decorator>@[a-zA-Z_]\\w*)|(?<number>\\b\\d+(?:\\.\\d+)?\\b)|(?<const>\\b(?:True|False|None)\\b)|(?<keyword>\\b(?:def|class|return|if|elif|else|for|while|in|not|and|or|is|import|from|as|with|try|except|finally|raise|yield|lambda|pass|break|continue|global|nonlocal|del|assert|async|await|match|case)\\b)|(?<builtin>\\b(?:print|len|range|enumerate|zip|sum|abs|min|max|sorted|list|dict|set|tuple|str|int|float|bool|type|isinstance|input|open|map|filter|reversed|any|all|repr|round|super|self)\\b)|(?<call>\\b[A-Za-z_]\\w*(?=\\())|(?<rest>\\S+|\\s+)";

const TOKEN_RE = new RegExp(TOKEN_SOURCE, "g");

const COLORS: Record<string, string> = {
  comment: "text-muted italic",
  string: "text-[var(--syn-string)]",
  decorator: "text-[var(--syn-decorator)]",
  number: "text-[var(--syn-number)]",
  const: "text-[var(--syn-number)] italic",
  keyword: "text-accent",
  builtin: "text-[var(--syn-builtin)]",
  call: "text-[var(--syn-call)]",
  rest: "text-fg",
};

function highlightTokens(row: string): React.ReactNode[] {
  const out: React.ReactNode[] = [];
  let last = 0;
  let m: RegExpExecArray | null;
  TOKEN_RE.lastIndex = 0;
  while ((m = TOKEN_RE.exec(row)) !== null) {
    if (m.index > last) out.push(<span key={`t-${last}`}>{row.slice(last, m.index)}</span>);
    const kind = Object.keys(m.groups ?? {}).find((k) => m!.groups![k] !== undefined);
    out.push(
      <span key={`t-${m.index}`} className={COLORS[kind ?? "rest"]}>
        {m[0]}
      </span>,
    );
    last = m.index + m[0].length;
  }
  if (last < row.length) out.push(<span key={`t-${last}`}>{row.slice(last)}</span>);
  return out;
}

interface CodeEditorProps {
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
  className?: string;
}

export default function CodeEditor({ value, onChange, placeholder = "# write some python…", className = "" }: CodeEditorProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const highlightRef = useRef<HTMLDivElement>(null);
  const lineNumRef = useRef<HTMLDivElement>(null);
  const syncRef = useRef<HTMLDivElement>(null);

  const lines = useMemo(() => value.split("\n"), [value]);
  const lineCount = lines.length;

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
      const ta = textareaRef.current;
      if (!ta) return;

      if (e.key === "Tab") {
        e.preventDefault();
        const start = ta.selectionStart;
        const end = ta.selectionEnd;
        const before = value.slice(0, start);
        const after = value.slice(end);
        const next = before + "    " + after;
        onChange(next);
        requestAnimationFrame(() => {
          ta.selectionStart = ta.selectionEnd = start + 4;
        });
      }

      if (e.key === "Enter") {
        e.preventDefault();
        const start = ta.selectionStart;
        const before = value.slice(0, start);
        const after = value.slice(ta.selectionEnd);
        const currentLine = before.split("\n").pop() ?? "";
        const indent = currentLine.match(/^\s*/)?.[0] ?? "";
        const trimmed = currentLine.trimEnd();
        let extra = "";
        if (trimmed.endsWith(":") || trimmed.endsWith("(") || trimmed.endsWith("[") || trimmed.endsWith("{")) {
          extra = "    ";
        }
        const insertion = "\n" + indent + extra;
        const next = before + insertion + after;
        onChange(next);
        requestAnimationFrame(() => {
          ta.selectionStart = ta.selectionEnd = start + insertion.length;
        });
      }
    },
    [value, onChange],
  );

  const handleScroll = useCallback(() => {
    const ta = textareaRef.current;
    if (!ta) return;
    const { scrollTop, scrollLeft } = ta;
    if (highlightRef.current) {
      highlightRef.current.style.transform = `translate(${-scrollLeft}px, ${-scrollTop}px)`;
    }
    if (lineNumRef.current) {
      lineNumRef.current.style.transform = `translate(0, ${-scrollTop}px)`;
    }
  }, []);

  useEffect(() => {
    const ta = textareaRef.current;
    if (!ta) return;
    ta.addEventListener("scroll", handleScroll, { passive: true });
    return () => ta.removeEventListener("scroll", handleScroll);
  }, [handleScroll]);

  return (
    <div className={`relative flex overflow-hidden rounded-2xl border border-line/50 bg-[#080f0c] transition-all focus-within:border-accent/40 ${className}`}>
      {/* Line numbers */}
      <div
        ref={lineNumRef}
        className="pointer-events-none sticky left-0 z-10 flex shrink-0 flex-col border-r border-line/30 bg-[#060d0a] px-2 py-4 text-right select-none"
        style={{ minWidth: "2.5rem" }}
      >
        {Array.from({ length: lineCount }, (_, i) => (
          <span key={i} className="font-mono text-[13px] leading-[1.5rem] text-muted/30">
            {i + 1}
          </span>
        ))}
      </div>

      {/* Editor area */}
      <div className="relative min-w-0 flex-1">
        {/* Highlighted display layer */}
        <div
          ref={(el) => {
            highlightRef.current = el;
            syncRef.current = el;
          }}
          className="pointer-events-none absolute inset-0 z-0 overflow-hidden p-4"
          aria-hidden="true"
        >
          <pre className="font-mono text-[13px] leading-[1.5rem] whitespace-pre">
            {lines.map((row, i) => (
              <React.Fragment key={i}>
                {highlightTokens(row)}
                {"\n"}
              </React.Fragment>
            ))}
          </pre>
        </div>

        {/* Textarea (actual input) */}
        <textarea
          ref={textareaRef}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          spellCheck={false}
          autoComplete="off"
          autoCapitalize="off"
          autoCorrect="off"
          data-gramm="false"
          placeholder={placeholder}
          className="relative z-10 h-full min-h-[24rem] w-full resize-none bg-transparent p-4 font-mono text-[13px] leading-[1.5rem] text-transparent caret-accent outline-none placeholder:text-muted/40"
          style={{ caretColor: "var(--accent)" }}
        />
      </div>
    </div>
  );
}
