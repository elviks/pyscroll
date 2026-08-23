"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { createPortal } from "react-dom";
import { AnimatePresence, motion } from "framer-motion";
import { Flame, Settings } from "lucide-react";
import { getUserMeta } from "@/lib/db";
import { PythonLogo } from "./icons";

const TITLES: Record<string, string> = {
     "/": "FEED",
     "/messages": "PYTHON TUTOR",
     "/notifications": "ACHIEVEMENTS",
     "/profile": "PROFILE",
     "/settings": "SETTINGS",
     "/playground": "TRY IT YOURSELF",
};

export default function TopBar() {
     const pathname = usePathname();
     const [mounted, setMounted] = useState(false);
     const [streak, setStreak] = useState(0);
     const [longest, setLongest] = useState(0);
     const [open, setOpen] = useState(false);
     const title = TITLES[pathname] ?? "FEED";

     useEffect(() => {
          const id = requestAnimationFrame(() =>
               setMounted(true),
          );
          return () => cancelAnimationFrame(id);
     }, []);

     useEffect(() => {
          let active = true;
          const load = () =>
               getUserMeta()
                    .then((m) => {
                         if (!active) return;
                         setStreak(m.current_streak ?? 0);
                         setLongest(m.longest_streak ?? 0);
                    })
                    .catch(() => {});
          load();
          window.addEventListener("focus", load);
          return () => {
               active = false;
               window.removeEventListener("focus", load);
          };
     }, [pathname]);

     useEffect(() => {
          if (!open) return;
          const onKey = (e: KeyboardEvent) => {
               if (e.key === "Escape") setOpen(false);
          };
          window.addEventListener("keydown", onKey);
          return () =>
               window.removeEventListener("keydown", onKey);
     }, [open]);

     if (mounted && pathname === "/") return null;

     return (
          <>
               <header className="shrink-0 border-b border-line bg-bgro/80 backdrop-blur-xl pt-[env(safe-area-inset-top)]">
                    <div className="relative flex h-14 items-center justify-between px-4">
                         <Link
                              href="/feed"
                              className="flex items-center gap-2.5"
                              aria-label="PyScroll home"
                         >
                              <motion.div
                                   whileHover={{
                                        scale: 1.08,
                                        rotate: 3,
                                   }}
                                   whileTap={{
                                        scale: 0.92,
                                   }}
                                   transition={{
                                        type: "spring",
                                        stiffness: 400,
                                        damping: 17,
                                   }}
                                   className="flex h-10 items-center justify-center rounded-xl bg-transparent"
                              >
                                   <PythonLogo
                                        className="h-15"
                                        icon
                                   />
                              </motion.div>
                         </Link>
                         <span className="pointer-events-none absolute left-1/2 -translate-x-1/2 text-sm font-bold tracking-tight text-fg">
                              {title}
                         </span>
                         <div className="flex items-center gap-2">
                              <motion.button
                                   key={streak}
                                   initial={{
                                        scale: 0.7,
                                        opacity: 0,
                                   }}
                                   animate={{
                                        scale: 1,
                                        opacity: 1,
                                   }}
                                   whileTap={{ scale: 0.9 }}
                                   transition={{
                                        type: "spring",
                                        stiffness: 400,
                                        damping: 20,
                                   }}
                                   onClick={() =>
                                        setOpen(true)
                                   }
                                   className="flex items-center gap-1 rounded-full border border-orange-500/30 bg-orange-500/20 px-2 py-1"
                                   title={`Daily streak: ${streak} day${streak === 1 ? "" : "s"}`}
                                   aria-label={`Daily streak: ${streak} days`}
                              >
                                   <Flame
                                        className="h-3.5 w-3.5 text-orange-500"
                                        strokeWidth={2}
                                   />
                                   <span className="font-mono text-[11px] font-semibold tabular-nums text-fg">
                                        {streak}
                                   </span>
                              </motion.button>
                              <Link
                                   href="/settings"
                                   aria-label="Settings"
                                   className="flex h-8 w-8 items-center justify-center rounded-full border border-line/50 bg-bgsoft/60 text-muted transition-colors hover:border-accent/30 hover:bg-accentsoft hover:text-accent"
                              >
                                   <Settings
                                        className="h-4 w-4"
                                        strokeWidth={1.9}
                                   />
                              </Link>
                         </div>
                    </div>
               </header>

               {mounted &&
                    createPortal(
                         <AnimatePresence>
                              {open && (
                                   <motion.div
                                        initial={{
                                             opacity: 0,
                                        }}
                                        animate={{
                                             opacity: 1,
                                        }}
                                        exit={{
                                             opacity: 0,
                                        }}
                                        transition={{
                                             duration: 0.2,
                                        }}
                                        onClick={() =>
                                             setOpen(false)
                                        }
                                        className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-6 backdrop-blur-sm"
                                   >
                                        <motion.div
                                             initial={{
                                                  scale: 0.85,
                                                  opacity: 0,
                                                  y: 14,
                                             }}
                                             animate={{
                                                  scale: 1,
                                                  opacity: 1,
                                                  y: 0,
                                             }}
                                             exit={{
                                                  scale: 0.9,
                                                  opacity: 0,
                                             }}
                                             transition={{
                                                  type: "spring",
                                                  stiffness: 380,
                                                  damping: 26,
                                             }}
                                             onClick={(e) =>
                                                  e.stopPropagation()
                                             }
                                             role="dialog"
                                             aria-modal="true"
                                             aria-label="Daily streak"
                                             className="flex w-full max-w-xs flex-col items-center gap-5 rounded-3xl border border-line/60 bg-bgsoft px-8 py-10 text-center shadow-xl"
                                        >
                                             <div className="relative flex h-24 w-24 items-center justify-center">
                                                  <motion.div
                                                       animate={{
                                                            scale: [
                                                                 1,
                                                                 1.15,
                                                                 1,
                                                            ],
                                                            opacity: [
                                                                 0.4,
                                                                 0.7,
                                                                 0.4,
                                                            ],
                                                       }}
                                                       transition={{
                                                            duration: 2,
                                                            repeat: Infinity,
                                                            ease: "easeInOut",
                                                       }}
                                                       className="absolute inset-0 rounded-full bg-orange-400/25 blur-2xl"
                                                  />
                                                  <Flame
                                                       className="relative h-16 w-16 text-orange-500 drop-shadow-[0_0_12px_var(--accentsoft)]"
                                                       strokeWidth={
                                                            1.5
                                                       }
                                                  />
                                             </div>
                                             <div>
                                                  <p className="text-lg font-semibold text-fg">
                                                       {
                                                            streak
                                                       }{" "}
                                                       day
                                                       streak
                                                  </p>
                                                  <p className="mt-1 font-mono text-[11px] uppercase tracking-widest text-muted">
                                                       keep
                                                       it
                                                       alive
                                                  </p>
                                             </div>
                                             <p className="font-mono text-[10px] uppercase tracking-widest text-muted/70">
                                                  longest ·{" "}
                                                  {longest}{" "}
                                                  {longest ===
                                                  1
                                                       ? "day"
                                                       : "days"}
                                             </p>
                                        </motion.div>
                                   </motion.div>
                              )}
                         </AnimatePresence>,
                         document.body,
                    )}
          </>
     );
}
