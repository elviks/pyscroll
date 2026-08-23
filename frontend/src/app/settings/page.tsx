"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { clearAllData, getUserMeta, setUserMeta } from "@/lib/db";
import { useTheme } from "@/lib/theme";
import { checkAchievements } from "@/lib/achievements";
import { FEED_CATEGORIES } from "@/lib/categories";
import { MoonIcon, SunIcon, TrashIcon } from "@/components/icons";

export default function SettingsPage() {
  const { theme, toggle } = useTheme();
  const [name, setName] = useState("Pythonista");
  const [saved, setSaved] = useState(false);
  const [confirming, setConfirming] = useState(false);
  const [cleared, setCleared] = useState(false);
  const [feedCat, setFeedCat] = useState("python");

  useEffect(() => {
    getUserMeta()
      .then((m) => {
        setName(m.name);
        setFeedCat(m.feed_category || "python");
      })
      .catch(() => {});
  }, []);

  async function saveName() {
    const next = name.trim().slice(0, 24) || "Pythonista";
    setName(next);
    await setUserMeta({ name: next }).catch(() => {});
    setSaved(true);
    setTimeout(() => setSaved(false), 1600);
  }

  async function wipeAll() {
    await clearAllData().catch(() => {});
    localStorage.removeItem("pyscroll-theme");
    setConfirming(false);
    setCleared(true);
    checkAchievements().catch(() => {});
    setTimeout(() => setCleared(false), 1600);
  }

  return (
    <main className="mx-auto h-full max-w-2xl overflow-y-auto bg-bg">
      <div className="space-y-8 p-4 pb-12">
        <motion.section
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="space-y-3"
        >
          <h2 className="px-1 text-[11px] uppercase tracking-widest text-muted">Profile</h2>
          <div className="rounded-2xl border border-line/50 bg-bgsoft/60 p-4 transition-colors hover:border-accent/30">
            <label htmlFor="name" className="text-xs text-muted/70">
              Display name
            </label>
            <div className="mt-2 flex gap-2">
              <input
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") saveName();
                }}
                maxLength={24}
                className="flex-1 rounded-full border border-line/50 bg-bg px-4 py-2.5 text-sm outline-none transition-colors placeholder:text-muted/50 focus:border-accent focus:bg-bgsoft"
              />
              <motion.button
                onClick={saveName}
                whileTap={{ scale: 0.96 }}
                className="rounded-full bg-accent px-5 py-2.5 text-sm font-medium text-white transition-all hover:opacity-90 active:scale-[0.98]"
              >
                {saved ? "Saved ✓" : "Save"}
              </motion.button>
            </div>
          </div>
        </motion.section>

        <motion.section
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.05, duration: 0.4 }}
          className="space-y-3"
        >
          <h2 className="px-1 text-[11px] uppercase tracking-widest text-muted">Appearance</h2>
          <div className="flex items-center justify-between rounded-2xl border border-line/50 bg-bgsoft/60 p-4 transition-colors hover:border-accent/30">
            <div className="flex items-center gap-3">
              <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-accentsoft text-accent">
                {theme === "dark" ? <MoonIcon className="h-5 w-5" /> : <SunIcon className="h-5 w-5" />}
              </span>
              <div>
                <p className="text-sm font-medium">{theme === "dark" ? "Dark mode" : "Light mode"}</p>
                <p className="text-xs text-muted/70">Deep black, easy on the eyes</p>
              </div>
            </div>
            <button
              onClick={toggle}
              role="switch"
              aria-checked={theme === "dark"}
              aria-label="Toggle dark mode"
              className={`relative h-7 w-12 rounded-full transition-colors duration-200 ${
                theme === "dark" ? "bg-accent" : "bg-line"
              }`}
            >
              <motion.span
                animate={{ x: theme === "dark" ? 22 : 0 }}
                transition={{ type: "spring", stiffness: 500, damping: 32 }}
                className="absolute left-0.5 top-0.5 h-6 w-6 rounded-full bg-white shadow-md"
              />
            </button>
          </div>
        </motion.section>

        <motion.section
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1, duration: 0.4 }}
          className="space-y-3"
        >
          <h2 className="px-1 text-[11px] uppercase tracking-widest text-muted">
            Customize your feed
          </h2>
          <p className="px-1 text-xs leading-5 text-muted/70">
            Pick what you want to doomscroll about. The Home feed only shows cards from the
            selected category.
          </p>
          <div className="grid grid-cols-2 gap-2">
            {FEED_CATEGORIES.map((c, i) => {
              const active = feedCat === c.id;
              return (
                <motion.button
                  key={c.id}
                  onClick={() => {
                    setFeedCat(c.id);
                    setUserMeta({ feed_category: c.id }).catch(() => {});
                  }}
                  aria-pressed={active}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 + i * 0.05, duration: 0.3 }}
                  whileTap={{ scale: 0.98 }}
                  className={`relative rounded-2xl border p-4 text-left transition-all duration-200 ${
                    active
                      ? "border-accent/50 bg-accentsoft/50 shadow-[0_0_0_1px_var(--accentsoft)]"
                      : "border-line/50 bg-bgsoft/60 hover:border-accent/30 hover:bg-accentsoft/20"
                  }`}
                >
                  <div className="flex items-start justify-between gap-2">
                    <p className={`text-sm font-medium ${active ? "text-accent" : "text-fg"}`}>
                      {c.label}
                    </p>
                    {active && (
                      <motion.span
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ type: "spring", stiffness: 400, damping: 17 }}
                        className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-accent text-[10px] text-white"
                      >
                        ✓
                      </motion.span>
                    )}
                  </div>
                  <p className="mt-2 line-clamp-2 text-[11px] leading-4 text-muted/70">{c.blurb}</p>
                </motion.button>
              );
            })}
          </div>
        </motion.section>

        <motion.section
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.15, duration: 0.4 }}
          className="space-y-3"
        >
          <h2 className="px-1 text-[11px] uppercase tracking-widest text-muted">Data</h2>
          <div className="rounded-2xl border border-line/50 bg-bgsoft/60 p-4 transition-colors hover:border-accent/30">
            <div className="flex items-center justify-between gap-3">
              <div className="flex items-center gap-3">
                <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-red-500/15 text-red-400">
                  <TrashIcon />
                </span>
                <div>
                  <p className="text-sm font-medium">Clear local cache</p>
                  <p className="text-xs text-muted/70">
                    Wipes likes, reposts, comments, chats & achievements from IndexedDB
                  </p>
                </div>
              </div>
              {!confirming ? (
                <motion.button
                  onClick={() => setConfirming(true)}
                  whileTap={{ scale: 0.96 }}
                  className="shrink-0 rounded-full border border-red-500/40 px-3.5 py-1.5 text-xs text-red-400 transition-all hover:bg-red-500/10"
                >
                  Wipe
                </motion.button>
              ) : (
                <div className="flex shrink-0 gap-2">
                  <motion.button
                    onClick={wipeAll}
                    whileTap={{ scale: 0.96 }}
                    className="rounded-full bg-red-500 px-3.5 py-1.5 text-xs font-medium text-white transition-opacity hover:opacity-90"
                  >
                    {cleared ? "Wiped ✓" : "Confirm"}
                  </motion.button>
                  <motion.button
                    onClick={() => setConfirming(false)}
                    whileTap={{ scale: 0.96 }}
                    className="rounded-full border border-line/50 px-3.5 py-1.5 text-xs text-muted transition-all hover:border-accent/30 hover:text-fg"
                  >
                    Cancel
                  </motion.button>
                </div>
              )}
            </div>
          </div>
        </motion.section>

        <motion.section
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.4 }}
          className="space-y-3"
        >
          <h2 className="px-1 text-[11px] uppercase tracking-widest text-muted">About</h2>
          <div className="rounded-2xl border border-line/50 bg-bgsoft/60 p-4 font-mono text-xs leading-6 text-muted/70">
            <p>pyscroll v1.0.0 — doomscrolling for Python</p>
            <p>frontend · next.js + tailwind + framer-motion</p>
            <p>storage · indexeddb (all local)</p>
            <p>backend · fastapi + groq llm</p>
          </div>
        </motion.section>
      </div>
    </main>
  );
}