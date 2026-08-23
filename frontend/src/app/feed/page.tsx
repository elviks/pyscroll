"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { motion } from "framer-motion";
import { fetchTips, FALLBACK_TIPS } from "@/lib/api";
import type { Tip } from "@/lib/types";
import {
  addFavorite,
  addRepost,
  getCommentsByTip,
  getFavorites,
  getReposts,
  getUserMeta,
  removeFavorite,
  removeRepost,
  setUserMeta,
} from "@/lib/db";
import { checkAchievements } from "@/lib/achievements";
import { feedCategoryOf, feedLabel } from "@/lib/categories";
import dynamic from "next/dynamic";
import TipCard from "@/components/TipCard";
const CommentSheet = dynamic(() => import("@/components/CommentSheet"), { ssr: false });
const AchievementToast = dynamic(() => import("@/components/AchievementToast"), { ssr: false });
import { PythonLogo } from "@/components/icons";
import { Compass } from "lucide-react";

const SCROLL_KEY = "pyscroll:feedScroll";
const SEEN_KEY = "pyscroll:feedSeen";

function loadScrollState(): Record<string, number> {
  try {
    const raw = sessionStorage.getItem(SCROLL_KEY);
    return raw ? (JSON.parse(raw) as Record<string, number>) : {};
  } catch {
    return {};
  }
}

function saveScrollState(map: Record<string, number>) {
  try {
    sessionStorage.setItem(SCROLL_KEY, JSON.stringify(map));
  } catch {
    // storage unavailable
  }
}

function loadSeenIds(): number[] {
  try {
    const raw = sessionStorage.getItem(SEEN_KEY);
    return raw ? (JSON.parse(raw) as number[]) : [];
  } catch {
    return [];
  }
}

function saveSeenIds(ids: Set<number>) {
  try {
    sessionStorage.setItem(SEEN_KEY, JSON.stringify([...ids]));
  } catch {
    // storage unavailable
  }
}

const FEED_CACHE_KEY = "pyscroll:feedCache";

interface FeedCache {
  tips: Tip[];
  feedItems: FeedItem[];
  offline: boolean;
  feedCat: string;
}

function loadFeedCache(): FeedCache | null {
  try {
    const raw = sessionStorage.getItem(FEED_CACHE_KEY);
    return raw ? (JSON.parse(raw) as FeedCache) : null;
  } catch {
    return null;
  }
}

function saveFeedCache(cache: FeedCache) {
  try {
    sessionStorage.setItem(FEED_CACHE_KEY, JSON.stringify(cache));
  } catch {
    // storage unavailable
  }
}

function shuffleArray<T>(array: T[]): T[] {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}

type FeedItem = { key: string; tip: Tip };

const BATCH_SIZE = 8;
const INITIAL_BATCHES = 3;
const MAX_FEED_ITEMS = 200;

let instanceSeq = 0;

function nextKey(tipId: number): string {
  instanceSeq += 1;
  return `${tipId}#${instanceSeq}`;
}

function buildBatch(source: Tip[]): FeedItem[] {
  return shuffleArray(source)
    .slice(0, BATCH_SIZE)
    .map((tip) => ({ key: nextKey(tip.id), tip }));
}

