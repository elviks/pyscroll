"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { fetchTips } from "@/lib/api";
import type { Tip } from "@/lib/types";
import {
     getAchievements,
     getAllComments,
     getFavorites,
     getReposts,
     getUserMeta,
     type Achievement,
     type Comment,
     type UserMeta,
} from "@/lib/db";
import { ACHIEVEMENTS } from "@/lib/achievements";
import { LockKeyhole } from "lucide-react";
import { formatClock, relTime } from "@/lib/time";

type Tab = "favorites" | "reposts" | "comments" | "achievements";

export default function ProfilePage() {
     const [meta, setMeta] = useState<UserMeta | null>(
          null,
     );
     const [tab, setTab] = useState<Tab>("favorites");
     const [tips, setTips] = useState<Tip[]>([]);
     const [favIds, setFavIds] = useState<number[]>([]);
     const [repIds, setRepIds] = useState<number[]>([]);
     const [comments, setComments] = useState<Comment[]>([]);
     const [achievements, setAchievements] = useState<
          Achievement[]
     >([]);
     const [favTimes, setFavTimes] = useState<
          Record<number, number>
     >({});
     const [repTimes, setRepTimes] = useState<
          Record<number, number>
     >({});
     const [loadedEvents, setLoadedEvents] = useState<
          Record<string, number>
     >({});

      const load = useCallback(() => {
           Promise.all([getUserMeta(), getFavorites(), getReposts()])
                .then(([m, favs, reps]) => {
                     setMeta(m);
                     setFavIds(favs.map((f) => f.tip_id));
                     setRepIds(reps.map((r) => r.tip_id));
                     const ft: Record<number, number> = {};
                     for (const f of favs) ft[f.tip_id] = f.timestamp;
                     setFavTimes(ft);
                     const rt: Record<number, number> = {};
                     for (const r of reps) rt[r.tip_id] = r.timestamp;
                     setRepTimes(rt);
                })
                .catch(() => {});
           fetchTips()
                .then((tipsList) => setTips(tipsList))
                .catch(() => {});
      }, []);

      // Lazy-load achievements only when tab needs it
      useEffect(() => {
           if (tab !== "achievements") return;
           getAchievements()
                .then((ach) => {
                     setAchievements(ach);
                     const ev: Record<string, number> = {};
                     for (const a of ach) ev[a.achievement_name] = a.timestamp;
                     setLoadedEvents(ev);
                })
                .catch(() => {});
      }, [tab]);

      useEffect(() => {
           if (tab !== "comments") return;
           const fetchComments = () =>
                getAllComments()
                     .then((all) => setComments([...all].sort((a, b) => b.timestamp - a.timestamp)))
                     .catch(() => {});
           fetchComments();
           const onFocus = () => fetchComments();
           window.addEventListener("focus", onFocus);
           return () => window.removeEventListener("focus", onFocus);
      }, [tab]);

     useEffect(() => {
          load();
          const onFocus = () => load();
          window.addEventListener("focus", onFocus);
          return () =>
               window.removeEventListener("focus", onFocus);
     }, [load]);

     const unlockedSet = new Set(
          achievements
               .filter((a) => a.unlocked)
               .map((a) => a.achievement_name),
     );
     const initials = (meta?.name ?? "P")
          .trim()
          .slice(0, 2)
          .toUpperCase();

     return (
          <main className="mx-auto h-full max-w-2xl overflow-y-auto bg-bg">
               {/* header */}
               <motion.header
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                    className="flex shrink-0 flex-col items-center gap-4 border-b border-line/50 px-4 pb-8 pt-[max(2.5rem,env(safe-area-inset-top))]"
               >
                    <motion.div
                         initial={{
                              scale: 0.8,
                              opacity: 0,
                         }}
                         animate={{ scale: 1, opacity: 1 }}
                         transition={{
                              type: "spring",
                              stiffness: 300,
                              damping: 20,
                              delay: 0.1,
                         }}
                         className="relative flex h-22 w-22 items-center justify-center rounded-full bg-gradient-to-br from-accent/20 to-accent/5 border border-accent/30 text-2xl font-semibold"
                    >
                         <span className="relative z-10 bg-gradient-to-r from-accent to-accent/70 bg-clip-text text-transparent">
                              {initials}
                         </span>
                         <div className="absolute inset-0 rounded-full bg-gradient-to-br from-accent/20 to-transparent blur-xl opacity-50" />
                    </motion.div>
                    <motion.div
                         initial={{ opacity: 0, y: 10 }}
                         animate={{ opacity: 1, y: 0 }}
                         transition={{
                              delay: 0.15,
                              duration: 0.3,
                         }}
                         className="text-center"
                    >
                         <h1 className="text-lg font-semibold text-fg">
                              {meta?.name ?? "Pythonista"}
                         </h1>
                         {/* <p className="font-mono text-[11px] text-muted/70">{"// pyscroll local profile"}</p> */}
                    </motion.div>
                    <motion.div
                         initial={{ opacity: 0, y: 10 }}
                         animate={{ opacity: 1, y: 0 }}
                         transition={{
                              delay: 0.2,
                              duration: 0.3,
                         }}
                         className="grid w-full max-w-sm grid-cols-3 gap-2 text-center"
                    >
                         <Stat
                              label="time"
                              value={formatClock(
                                   meta?.total_time ?? 0,
                              )}
                         />
                         <Stat
                              label="likes"
                              value={String(
                                   meta?.total_likes ?? 0,
                              )}
                         />
                         <Stat
                              label="reposts"
                              value={String(
                                   meta?.total_reposts ?? 0,
                              )}
                         />
                    </motion.div>
               </motion.header>

               {/* tabs */}
               <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{
                         delay: 0.25,
                         duration: 0.3,
                    }}
                    className="sticky top-0 z-10 flex border-b border-line/50 bg-bgro/80 backdrop-blur-xl"
               >
                     {(
                          [
                               ["favorites", "Favorites"],
                               ["reposts", "Reposts"],
                               ["comments", "Comments"],
                               [
                                    "achievements",
                                    "Achievements",
                               ],
                          ] as [Tab, string][]
                     ).map(([key, label], i) => (
                         <motion.button
                              key={key}
                              onClick={() => setTab(key)}
                              whileTap={{ scale: 0.98 }}
                              layout
                              className={`relative flex-1 py-3.5 text-sm font-medium transition-colors ${
                                   tab === key
                                        ? "text-fg"
                                        : "text-muted/70 hover:text-fg/80"
                              }`}
                              transition={{
                                   delay: i * 0.05,
                              }}
                         >
                              {label}
                              {tab === key && (
                                   <motion.span
                                        layoutId="profile-tab-indicator"
                                        className="absolute inset-x-6 bottom-0 h-0.5 rounded-full bg-accent"
                                   />
                              )}
                         </motion.button>
                    ))}
               </motion.div>

               <div className="p-4 pb-32">
                    {tab === "favorites" && (
                         <motion.div
                              initial={{
                                   opacity: 0,
                                   y: 10,
                              }}
                              animate={{ opacity: 1, y: 0 }}
                              transition={{ duration: 0.3 }}
                              key="favorites"
                         >
                              <ListGroup
                                   title="Liked tips"
                                   items={favIds}
                                   tips={tips}
                                   times={favTimes}
                                   empty="Nothing liked yet. Hit the heart on a tip you love."
                              />
                         </motion.div>
                    )}
                     {tab === "reposts" && (
                          <motion.div
                               initial={{
                                    opacity: 0,
                                    y: 10,
                               }}
                               animate={{ opacity: 1, y: 0 }}
                               transition={{ duration: 0.3 }}
                               key="reposts"
                          >
                               <ListGroup
                                    title="Reposted tips"
                                    items={repIds}
                                    tips={tips}
                                    times={repTimes}
                                    empty="Nothing reposted yet."
                               />
                          </motion.div>
                     )}
                     {tab === "comments" && (
                          <motion.div
                               initial={{
                                    opacity: 0,
                                    y: 10,
                               }}
                               animate={{ opacity: 1, y: 0 }}
                               transition={{ duration: 0.3 }}
                               key="comments"
                          >
                               <CommentGroup
                                    comments={comments}
                                    tips={tips}
                                    empty="No comments yet. Join the discussion on any tip."
                               />
                          </motion.div>
                     )}
                     {tab === "achievements" && (
                         <motion.div
                              initial={{
                                   opacity: 0,
                                   y: 10,
                              }}
                              animate={{ opacity: 1, y: 0 }}
                              transition={{ duration: 0.3 }}
                              key="achievements"
                         >
                              <div className="grid grid-cols-3 gap-3 pt-2">
                                   {ACHIEVEMENTS.map(
                                        (def, i) => {
                                             const unlocked =
                                                  unlockedSet.has(
                                                       def.id,
                                                  );
                                              return (
                                                   <Link
                                                        key={def.id}
                                                        href={`/notifications?achievement=${def.id}`}
                                                        aria-label={def.name}
                                                        className="block rounded-2xl"
                                                   >
                                                   <motion.div
                                                        initial={{
                                                             scale: 0.9,
                                                             opacity: 0,
                                                        }}
                                                       animate={{
                                                            scale: 1,
                                                            opacity: 1,
                                                       }}
                                                       transition={{
                                                            delay:
                                                                 0.05 +
                                                                 i *
                                                                      0.03,
                                                            duration: 0.3,
                                                       }}
                                                       whileHover={{
                                                            scale: 1.02,
                                                       }}
                                                       className={`flex flex-col items-center gap-1.5 rounded-2xl border p-3 text-center transition-all ${
                                                            unlocked
                                                                 ? "border-accent/40 bg-accentsoft/50 shadow-[0_0_20px_-5px_var(--accentsoft)]"
                                                                 : "border-line/50 bg-bgsoft/40 opacity-70 hover:border-accent/30 hover:bg-accentsoft/20"
                                                       }`}
                                                       title={
                                                            def.description
                                                       }
                                                  >
                                                       <span
                                                            className={`flex h-10 w-10 items-center justify-center rounded-xl ${unlocked ? "bg-accent/15 text-accent" : "bg-bgsoft/50 text-muted/50"}`}
                                                       >
                                                            {unlocked ? (
                                                                 <def.Icon
                                                                      className="h-5 w-5"
                                                                      strokeWidth={
                                                                           1.9
                                                                      }
                                                                 />
                                                            ) : (
                                                                 <LockKeyhole
                                                                      className="h-5 w-5"
                                                                      strokeWidth={
                                                                           1.9
                                                                      }
                                                                 />
                                                            )}
                                                       </span>
                                                       <span
                                                            className={`text-[11px] leading-tight ${unlocked ? "text-fg" : "text-muted/70"}`}
                                                       >
                                                            {
                                                                 def.name
                                                            }
                                                       </span>
                                                       {unlocked &&
                                                            loadedEvents[
                                                                 def
                                                                      .id
                                                            ] && (
                                                                 <span className="font-mono text-[9px] text-accent/80">
                                                                      {relTime(
                                                                           loadedEvents[
                                                                                def
                                                                                     .id
                                                                           ],
                                                                      )}
                                                                  </span>
                                                             )}
                                                   </motion.div>
                                                   </Link>
                                              );
                                        },
                                   )}
                              </div>
                         </motion.div>
                    )}
               </div>
          </main>
     );
}

