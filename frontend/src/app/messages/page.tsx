"use client";

import {
     useEffect,
     useRef,
     useState,
     useCallback,
     useMemo,
} from "react";
import {
     motion,
     AnimatePresence,
     useReducedMotion,
} from "framer-motion";
import type { ChatMessage } from "@/lib/db";
import {
     addChatMessage,
     clearChatHistory,
     getChatHistory,
     getUserMeta,
     setUserMeta,
} from "@/lib/db";
import { API_URL } from "@/lib/api";
import { checkAchievements } from "@/lib/achievements";
import AchievementToast from "@/components/AchievementToast";
import {
     PythonLogo,
     SendIcon,
     TrashIcon,
} from "@/components/icons";
import { highlightRow } from "@/lib/highlight";
import React from "react";

interface Msg extends ChatMessage {
     ck: number;
}

/* ── Code block with syntax highlight + copy ── */

function CodeBlock({ code }: { code: string }) {
     const [copied, setCopied] = useState(false);
     const lines = useMemo(
          () => code.trimEnd().split("\n"),
          [code],
     );

     function copy() {
          navigator.clipboard
               .writeText(code.trimEnd())
               .then(() => {
                    setCopied(true);
                    setTimeout(
                         () => setCopied(false),
                         1500,
                    );
               });
     }

     return (
          <div className="group/code relative mt-2 overflow-hidden rounded-xl border border-white/6 bg-[#080e0b] shadow-lg shadow-black/20">
               {/* Header bar */}
               <div className="flex items-center justify-between border-b border-white/6 bg-white/2 px-3 py-2">
                    <div className="flex items-center gap-2">
                         <div className="flex gap-1">
                              <span className="h-2 w-2 rounded-full bg-red-500/60" />
                              <span className="h-2 w-2 rounded-full bg-yellow-500/60" />
                              <span className="h-2 w-2 rounded-full bg-green-500/60" />
                         </div>
                         <span className="font-mono text-[10px] tracking-wider text-white/30">
                              python
                         </span>
                    </div>
                    <motion.button
                         onClick={copy}
                         whileTap={{ scale: 0.92 }}
                         className="rounded-md px-2.5 py-1 font-mono text-[10px] text-white/30 opacity-0 transition-all hover:bg-white/6 hover:text-white/60 group-hover/code:opacity-100"
                    >
                         {copied ? (
                              <span className="text-accent">
                                   copied!
                              </span>
                         ) : (
                              <span className="flex items-center gap-1">
                                   <svg
                                        className="h-3 w-3"
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        stroke="currentColor"
                                        strokeWidth={2}
                                   >
                                        <rect
                                             x="9"
                                             y="9"
                                             width="13"
                                             height="13"
                                             rx="2"
                                        />
                                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
                                   </svg>
                                   copy
                              </span>
                         )}
                    </motion.button>
               </div>
               {/* Code body */}
               <div className="overflow-x-auto">
                    <table className="border-collapse">
                         <tbody>
                              {lines.map((row, i) => (
                                   <tr
                                        key={i}
                                        className="hover:bg-white/2"
                                   >
                                        <td className="select-none border-r border-white/4 py-0 pr-3 pl-3 text-right">
                                             <span className="inline-block font-mono text-[11px] leading-[1.45rem] text-white/15">
                                                  {i + 1}
                                             </span>
                                        </td>
                                        <td className="py-0 pr-4 pl-3">
                                             <pre className="font-mono text-[12px] leading-[1.45rem]">
                                                  {highlightRow(
                                                       row,
                                                  )}
                                                  {"\n"}
                                             </pre>
                                        </td>
                                   </tr>
                              ))}
                         </tbody>
                    </table>
               </div>
          </div>
     );
}

/* ── Message content renderer ── */