export default function FeedPage() {
  const [tips, setTips] = useState<Tip[]>(FALLBACK_TIPS);
  const [offline, setOffline] = useState(false);
  const [favs, setFavs] = useState<Set<number>>(new Set());
  const [reposts, setReposts] = useState<Set<number>>(new Set());
  const [likeCounts, setLikeCounts] = useState<Record<number, number>>({});
  const [commentCounts, setCommentCounts] = useState<Record<number, number>>({});
  const [commentFor, setCommentFor] = useState<Tip | null>(null);
  const [toast, setToast] = useState<string | null>(null);
  const [highlight, setHighlight] = useState<number | null>(null);
  const [feedCat, setFeedCat] = useState("python");
  const [pinnedTip, setPinnedTip] = useState<number | null>(null);
  const [feedLoaded, setFeedLoaded] = useState(false);
  const [feedItems, setFeedItems] = useState<FeedItem[]>([]);

  const scrollRef = useRef<HTMLDivElement>(null);
  const sentinelRef = useRef<HTMLDivElement>(null);
  const seenRef = useRef<Set<number>>(new Set(loadSeenIds()));
  const queuedToast = useRef<string | null>(null);
  const scrollDone = useRef(false);
  const scrollStateRef = useRef<Record<string, number>>(loadScrollState());
  const restoredRef = useRef(false);
  const hydratedRef = useRef(false);
  const cachedFeedCatRef = useRef<string | null>(null);

  // Hydrate persisted feed on client only (avoids server/client mismatch)
  useEffect(() => {
    const cache = loadFeedCache();
    if (cache?.tips.length && cache?.feedItems.length) {
      cachedFeedCatRef.current = cache.feedCat;
      hydratedRef.current = true;
      setTips(cache.tips);
      setFeedItems(cache.feedItems);
      setOffline(cache.offline);
      setFeedCat(cache.feedCat || "python");
      setFeedLoaded(true);
      for (const it of cache.feedItems) {
        const seq = Number(it.key.split("#")[1]);
        if (!Number.isNaN(seq) && seq > instanceSeq) instanceSeq = seq;
      }
    }
  }, []);

  useEffect(() => {
    fetchTips().then((list) => {
      if (list !== FALLBACK_TIPS && list.length > 0) {
        setOffline(false);
        setTips(list);
      } else {
        setOffline(true);
        setTips(shuffleArray(FALLBACK_TIPS));
      }
    });
  }, []);

  useEffect(() => {
    let active = true;
    (async () => {
      const params = new URLSearchParams(window.location.search);
      const target = Number(params.get("tip"));
      const meta = await getUserMeta().catch(() => null);
      if (!active) return;
      if (target) setPinnedTip(target);
      if (meta) setFeedCat(meta.feed_category || "python");
      setFeedLoaded(true);
    })();
    return () => {
      active = false;
    };
  }, []);

  const baseTips = useMemo(
    () => tips.filter((t) => feedCategoryOf(t.category) === feedCat),
    [tips, feedCat],
  );

  // ---- build the (endless) feed once tips/category are known ----
  useEffect(() => {
    if (!feedLoaded || baseTips.length === 0) return;
    // Skip rebuild only if hydrated AND category hasn't changed
    if (hydratedRef.current && feedCat === (cachedFeedCatRef.current || "python")) return;
    const saved = scrollStateRef.current[feedCat] ?? 0;
    const perBatch = Math.min(BATCH_SIZE, baseTips.length);
    const batches = Math.min(
      50,
      Math.max(INITIAL_BATCHES, Math.ceil((saved + 1) / perBatch)),
    );
    setFeedItems(
      Array.from({ length: batches }, () => buildBatch(baseTips)).flat(),
    );
  }, [baseTips, feedCat, feedLoaded]);

  // ---- persist feed so returning keeps the exact cards + scroll ----
  useEffect(() => {
    if (!feedLoaded || feedItems.length === 0) return;
    saveFeedCache({
      tips,
      feedItems: feedItems.slice(0, 200),
      offline,
      feedCat,
    });
  }, [feedItems, tips, offline, feedCat, feedLoaded]);

  // ---- append more randomized cards as the user nears the end ----
  useEffect(() => {
    const container = scrollRef.current;
    const sentinel = sentinelRef.current;
    if (!container || !sentinel || !feedLoaded || baseTips.length === 0) return;
    const io = new IntersectionObserver(
      (entries) => {
        if (entries.some((e) => e.isIntersecting)) {
          setFeedItems((prev) => {
            const next = [...prev, ...buildBatch(baseTips)];
            if (next.length > MAX_FEED_ITEMS) {
              const extra = next.length - MAX_FEED_ITEMS;
              if (container) container.scrollTop = Math.max(0, container.scrollTop - extra * (container.scrollHeight / next.length));
              return next.slice(-MAX_FEED_ITEMS);
            }
            return next;
          });
        }
      },
      { root: container, rootMargin: "120% 0px", threshold: 0 },
    );
    io.observe(sentinel);
    return () => io.disconnect();
  }, [baseTips, feedLoaded]);

  const uniqueIdsKey = useMemo(
    () =>
      [...new Set(feedItems.map((f) => f.tip.id))].sort((a, b) => a - b).join(","),
    [feedItems],
  );

  useEffect(() => {
    let active = true;
    Promise.all([getFavorites(), getReposts(), getUserMeta()])
      .then(([favList, repList]) => {
        if (!active) return;
        setFavs(new Set(favList.map((f) => f.tip_id)));
        setReposts(new Set(repList.map((r) => r.tip_id)));
        const likes: Record<number, number> = {};
        for (const f of favList) likes[f.tip_id] = (likes[f.tip_id] ?? 0) + 1;
        setLikeCounts(likes);
      })
      .catch(() => {});
    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    if (!uniqueIdsKey) return;
    let active = true;
    const ids = uniqueIdsKey.split(",").map(Number);
    Promise.all(ids.map((id) => getCommentsByTip(id)))
      .then((lists) => {
        if (!active) return;
        const counts: Record<number, number> = {};
        ids.forEach((id, i) => {
          counts[id] = lists[i].length;
        });
        setCommentCounts(counts);
      })
      .catch(() => {});
    return () => {
      active = false;
    };
  }, [uniqueIdsKey]);

  // ---- jump to a specific tip (?tip=ID) ----
  useEffect(() => {
    if (scrollDone.current) return;
    if (!pinnedTip || !feedLoaded) return;
    const target = pinnedTip;
    const container = scrollRef.current;
    const card = container?.querySelector<HTMLElement>(`[data-tip-id="${target}"]`);
    if (card && container) {
      scrollDone.current = true;
      container.scrollTo({ top: card.offsetTop, behavior: "smooth" });
      setHighlight(target);
      setTimeout(() => {
        setHighlight(null);
        setPinnedTip(null);
      }, 2200);
      history.replaceState(null, "", "/feed");
      return;
    }
    const tip = tips.find((t) => t.id === target);
    if (!tip) {
      history.replaceState(null, "", "/feed");
      const clear = setTimeout(() => setPinnedTip(null), 0);
      return () => clearTimeout(clear);
    }
    // tip exists but isn't rendered yet — inject it at the front
    setFeedItems((prev) => [{ key: nextKey(tip.id), tip }, ...prev]);
  }, [feedItems, pinnedTip, tips, feedLoaded]);

  // ---- restore saved scroll position ----
  useEffect(() => {
    if (!feedLoaded || !feedItems.length || pinnedTip || restoredRef.current) return;
    const saved = scrollStateRef.current[feedCat];
    if (saved == null) return;
    restoredRef.current = true;
    const container = scrollRef.current;
    const cards = container?.querySelectorAll<HTMLElement>("[data-tip-id]");
    if (container && cards && cards.length) {
      const idx = Math.min(Math.max(saved, 0), cards.length - 1);
      requestAnimationFrame(() => {
        container.scrollTo({ top: cards[idx].offsetTop });
      });
    }
  }, [feedItems, pinnedTip, feedCat, feedLoaded]);

  // ---- save scroll position per category ----
  useEffect(() => {
    const container = scrollRef.current;
    if (!container || !feedLoaded) return;
    let ticking = false;
    const onScroll = () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => {
        ticking = false;
        if (pinnedTip) return;
        const cards = Array.from(container.querySelectorAll<HTMLElement>("[data-tip-id]"));
        if (!cards.length) return;
        let best = 0;
        let bestDist = Infinity;
        cards.forEach((card, i) => {
          const d = Math.abs(card.offsetTop - container.scrollTop);
          if (d < bestDist) {
            bestDist = d;
            best = i;
          }
        });
        scrollStateRef.current = { ...scrollStateRef.current, [feedCat]: best };
        saveScrollState(scrollStateRef.current);
      });
    };
    container.addEventListener("scroll", onScroll, { passive: true });
    return () => container.removeEventListener("scroll", onScroll);
  }, [feedCat, feedLoaded, pinnedTip]);

  // ---- time + view tracking ----
  useEffect(() => {
    const tick = setInterval(() => {
      if (document.visibilityState !== "visible") return;
      setUserMeta((m) => ({
        time_spent_today: m.time_spent_today + 10,
        total_time: m.total_time + 10,
      })).catch(() => {});
    }, 10_000);
    const check = setInterval(() => {
      checkAchievements().then((fresh) => {
        if (fresh.length > 0) queuedToast.current = fresh[0];
      }).catch(() => {});
    }, 30_000);
    const flush = () => {
      checkAchievements().then((fresh) => {
        if (fresh.length > 0) queuedToast.current = fresh[0];
      }).catch(() => {});
    };
    window.addEventListener("pagehide", flush);
    return () => {
      clearInterval(tick);
      clearInterval(check);
      window.removeEventListener("pagehide", flush);
    };
  }, []);

  // ---- active card tracking -> views (incremental observer) ----
  const viewObserverRef = useRef<IntersectionObserver | null>(null);
  const observedElementsRef = useRef<Set<Element>>(new Set());
  const tipMapRef = useRef<Map<number, Tip>>(new Map());

  useEffect(() => {
    tipMapRef.current = new Map(feedItems.map((f) => [f.tip.id, f.tip]));
  }, [feedItems]);

  useEffect(() => {
    const container = scrollRef.current;
    if (!container || feedItems.length === 0) return;

    if (!viewObserverRef.current) {
      viewObserverRef.current = new IntersectionObserver(
        (entries) => {
          for (const entry of entries) {
            if (!entry.isIntersecting) continue;
            const id = Number((entry.target as HTMLElement).dataset.tipId);
            if (seenRef.current.has(id)) continue;
            seenRef.current.add(id);
            saveSeenIds(seenRef.current);
            const tip = tipMapRef.current.get(id);
            setUserMeta((m) => ({
              views_today: m.views_today + 1,
              views_total: m.views_total + 1,
              last_action_ts: Date.now(),
              max_tip_id_viewed: Math.max(m.max_tip_id_viewed ?? 0, id),
              viewed_categories:
                tip && !(m.viewed_categories ?? []).includes(tip.category)
                  ? [...(m.viewed_categories ?? []), tip.category]
                  : m.viewed_categories ?? [],
            }))
              .then(() => checkAchievements())
              .then((fresh) => {
                if (fresh.length > 0) {
                  queuedToast.current = fresh[0];
                  setToast(fresh[0]);
                }
              })
              .catch(() => {});
          }
        },
        { threshold: 0.6 },
      );
    }
    const io = viewObserverRef.current;
    for (const card of container.querySelectorAll<HTMLElement>("[data-tip-id]")) {
      if (!observedElementsRef.current.has(card)) {
        observedElementsRef.current.add(card);
        io.observe(card);
      }
    }
  }, [feedItems]);

  useEffect(() => {
    return () => {
      viewObserverRef.current?.disconnect();
      observedElementsRef.current.clear();
    };
  }, []);

  // ---- actions ----
  async function handleLike(tip: Tip) {
    try {
      const liked = favs.has(tip.id);
      if (liked) {
        await removeFavorite(tip.id);
        setFavs((prev) => {
          const next = new Set(prev);
          next.delete(tip.id);
          return next;
        });
        setLikeCounts((prev) => ({ ...prev, [tip.id]: Math.max(0, (prev[tip.id] ?? 1) - 1) }));
      } else {
        await addFavorite(tip.id);
        setFavs((prev) => new Set(prev).add(tip.id));
        setLikeCounts((prev) => ({ ...prev, [tip.id]: (prev[tip.id] ?? 0) + 1 }));
        const meta = await getUserMeta();
        await setUserMeta({
          likes_today: meta.likes_today + 1,
          total_likes: meta.total_likes + 1,
          last_action_ts: Date.now(),
        });
        const fresh = await checkAchievements();
        if (fresh.length > 0) {
          queuedToast.current = fresh[0];
          setToast(fresh[0]);
        }
      }
    } catch {
      // IndexedDB unavailable
    }
  }

  async function handleRepost(tip: Tip) {
    try {
      const reposted = reposts.has(tip.id);
      if (reposted) {
        await removeRepost(tip.id);
        setReposts((prev) => {
          const next = new Set(prev);
          next.delete(tip.id);
          return next;
        });
      } else {
        await addRepost(tip.id);
        setReposts((prev) => new Set(prev).add(tip.id));
        await setUserMeta({ last_action_ts: Date.now() }).catch(() => {});
        const fresh = await checkAchievements();
        if (fresh.length > 0) {
          queuedToast.current = fresh[0];
          setToast(fresh[0]);
        }
      }
    } catch {
      // IndexedDB unavailable
    }
  }

  function handleToastDone() {
    setToast(null);
    if (queuedToast.current) {
      setToast(queuedToast.current);
      queuedToast.current = null;
    }
  }

  return (
    <main className="relative h-full bg-bg">
      <div
        ref={scrollRef}
        className="mx-auto h-full w-full max-w-3xl overflow-y-scroll snap-y snap-mandatory no-scrollbar"
      >
        {!feedLoaded && (
          <div className="flex h-[60vh] flex-col items-center justify-center gap-4 px-8 text-center">
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-accentsoft">
              <div className="flex h-6 w-6 items-center justify-center">
                <PythonLogo className="h-6 w-6" icon />
              </div>
            </div>
            <div className="flex gap-1">
              <span className="typing-dot h-2 w-2 rounded-full bg-accent" style={{ animationDelay: "0s" }} />
              <span className="typing-dot h-2 w-2 rounded-full bg-accent" style={{ animationDelay: "0.15s" }} />
              <span className="typing-dot h-2 w-2 rounded-full bg-accent" style={{ animationDelay: "0.3s" }} />
            </div>
            <p className="text-sm text-muted">Loading tips…</p>
          </div>
        )}

        {feedLoaded && feedItems.map(({ key, tip }) => (
          <TipCard
            key={key}
            tip={tip}
            liked={favs.has(tip.id)}
            reposted={reposts.has(tip.id)}
            likeCount={likeCounts[tip.id] ?? 0}
            commentCount={commentCounts[tip.id] ?? 0}
            highlighted={highlight === tip.id}
            onLike={handleLike}
            onComment={(t) => setCommentFor(t)}
            onRepost={handleRepost}
          />
        ))}

        {feedLoaded && <div ref={sentinelRef} aria-hidden="true" className="h-px w-full shrink-0" />}

        {feedLoaded && feedItems.length === 0 && !pinnedTip && (
          <div className="flex h-[70vh] flex-col items-center justify-center gap-5 px-8 text-center">
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
              className="flex h-16 w-16 items-center justify-center rounded-2xl border border-line/50 bg-bgsoft"
            >
              <Compass className="h-8 w-8 text-muted/60" strokeWidth={1.5} />
            </motion.div>
            <motion.div
              initial={{ y: 10, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.1, duration: 0.4 }}
            >
              <p className="text-base font-medium text-fg">No {feedLabel(feedCat)} cards yet</p>
              <p className="mt-2 max-w-xs text-sm leading-6 text-muted/70">
                This feed is empty right now. Pick another category under Customize your feed in
                Settings — more cards are on the way.
              </p>
            </motion.div>
          </div>
        )}
      </div>

      {offline && (
        <div className="absolute left-0 right-0 top-4 z-30 flex justify-center px-4">
          <div className="flex items-center gap-2 rounded-full border border-line/50 bg-bgro/80 px-3 py-1.5 text-[11px] text-muted backdrop-blur-md">
            <PythonLogo className="h-4 w-4" icon />
            backend offline — showing built-in tips
          </div>
        </div>
      )}

      <CommentSheet
        key={commentFor?.id ?? "closed"}
        tip={commentFor}
        onClose={() => setCommentFor(null)}
        onFreshAchievement={(name) => {
          queuedToast.current = name;
          setToast(name);
        }}
        onCountChange={(tipId, count) =>
          setCommentCounts((prev) => ({ ...prev, [tipId]: count }))
        }
      />

      <AchievementToast unlockId={toast} onDone={handleToastDone} />
    </main>
  );
}