function Stat({
     label,
     value,
}: {
     label: string;
     value: string;
}) {
     return (
          <motion.div
               whileHover={{ y: -2 }}
               className="rounded-xl border border-line/50 bg-bgsoft/60 px-3 py-3 transition-all hover:border-accent/30"
          >
               <p className="font-mono text-sm font-semibold tabular-nums text-fg">
                    {value}
               </p>
               <p className="text-[10px] uppercase tracking-widest text-muted/70">
                    {label}
               </p>
          </motion.div>
     );
}

function ListGroup({
     title,
     items,
     tips,
     times,
     empty,
}: {
     title: string;
     items: number[];
     tips: Tip[];
     times: Record<number, number>;
     empty: string;
}) {
     const tipMap = new Map(tips.map((t) => [t.id, t]));
     if (items.length === 0) {
          return (
               <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="py-16 text-center"
               >
                    <p className="text-sm text-muted/70">
                         {empty}
                    </p>
               </motion.div>
          );
     }
     return (
          <motion.div
               initial={{ opacity: 0 }}
               animate={{ opacity: 1 }}
               className="space-y-2"
          >
               <p className="px-1 text-[11px] uppercase tracking-widest text-muted/70">
                    {title}
               </p>
               {items.map((id, i) => {
                    const tip = tipMap.get(id);
                    if (!tip) return null;
                    return (
                         <motion.div
                              key={id}
                              initial={{
                                   opacity: 0,
                                   x: -10,
                              }}
                              animate={{ opacity: 1, x: 0 }}
                              transition={{
                                   delay: i * 0.03,
                                   duration: 0.2,
                              }}
                              layout
                         >
                              <Link
                                    href={`/feed?tip=${tip.id}`}
                                   className="group flex items-center gap-3 rounded-2xl border border-line/50 bg-bgsoft/60 px-4 py-3 transition-all hover:border-accent/30 hover:bg-accentsoft/20"
                              >
                                   <div className="min-w-0 flex-1">
                                        <p className="truncate text-sm font-medium group-hover:text-accent transition-colors">
                                             {tip.title}
                                        </p>
                                        <div className="flex items-center gap-2">
                                             <span className="rounded-full bg-accentsoft px-2 py-0.5 font-mono text-[10px] uppercase tracking-wider text-accent">
                                                  {
                                                       tip.category
                                                  }
                                             </span>
                                             <span className="font-mono text-[10px] text-muted/60">
                                                  {times[
                                                       id
                                                  ] !==
                                                  undefined
                                                       ? relTime(
                                                              times[
                                                                   id
                                                              ],
                                                         )
                                                       : ""}
                                             </span>
                                        </div>
                                   </div>
                                   <motion.span
                                        whileHover={{
                                             x: 3,
                                        }}
                                        className="shrink-0 text-muted/60 transition-transform"
                                   >
                                        →
                                   </motion.span>
                              </Link>
                         </motion.div>
                    );
                })}
           </motion.div>
      );
}

