"use client";

import { useEffect, useRef, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import type { Comment } from "@/lib/db";
import type { Tip } from "@/lib/types";
import {
     addComment,
     getCommentsByTip,
     setUserMeta,
} from "@/lib/db";
import { checkAchievements } from "@/lib/achievements";
import { relTime } from "@/lib/time";
import { CommentIcon, PythonLogo } from "./icons";

interface Props {
     tip: Tip | null;
     onClose: () => void;
     onFreshAchievement: (name: string) => void;
     onCountChange: (tipId: number, count: number) => void;
}

export default function CommentSheet({
     tip,
     onClose,
     onFreshAchievement,
     onCountChange,
}: Props) {
     const [comments, setComments] = useState<Comment[]>(
          [],
     );
     const [text, setText] = useState("");
     const [busy, setBusy] = useState(false);
     const listRef = useRef<HTMLDivElement>(null);

     useEffect(() => {
          if (!tip) return;
          getCommentsByTip(tip.id)
               .then(setComments)
               .catch(() => {});
     }, [tip]);

     useEffect(() => {
          listRef.current?.scrollTo({
               top: listRef.current.scrollHeight,
               behavior: "smooth",
          });
     }, [comments.length]);

     async function submit() {
          const content = text.trim();
          if (!content || !tip || busy) return;
          setBusy(true);
          try {
               const added = await addComment(
                    tip.id,
                    content,
               );
               setComments((c) => [...c, added]);
               onCountChange(tip.id, comments.length + 1);
               setText("");
               await setUserMeta({
                    last_action_ts: Date.now(),
               }).catch(() => {});
               const fresh = await checkAchievements();
               if (fresh.length > 0)
                    onFreshAchievement(fresh[0]);
          } finally {
               setBusy(false);
          }
     }

     return (
          <AnimatePresence>
               {tip && (
                    <>
                         <motion.div
                              className="fixed inset-0 z-40 bg-black/60 backdrop-blur-sm"
                              initial={{ opacity: 0 }}
                              animate={{ opacity: 1 }}
                              exit={{ opacity: 0 }}
                              onClick={onClose}
                         />
                         <motion.div
                              className="fixed inset-x-0 bottom-0 z-50 flex h-[72dvh] flex-col rounded-t-2xl border-t border-line/50 bg-bgsoft/95 backdrop-blur-xl"
                              initial={{ y: "100%" }}
                              animate={{ y: 0 }}
                              exit={{ y: "100%" }}
                              transition={{
                                   type: "spring",
                                   stiffness: 350,
                                   damping: 30,
                              }}
                         >
                              <motion.div
                                   initial={{
                                        opacity: 0,
                                        scale: 0.9,
                                   }}
                                   animate={{
                                        opacity: 1,
                                        scale: 1,
                                   }}
                                   transition={{
                                        delay: 0.1,
                                   }}
                                   className="mx-auto mt-3 h-1 w-12 rounded-full bg-line/50"
                              />
                              <div className="flex items-center justify-between px-5 py-3 border-b border-line/50">
                                   <div className="flex items-center gap-2 text-sm font-medium text-fg">
                                        <CommentIcon className="text-accent" />
                                        <span>
                                             Comments{" "}
                                             <span className="font-mono text-muted/60">
                                                  (
                                                  {
                                                       comments.length
                                                  }
                                                  )
                                             </span>
                                        </span>
                                   </div>
                                   <motion.button
                                        onClick={onClose}
                                        whileTap={{
                                             scale: 0.9,
                                        }}
                                        className="flex h-9 w-9 items-center justify-center rounded-full text-muted/70 transition-colors hover:bg-line/30 hover:text-fg"
                                        aria-label="Close comments"
                                   >
                                        ✕
                                   </motion.button>
                              </div>

                              <div
                                   ref={listRef}
                                   className="flex-1 overflow-y-auto px-5 pb-4 space-y-3"
                              >
                                   <p className="px-1 pb-1 text-[11px] uppercase tracking-widest text-muted/60">
                                        {tip.title}
                                   </p>
                                   {comments.length ===
                                        0 && (
                                        <motion.p
                                             initial={{
                                                  opacity: 0,
                                                  y: 10,
                                             }}
                                             animate={{
                                                  opacity: 1,
                                                  y: 0,
                                             }}
                                             transition={{
                                                  delay: 0.2,
                                             }}
                                             className="pt-16 text-center text-sm text-muted/60"
                                        >
                                             No comments
                                             yet. Be the
                                             first to say
                                             something
                                             smart.
                                        </motion.p>
                                   )}
                                   {comments.map((c, i) => (
                                        <motion.div
                                             key={c.id}
                                             initial={{
                                                  opacity: 0,
                                                  x: -20,
                                             }}
                                             animate={{
                                                  opacity: 1,
                                                  x: 0,
                                             }}
                                             transition={{
                                                  delay:
                                                       0.05 +
                                                       i *
                                                            0.03,
                                                  duration: 0.2,
                                             }}
                                             className="flex gap-3"
                                        >
                                             <div className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-accentsoft text-accent">
                                                  <PythonLogo className="h-5 w-5" icon />
                                             </div>
                                             <div className="min-w-0 flex-1 rounded-xl border border-line/50 bg-bg/50 px-3.5 py-2.5">
                                                  <div className="flex items-baseline justify-between gap-2">
                                                       <span className="text-xs font-medium text-fg">
                                                            You
                                                       </span>
                                                       <span className="font-mono text-[10px] text-muted/60">
                                                            {relTime(
                                                                 c.timestamp,
                                                            )}
                                                       </span>
                                                  </div>
                                                  <p className="mt-1 text-sm leading-relaxed break-words text-fg/90">
                                                       {
                                                            c.comment_text
                                                       }
                                                  </p>
                                             </div>
                                        </motion.div>
                                   ))}
                              </div>

                              <div className="border-t border-line/50 bg-bgsoft/50 p-3 pb-[max(0.75rem,env(safe-area-inset-bottom))]">
                                   <div className="flex items-center gap-2 rounded-full border border-line/50 bg-bg/50 px-4 py-2 transition-colors focus-within:border-accent/40">
                                        <input
                                             value={text}
                                             onChange={(
                                                  e,
                                             ) =>
                                                  setText(
                                                       e
                                                            .target
                                                            .value,
                                                  )
                                             }
                                             onKeyDown={(
                                                  e,
                                             ) => {
                                                  if (
                                                       e.key ===
                                                            "Enter" &&
                                                       !e.shiftKey
                                                  ) {
                                                       e.preventDefault();
                                                       submit();
                                                  }
                                             }}
                                             placeholder="Add a comment…"
                                             className="flex-1 bg-transparent text-sm outline-none placeholder:text-muted/50"
                                             maxLength={280}
                                             autoComplete="off"
                                        />
                                        <motion.button
                                             onClick={
                                                  submit
                                             }
                                             disabled={
                                                  !text.trim() ||
                                                  busy
                                             }
                                             whileTap={{
                                                  scale: 0.95,
                                             }}
                                             className="rounded-full bg-accent px-4 py-1.5 text-xs font-medium text-white transition-all disabled:opacity-30 disabled:cursor-not-allowed hover:opacity-90"
                                        >
                                             Post
                                        </motion.button>
                                   </div>
                              </div>
                         </motion.div>
                    </>
               )}
          </AnimatePresence>
     );
}
