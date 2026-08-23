"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { motion } from "framer-motion";
import { ACHIEVEMENTS } from "@/lib/achievements";
import type { Achievement } from "@/lib/db";
import { getAchievements } from "@/lib/db";
import { relTime } from "@/lib/time";
import { TrophyIcon } from "@/components/icons";
import { LockKeyhole } from "lucide-react";

export default function NotificationsPage() {
  const [unlocked, setUnlocked] = useState<Record<string, Achievement>>({});
  const [loaded, setLoaded] = useState(false);
  const [highlight, setHighlight] = useState<string | null>(null);
  const scrolledRef = useRef(false);

  function buildMap(all: Achievement[]): Record<string, Achievement> {
    const map: Record<string, Achievement> = {};
    for (const a of all) map[a.achievement_name] = a;
    return map;
  }

  useEffect(() => {
    getAchievements()
      .then((all) => {
        setUnlocked(buildMap(all));
        setLoaded(true);
      })
      .catch(() => setLoaded(true));
    const onFocus = () => {
      getAchievements()
        .then((all) => setUnlocked(buildMap(all)))
        .catch(() => {});
    };
    window.addEventListener("focus", onFocus);
    return () => window.removeEventListener("focus", onFocus);
  }, []);

  // ---- deep link (?achievement=ID): scroll to & flash that badge ----
  useEffect(() => {
    if (!loaded || scrolledRef.current) return;
    const target = new URLSearchParams(window.location.search).get("achievement");
    history.replaceState(null, "", "/notifications");
    if (!target) return;
    scrolledRef.current = true;
    const el = document.querySelector<HTMLElement>(`[data-achievement-id="${target}"]`);
    if (!el) return;
    const t = setTimeout(() => {
      el.scrollIntoView({ behavior: "smooth", block: "center" });
      setHighlight(target);
    }, 350);
    const clear = setTimeout(() => setHighlight(null), 2600);
    return () => {
      clearTimeout(t);
      clearTimeout(clear);
    };
  }, [loaded]);

  const unlockedList = useMemo(
    () =>
      ACHIEVEMENTS.filter((a) => unlocked[a.id]).sort(
        (a, b) => (unlocked[b.id]?.timestamp ?? 0) - (unlocked[a.id]?.timestamp ?? 0),
      ),
    [unlocked],
  );
  const lockedList = useMemo(() => ACHIEVEMENTS.filter((a) => !unlocked[a.id]), [unlocked]);

  const [visibleLocked, setVisibleLocked] = useState(20);
  useEffect(() => {
    setVisibleLocked(20);
  }, [lockedList.length]);
  const visibleLockedList = useMemo(
    () => lockedList.slice(0, visibleLocked),
    [lockedList, visibleLocked],
  );

  return (
    <main className="mx-auto h-full max-w-2xl overflow-y-auto bg-bg">
      <motion.header
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="sticky top-0 z-10 flex items-center gap-3 border-b border-line/50 bg-bgro/80 px-4 py-3 backdrop-blur-xl"
      >
        <motion.span
          whileHover={{ scale: 1.05, rotate: 5 }}
          className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-accent/20 to-accent/5 border border-accent/30"
        >
          <TrophyIcon className="h-5 w-5 text-accent" />
        </motion.span>
        <p className="text-[11px] uppercase tracking-widest text-muted/70">
          {Object.keys(unlocked).length} / {ACHIEVEMENTS.length} unlocked
        </p>
      </motion.header>

      <div className="space-y-3 p-4">
        {!loaded && (
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="py-16 text-center text-sm text-muted/60"
          >
            loading…
          </motion.p>
        )}
        {loaded && unlockedList.length === 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="py-20 text-center"
          >
            <p className="text-sm text-muted/60">
              Nothing yet. Go like, scroll, and ask questions — badges will land here.
            </p>
          </motion.div>
        )}

        {unlockedList.map((def, i) => (
          <motion.div
            key={def.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.05, duration: 0.3 }}
            whileHover={{ x: 4 }}
            data-achievement-id={def.id}
            className={`flex items-center gap-3 rounded-2xl border px-4 py-3 transition-all hover:border-accent/60 hover:bg-accentsoft hover:shadow-[0_0_20px_-5px_var(--accentsoft)] ${
              highlight === def.id
                ? "border-accent bg-accentsoft shadow-[0_0_30px_-5px_var(--accentsoft)]"
                : "border-accent/40 bg-accentsoft/50"
            }`}
          >
            <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-accent/15 text-accent">
              <def.Icon className="h-5 w-5" strokeWidth={1.9} />
            </span>
            <div className="min-w-0 flex-1">
              <p className="text-sm font-semibold text-fg">{def.name}</p>
              <p className="text-xs text-muted/70">{def.description}</p>
            </div>
            <span className="shrink-0 font-mono text-[10px] text-muted/60">
              {unlocked[def.id] ? relTime(unlocked[def.id].timestamp) : ""}
            </span>
          </motion.div>
        ))}

        {lockedList.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: unlockedList.length * 0.05 + 0.1 }}
            className="pt-4"
          >
            <p className="px-1 pb-2 text-[11px] uppercase tracking-widest text-muted/60">
              Locked
            </p>
            {visibleLockedList.map((def, i) => (
              <motion.div
                key={def.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: Math.min(i * 0.015, 0.3), duration: 0.2 }}
                data-achievement-id={def.id}
                className={`flex items-center gap-3 rounded-2xl border px-4 py-3 transition-colors hover:border-accent/30 hover:bg-accentsoft/20 hover:opacity-80 ${
                  highlight === def.id
                    ? "border-accent bg-accentsoft/40 opacity-100"
                    : "border-line/50 bg-bgsoft/40 opacity-60"
                }`}
              >
                <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-bgsoft/50 text-muted/40">
                  <def.Icon className="h-5 w-5" strokeWidth={1.9} />
                </span>
                <div className="min-w-0 flex-1">
                  <p className="text-sm font-medium text-fg/60">{def.name}</p>
                  <p className="text-xs text-muted/50">{def.description}</p>
                </div>
                <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-bgsoft/50 text-muted/50">
                  <LockKeyhole className="h-4 w-4" strokeWidth={1.9} />
                </span>
              </motion.div>
            ))}
            {visibleLocked < lockedList.length && (
              <button
                onClick={() => setVisibleLocked((n) => Math.min(n + 20, lockedList.length))}
                className="mt-3 w-full rounded-2xl border border-line/50 bg-bgsoft/40 px-4 py-3 text-sm text-muted transition-colors hover:border-accent/30 hover:bg-accentsoft/20"
              >
                Show {Math.min(20, lockedList.length - visibleLocked)} more ({lockedList.length - visibleLocked} remaining)
              </button>
            )}
          </motion.div>
        )}
      </div>
    </main>
  );
}