function CommentGroup({
     comments,
     tips,
     empty,
}: {
     comments: Comment[];
     tips: Tip[];
     empty: string;
}) {
     const tipMap = new Map(tips.map((t) => [t.id, t]));
     if (comments.length === 0) {
          return (
               <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="py-16 text-center"
               >
                    <p className="text-sm text-muted/70">{empty}</p>
               </motion.div>
          );
     }
     return (
          <motion.div
               initial={{ opacity: 0 }}
               animate={{ opacity: 1 }}
               className="space-y-2"
          >
               <p className="px-1 text-[11px] uppercase tracking-widest text-muted/70">
                    Comments
               </p>
               {comments.map((c, i) => {
                    const tip = tipMap.get(c.tip_id);
                    if (!tip) return null;
                    return (
                         <motion.div
                              key={c.id ?? `${c.tip_id}-${c.timestamp}-${i}`}
                              initial={{ opacity: 0, x: -10 }}
                              animate={{ opacity: 1, x: 0 }}
                              transition={{ delay: i * 0.03, duration: 0.2 }}
                              layout
                         >
                              <Link
                                   href={`/feed?tip=${c.tip_id}`}
                                   className="group flex flex-col gap-2 rounded-2xl border border-line/50 bg-bgsoft/60 px-4 py-3 transition-all hover:border-accent/30 hover:bg-accentsoft/20"
                              >
                                   <div className="flex items-center gap-2">
                                        <span className="rounded-full bg-accentsoft px-2 py-0.5 font-mono text-[10px] uppercase tracking-wider text-accent">
                                             {tip.category}
                                        </span>
                                        <span className="truncate text-xs font-medium text-fg/80 group-hover:text-accent">
                                             {tip.title}
                                        </span>
                                        <span className="ml-auto shrink-0 font-mono text-[10px] text-muted/60">
                                             {relTime(c.timestamp)}
                                        </span>
                                   </div>
                                   <p className="line-clamp-2 text-sm leading-5 text-fg/90">
                                        “{c.comment_text}”
                                   </p>
                                   <span className="self-end text-[11px] text-muted/60 group-hover:text-accent transition-colors">
                                        View tip →
                                   </span>
                              </Link>
                         </motion.div>
                    );
               })}
          </motion.div>
     );
}
