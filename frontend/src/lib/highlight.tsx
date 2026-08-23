import React, { useMemo } from "react";

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

export function highlightRow(row: string) {
  const out: React.ReactNode[] = [];
  let last = 0;
  let m: RegExpExecArray | null;
  TOKEN_RE.lastIndex = 0;
  while ((m = TOKEN_RE.exec(row)) !== null) {
    if (m.index > last) out.push(row.slice(last, m.index));
    const kind = Object.keys(m.groups ?? {}).find((k) => m!.groups![k] !== undefined);
    out.push(
      <span key={m.index} className={COLORS[kind ?? "rest"]}>
        {m[0]}
      </span>,
    );
    last = m.index + m[0].length;
  }
  if (last < row.length) out.push(row.slice(last));
  return <>{out}</>;
}

export function PythonCode({ code }: { code: string }) {
  const rows = useMemo(() => code.trimEnd().split("\n"), [code]);
  return (
    <pre className="font-mono text-[0.85rem] leading-6 whitespace-pre overflow-x-auto">
      {rows.map((row, i) => (
        <React.Fragment key={i}>
          {highlightRow(row)}
          {"\n"}
        </React.Fragment>
      ))}
    </pre>
  );
}