function renderContent(content: string) {
     const blocks = content.split(/```/g);
     return blocks.map((block, i) => {
          if (i % 2 === 1) {
               const langLine = block.split("\n")[0];
               const code = block
                    .slice(langLine.length)
                    .replace(/^\n/, "");
               return <CodeBlock key={i} code={code} />;
          }
          return (
               <span
                    key={i}
                    className="whitespace-pre-wrap wrap-break-word"
               >
                    {block}
               </span>
          );
     });
}

/* ── Helpers ── */

function formatTime(ts: number) {
     const d = new Date(ts);
     const h = d.getHours();
     const m = d.getMinutes().toString().padStart(2, "0");
     const ampm = h >= 12 ? "PM" : "AM";
     return `${h % 12 || 12}:${m} ${ampm}`;
}

function formatRelative(ts: number) {
     const diff = Date.now() - ts;
     if (diff < 60_000) return "just now";
     if (diff < 3600_000)
          return `${Math.floor(diff / 60_000)}m ago`;
     if (diff < 86400_000)
          return `${Math.floor(diff / 3600_000)}h ago`;
     return formatTime(ts);
}

/* ── Typing indicator ── */

function TypingIndicator() {
     return (
          <motion.div
               initial={{ opacity: 0, y: 6, scale: 0.95 }}
               animate={{ opacity: 1, y: 0, scale: 1 }}
               exit={{ opacity: 0, y: -4, scale: 0.95 }}
               transition={{
                    type: "spring",
                    stiffness: 400,
                    damping: 28,
               }}
               className="flex gap-2.5"
          >
               <div className="flex h-10 shrink-0 items-center justify-center rounded-full bg-linear-to-br from-accent/25 to-accent/5 ring-1 ring-accent/20">
                    <PythonLogo className="h-10" icon />
               </div>
               <div className="flex items-center gap-1.25 rounded-2xl rounded-bl-md border border-white/6 bg-white/4 px-4 py-3.5 backdrop-blur-sm">
                    {[0, 1, 2].map((i) => (
                         <motion.span
                              key={i}
                              animate={{
                                   y: [0, -4, 0],
                                   opacity: [0.3, 1, 0.3],
                              }}
                              transition={{
                                   duration: 0.9,
                                   repeat: Infinity,
                                   delay: i * 0.18,
                                   ease: "easeInOut",
                              }}
                              className="h-1.25 w-1.25 rounded-full bg-accent"
                         />
                    ))}
               </div>
          </motion.div>
     );
}

/* ── Empty state ── */

function EmptyState({
     onPick,
}: {
     onPick: (q: string) => void;
}) {
     const prompts = useMemo(
          () => [
               { q: "What is a decorator?", icon: "@" },
               { q: "List vs tuple?", icon: "[]" },
               { q: "Async/await basics", icon: "~" },
               { q: "Fix my bug", icon: "?" },
          ],
          [],
     );

     return (
          <motion.div
               initial={{ opacity: 0 }}
               animate={{ opacity: 1 }}
               exit={{ opacity: 0, scale: 0.98 }}
               transition={{ duration: 0.4 }}
               className="flex flex-col items-center px-6 pt-20 text-center"
          >
               {/* Floating orb */}
               <div className="relative mb-6">
                    <motion.div
                         animate={{
                              y: [0, -6, 0],
                              rotate: [0, 3, -3, 0],
                         }}
                         transition={{
                              duration: 5,
                              repeat: Infinity,
                              ease: "easeInOut",
                         }}
                         className="flex h-16 w-16 items-center justify-center rounded-[1.25rem] bg-linear-to-br from-accent/20 via-accent/10 to-transparent ring-1 ring-accent/15"
                    >
                         <PythonLogo className="h-20" />
                    </motion.div>
               </div>

               <h2 className="text-[15px] font-semibold text-fg">
                    Python Tutor
               </h2>
               <p className="mt-1.5 max-w-60 text-[12px] leading-normal text-muted/50">
                    Ask anything about Python.
               </p>

               <div className="mt-8 grid w-full max-w-[320px] grid-cols-2 gap-2">
                    {prompts.map((p, i) => (
                         <motion.button
                              key={p.q}
                              onClick={() => onPick(p.q)}
                              initial={{
                                   opacity: 0,
                                   y: 12,
                              }}
                              animate={{ opacity: 1, y: 0 }}
                              transition={{
                                   delay: 0.15 + i * 0.06,
                                   type: "spring",
                                   stiffness: 300,
                                   damping: 24,
                              }}
                              whileTap={{ scale: 0.97 }}
                              className="flex items-center gap-2.5 rounded-xl border border-white/6 bg-white/3 px-3.5 py-3 text-left hover:cursor-pointer hover:bg-white/1"
                         >
                              <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-accent/10 font-mono text-[11px] text-accent/70">
                                   {p.icon}
                              </span>
                              <span className="text-[12px] leading-tight text-muted/60">
                                   {p.q}
                              </span>
                         </motion.button>
                    ))}
               </div>
          </motion.div>
     );
}

/* ── Main page ── */

export default function MessagesPage() {
     const [messages, setMessages] = useState<Msg[]>([]);
     const [input, setInput] = useState("");
     const [streaming, setStreaming] = useState(false);
     const [, setName] = useState("Pythonista");
     const [toast, setToast] = useState<string | null>(
          null,
     );
     const [confirmingClear, setConfirmingClear] =
          useState(false);
     const scrollRef = useRef<HTMLDivElement>(null);
     const textareaRef = useRef<HTMLTextAreaElement>(null);
     const keyCounter = useRef(0);
     const streamGenRef = useRef(0);
     const sendingRef = useRef(false);
     const bottomRef = useRef<HTMLDivElement>(null);
     const prefersReduced = useReducedMotion();
     const nextKey = () => ++keyCounter.current;

     /* Load history */
     useEffect(() => {
          getChatHistory()
               .then((h) =>
                    setMessages(
                         h.map((m) => ({
                              ...m,
                              ck: nextKey(),
                         })),
                    ),
               )
               .catch(() => {});
          getUserMeta()
               .then((m) => setName(m.name))
               .catch(() => {});
     }, []);

     /* Auto-scroll */
     useEffect(() => {
          bottomRef.current?.scrollIntoView({
               behavior: prefersReduced ? "auto" : "smooth",
          });
     }, [messages, streaming, prefersReduced]);

     /* Clear chat */
     async function clearChat() {
          if (!confirmingClear) {
               setConfirmingClear(true);
               setTimeout(
                    () => setConfirmingClear(false),
                    2500,
               );
               return;
          }
          setConfirmingClear(false);
          streamGenRef.current += 1;
          setMessages([]);
          await clearChatHistory().catch(() => {});
     }

     /* Auto-resize textarea */
     function autoResize() {
          const ta = textareaRef.current;
          if (!ta) return;
          ta.style.height = "auto";
          ta.style.height =
               Math.min(ta.scrollHeight, 140) + "px";
     }
     useEffect(() => autoResize(), [input]);

     /* Send message */
     const send = useCallback(async () => {
          const text = input.trim();
          if (!text || streaming || sendingRef.current)
               return;
          setInput("");
          if (textareaRef.current)
               textareaRef.current.style.height = "auto";
          setStreaming(true);
          sendingRef.current = true;
          const gen = streamGenRef.current;
          const liveCk = nextKey();

          let savedUser: ChatMessage | null = null;
          try {
               savedUser = await addChatMessage(
                    "user",
                    text,
               );
               await setUserMeta({
                    last_action_ts: Date.now(),
               }).catch(() => {});
          } catch {}
          const userCk = nextKey();
          const userMsg: Msg = {
               role: "user",
               content: text,
               timestamp: Date.now(),
               ck: userCk,
          };
          if (savedUser) userMsg.id = savedUser.id;
          setMessages((prev) => [...prev, userMsg]);

          let full = "";
          try {
               const res = await fetch(
                    `${API_URL}/api/chat`,
                    {
                         method: "POST",
                         headers: {
                              "Content-Type":
                                   "application/json",
                         },
                         body: JSON.stringify({
                              message: text,
                              history: messages
                                   .slice(-12)
                                   .map((m) => ({
                                        role: m.role,
                                        content: m.content,
                                   })),
                         }),
                    },
               );
               if (res.body) {
                    const reader = res.body.getReader();
                    const decoder = new TextDecoder();
                    let buffer = "";
                    while (true) {
                         const { value, done } =
                              await reader.read();
                         if (done) break;
                         if (gen !== streamGenRef.current)
                              break;
                         buffer += decoder.decode(value, {
                              stream: true,
                         });
                         const events =
                              buffer.split("\n\n");
                         buffer = events.pop() ?? "";
                         for (const ev of events) {
                              const line = ev.trim();
                              if (!line.startsWith("data:"))
                                   continue;
                              const payload = line
                                   .slice(5)
                                   .trim();
                              if (!payload) continue;
                              try {
                                   const data =
                                        JSON.parse(payload);
                                   if (data.done) break;
                                   if (
                                        typeof data.content ===
                                        "string"
                                   ) {
                                        full +=
                                             data.content;
                                        setMessages(
                                             (prev) => {
                                                  const base =
                                                       prev.filter(
                                                            (
                                                                 m,
                                                            ) =>
                                                                 m.ck !==
                                                                 liveCk,
                                                       );
                                                  return [
                                                       ...base,
                                                       {
                                                            role: "assistant",
                                                            content: full,
                                                            timestamp:
                                                                 Date.now(),
                                                            ck: liveCk,
                                                       },
                                                  ];
                                             },
                                        );
                                   }
                              } catch {}
                         }
                    }
               } else {
                    full =
                         "Could not reach the tutor. Is the backend running on port 8000?";
               }
          } catch {
               full =
                    "Could not reach the tutor. Is the backend running on port 8000?";
          }

          if (gen !== streamGenRef.current) {
               setStreaming(false);
               sendingRef.current = false;
               return;
          }
          const finalCk = nextKey();
          setMessages((prev) => {
               const base = prev.filter(
                    (m) => m.ck !== liveCk,
               );
               return [
                    ...base,
                    {
                         role: "assistant",
                         content: full,
                         timestamp: Date.now(),
                         ck: finalCk,
                    },
               ];
          });
          setStreaming(false);
          sendingRef.current = false;

          try {
               const saved = await addChatMessage(
                    "assistant",
                    full,
               );
               setMessages((prev) =>
                    prev.map((m) =>
                         m.ck === finalCk && !m.id && saved
                              ? { ...m, id: saved.id }
                              : m,
                    ),
               );
          } catch {}

          checkAchievements()
               .then((f) => {
                    if (f.length > 0) setToast(f[0]);
               })
               .catch(() => {});
     }, [input, streaming, messages]);

     /* Key binding */
     useEffect(() => {
          const onKey = (e: KeyboardEvent) => {
               if (
                    (e.metaKey || e.ctrlKey) &&
                    e.key === "Enter"
               ) {
                    e.preventDefault();
                    send();
               }
          };
          window.addEventListener("keydown", onKey);
          return () =>
               window.removeEventListener("keydown", onKey);
     }, [send]);

     /* Message grouping logic */
     const groupedMessages = useMemo(() => {
          return messages.map((m, idx) => {
               const prev = messages[idx - 1];
               const next = messages[idx + 1];
               const isUser = m.role === "user";
               const sameAsPrev = prev?.role === m.role;
               const sameAsNext = next?.role === m.role;
               const gapTime = prev
                    ? m.timestamp - prev.timestamp > 120_000
                    : true;
               const showTime = !sameAsPrev || gapTime;
               const isFirstOfGroup =
                    !sameAsPrev || gapTime;
               const isLastOfGroup =
                    !sameAsNext ||
                    (next &&
                         next.timestamp - m.timestamp >
                              120_000);
               return {
                    ...m,
                    isUser,
                    showTime,
                    isFirstOfGroup,
                    isLastOfGroup,
                    idx,
               };
          });
     }, [messages]);

     const hasMessages = messages.length > 0;

     return (
          <main className="mx-auto flex h-full max-w-2xl flex-col bg-bg">
               {/* ── Background gradient ── */}
               <div className="pointer-events-none fixed inset-0 -z-10">
                    <div className="absolute left-1/2 top-0 h-125 w-150 -translate-x-1/2 rounded-full bg-accent/3 blur-[120px]" />
               </div>

               {/* ── Header ── */}
               <motion.header
                    initial={{ opacity: 0, y: -12 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{
                         type: "spring",
                         stiffness: 300,
                         damping: 30,
                    }}
                    className="relative z-20 flex shrink-0 items-center gap-3 border-b border-white/6 bg-bgro/70 px-4 py-3 backdrop-blur-2xl"
               >
                    {/* Avatar with online dot */}
                    <div className="relative">
                         <div className="flex h-11 w-11 items-center justify-center rounded-full bg-linear-to-br from-accent/20 to-accent/4 ring-1 ring-accent/20">
                              <PythonLogo className="h-15" />
                         </div>
                         <span className="absolute -bottom-0.5 -right-0.5 h-3.5 w-3.5 rounded-full border-2 border-bg bg-emerald-400 shadow-sm shadow-emerald-500/30" />
                    </div>

                    <div className="flex-1 min-w-0">
                         <h1 className="text-[14px] font-semibold tracking-tight text-fg">
                              Python Tutor
                         </h1>
                         <p className="text-[11px] text-muted/50">
                              online
                         </p>
                    </div>

                    <motion.button
                         onClick={clearChat}
                         whileTap={{ scale: 0.92 }}
                         aria-label="Clear chat"
                         className={`flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-[11px] font-medium transition-all ${
                              confirmingClear
                                   ? "border-red-500/40 bg-red-500/10 text-red-400"
                                   : "border-white/6 text-muted/50 hover:border-white/10 hover:text-fg/70 hover:bg-white/4"
                         }`}
                    >
                         <TrashIcon className="h-3.5 w-3.5" />
                         {confirmingClear
                              ? "Confirm?"
                              : hasMessages
                                ? "Clear"
                                : ""}
                    </motion.button>
               </motion.header>

               {/* ── Messages area ── */}
               <div
                    ref={scrollRef}
                    className="min-h-0 flex-1 overflow-y-auto"
               >
                    <div className="mx-auto max-w-2xl px-4 py-5">
                         <AnimatePresence initial={false}>
                              {!hasMessages &&
                                   !streaming && (
                                        <EmptyState
                                             onPick={(
                                                  q,
                                             ) => {
                                                  setInput(
                                                       q,
                                                  );
                                                  textareaRef.current?.focus();
                                             }}
                                        />
                                   )}
                         </AnimatePresence>

                         {groupedMessages.map((m) => {
                              const bubbleRadius =
                                   m.isFirstOfGroup &&
                                   m.isLastOfGroup
                                        ? "rounded-2xl"
                                        : m.isFirstOfGroup
                                          ? m.isUser
                                               ? "rounded-2xl rounded-br-md"
                                               : "rounded-2xl rounded-bl-md"
                                          : m.isLastOfGroup
                                            ? m.isUser
                                                 ? "rounded-2xl rounded-tr-md"
                                                 : "rounded-2xl rounded-tl-md"
                                            : m.isUser
                                              ? "rounded-2xl rounded-r-md"
                                              : "rounded-2xl rounded-l-md";

                              return (
                                   <motion.div
                                        key={
                                             m.id != null
                                                  ? `id-${m.id}`
                                                  : `ck-${m.ck}`
                                        }
                                        initial={{
                                             opacity: 0,
                                             y: 10,
                                             scale: 0.98,
                                        }}
                                        animate={{
                                             opacity: 1,
                                             y: 0,
                                             scale: 1,
                                        }}
                                        transition={{
                                             type: "spring",
                                             stiffness: 380,
                                             damping: 28,
                                        }}
                                        className={`flex ${m.isUser ? "justify-end" : "justify-start"} ${
                                             m.isFirstOfGroup
                                                  ? "mt-3"
                                                  : "mt-0.5"
                                        }`}
                                   >
                                        {/* Assistant avatar — only first of group */}
                                        {!m.isUser && (
                                             <div
                                                  className={`mr-2.5 flex w-8 shrink-0 ${m.isFirstOfGroup ? "mt-5 opacity-100" : "mt-0 opacity-0"}`}
                                             >
                                                  {m.isFirstOfGroup && (
                                                       <div className="flex h-8 w-8 items-center justify-center rounded-full bg-linear-to-br from-accent/20 to-accent/4 ring-1 ring-accent/15">
                                                            <PythonLogo
                                                                 className="h-4 w-4"
                                                                 icon
                                                            />
                                                       </div>
                                                  )}
                                             </div>
                                        )}

                                        <div
                                             className={`flex flex-col ${m.isUser ? "items-end" : "items-start"} max-w-[78%]`}
                                        >
                                             {/* Timestamp */}
                                             {m.showTime && (
                                                  <motion.span
                                                       initial={{
                                                            opacity: 0,
                                                       }}
                                                       animate={{
                                                            opacity: 1,
                                                       }}
                                                       className={`mb-1 px-1 font-mono text-[10px] text-muted/30 ${m.isUser ? "text-right" : ""}`}
                                                  >
                                                       {formatRelative(
                                                            m.timestamp,
                                                       )}
                                                  </motion.span>
                                             )}

                                             {/* Bubble */}
                                             <div
                                                  className={`relative px-4 py-2.5 text-[13px] leading-[1.6] transition-shadow ${
                                                       bubbleRadius
                                                  } ${
                                                       m.isUser
                                                            ? "bg-gradient-to-br from-accent to-accent/85 text-white shadow-lg shadow-accent/15"
                                                            : "border border-white/[0.06] bg-white/[0.04] text-fg/85 backdrop-blur-sm"
                                                  }`}
                                             >
                                                  {m.isUser ? (
                                                       <span className="whitespace-pre-wrap break-words">
                                                            {
                                                                 m.content
                                                            }
                                                       </span>
                                                  ) : (
                                                       renderContent(
                                                            m.content,
                                                       )
                                                  )}

                                                  {/* Streaming cursor */}
                                                  {m.role ===
                                                       "assistant" &&
                                                       streaming &&
                                                       !m.id && (
                                                            <span className="pulse-soft ml-0.5 inline-block text-accent">
                                                                 ▍
                                                            </span>
                                                       )}
                                             </div>

                                             {/* Read receipt for user */}
                                             {m.isUser &&
                                                  m.isLastOfGroup && (
                                                       <motion.span
                                                            initial={{
                                                                 opacity: 0,
                                                            }}
                                                            animate={{
                                                                 opacity: 1,
                                                            }}
                                                            transition={{
                                                                 delay: 0.3,
                                                            }}
                                                            className="mt-0.5 px-1 text-[10px] text-muted/25"
                                                       >
                                                            sent
                                                       </motion.span>
                                                  )}
                                        </div>
                                   </motion.div>
                              );
                         })}

                         {/* Typing indicator */}
                         <AnimatePresence>
                              {streaming &&
                                   !messages.some(
                                        (m) =>
                                             m.role ===
                                                  "assistant" &&
                                             !m.id,
                                   ) && <TypingIndicator />}
                         </AnimatePresence>

                         <div
                              ref={bottomRef}
                              className="h-1"
                         />
                    </div>
               </div>

               {/* ── Input area ── */}
               <motion.div
                    initial={{ opacity: 0, y: 16 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{
                         type: "spring",
                         stiffness: 300,
                         damping: 28,
                         delay: 0.15,
                    }}
                    className="shrink-0 border-line/40 px-4 py-3 pb-[max(0.75rem,env(safe-area-inset-bottom))]"
               >
                    <div className="flex items-center gap-2 p-2 ">
                         <textarea
                              ref={textareaRef}
                              value={input}
                              onChange={(e) =>
                                   setInput(e.target.value)
                              }
                              onKeyDown={(e) => {
                                   if (
                                        e.key === "Enter" &&
                                        !e.shiftKey
                                   ) {
                                        e.preventDefault();
                                        send();
                                   }
                              }}
                              placeholder="Ask something about Python…"
                              rows={1}
                              className="min-h-10 max-h-35 flex-1 resize-none bg-green-900/10 rounded-2xl p-2 text-[13px] leading-relaxed outline-none placeholder:text-muted/40"
                              autoComplete="off"
                         />
                         <motion.button
                              onClick={send}
                              disabled={
                                   !input.trim() ||
                                   streaming
                              }
                              whileTap={{ scale: 0.92 }}
                              aria-label="Send"
                              className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-full transition-all ${
                                   input.trim() &&
                                   !streaming
                                        ? "bg-accent text-white"
                                        : "bg-white/[0.06] text-muted/40"
                              } disabled:cursor-not-allowed`}
                         >
                              <SendIcon className="h-4 w-4" />
                         </motion.button>
                    </div>
                    <p className="mt-1.5 text-center text-[10px] text-muted/25">
                         <kbd className="rounded border border-line/40 px-1 py-0.5 font-mono text-[9px]">
                              Enter
                         </kbd>{" "}
                         send ·{" "}
                         <kbd className="rounded border border-line/40 px-1 py-0.5 font-mono text-[9px]">
                              Shift+Enter
                         </kbd>{" "}
                         newline
                    </p>
               </motion.div>

               <AchievementToast
                    unlockId={toast}
                    onDone={() => setToast(null)}
               />
          </main>
     );
}
