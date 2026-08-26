import {
  AlarmClock,
  Award,
  BadgeCheck,
  Bell,
  Binoculars,
  Bird,
  BookMarked,
  BookOpen,
  Bot,
  Brain,
  Bug,
  Cake,
  CalendarDays,
  CircleSlash,
  Clock,
  Coffee,
  Compass,
  Crown,
  CupSoda,
  Database,
  Eye,
  Feather,
  Flag,
  Flame,
  FlaskConical,
  Footprints,
  FolderOpen,
  FunctionSquare,
  Gamepad2,
  Gauge,
  Gem,
  Globe,
  Globe2,
  GraduationCap,
  Grid3x3,
  Handshake,
  Heart,
  Hourglass,
  Joystick,
  Landmark,
  Layers,
  Library,
  List,
  Magnet,
  Map as MapIcon,
  Medal,
  Megaphone,
  MessageCircle,
  MessageCircleQuestion,
  MessagesSquare,
  Mic,
  Microscope,
  Milestone,
  Moon,
  MoonStar,
  Mountain,
  NotebookPen,
  Orbit,
  Puzzle,
  Radio,
  RefreshCcw,
  RefreshCw,
  Rocket,
  Rss,
  Route,
  Satellite,
  Scroll,
  ScrollText,
  Share,
  Space,
  Sparkle,
  Sparkles,
  Sprout,
  SquareTerminal,
  Star,
  Stars,
  Sun,
  Sunrise,
  Sunset,
  Target,
  Telescope,
  Timer,
  Tornado,
  TrafficCone,
  Trophy,
  Tv,
  Umbrella,
  WandSparkles,
  Waves,
  Wrench,
  Zap,
  type LucideIcon,
} from "lucide-react";
import { fetchTips } from "./api";
import {
  countAllComments,
  countChatUserMessages,
  countCommentsToday,
  countRepostsToday,
  getAchievements,
  getAllComments,
  getChatHistory,
  getCommentedTipIds,
  getFavoriteTipIds,
  getFavorites,
  getLongestCommentLength,
  getRepostTipIds,
  getReposts,
  getUserMeta,
  todayStr,
  unlockAchievement,
} from "./db";

export interface AchievementDef {
  id: string;
  Icon: LucideIcon;
  name: string;
  description: string;
  check: () => Promise<boolean>;
}

type Meta = Awaited<ReturnType<typeof getUserMeta>>;
type MetaNum = (m: Meta) => number;

function fromMeta(
  prefix: string,
  tierDefs: [number, string, LucideIcon][],
  getter: MetaNum,
  describe: (n: number) => string,
): AchievementDef[] {
  return tierDefs.map(([threshold, name, Icon]) => ({
    id: `${prefix}_${threshold}`,
    Icon,
    name,
    description: describe(threshold),
    check: () =>
      getUserMeta()
        .then((m) => getter(m) >= threshold)
        .catch(() => false),
  }));
}

function fromCount(
  prefix: string,
  tierDefs: [number, string, LucideIcon][],
  getter: () => Promise<number>,
  describe: (n: number) => string,
): AchievementDef[] {
  return tierDefs.map(([threshold, name, Icon]) => ({
    id: `${prefix}_${threshold}`,
    Icon,
    name,
    description: describe(threshold),
    check: () => getter().then((v) => v >= threshold).catch(() => false),
  }));
}

function atLeast(getter: () => Promise<number>, n: number): () => Promise<boolean> {
  return () => getter().then((v) => v >= n).catch(() => false);
}

function intersection(a: () => Promise<number[]>, b: () => Promise<number[]>) {
  return () => Promise.all([a(), b()]).then(([x, y]) => x.some((id) => y.includes(id)));
}

function hourOfLastAction(m: Meta): number {
  if (!m.last_action_ts) return -1;
  return new Date(m.last_action_ts).getHours();
}

async function distinctActiveDays(): Promise<number> {
  try {
    const [favs, reps, comments, chat] = await Promise.all([
      getFavorites(),
      getReposts(),
      getAllComments(),
      getChatHistory(),
    ]);
    const stamps = [
      ...favs.map((f) => f.timestamp),
      ...reps.map((r) => r.timestamp),
      ...comments.map((c) => c.timestamp),
      ...chat.map((c) => c.timestamp),
    ];
    const days = new Set(stamps.map((t) => new Date(t).toDateString()));
    return days.size;
  } catch {
    return 0;
  }
}

async function activityDayTypes(): Promise<Set<number>> {
  try {
    const [favs, reps, comments, chat] = await Promise.all([
      getFavorites(),
      getReposts(),
      getAllComments(),
      getChatHistory(),
    ]);
    const stamps = [
      ...favs.map((f) => f.timestamp),
      ...reps.map((r) => r.timestamp),
      ...comments.map((c) => c.timestamp),
      ...chat.map((c) => c.timestamp),
    ];
    return new Set(stamps.map((t) => new Date(t).getDay()));
  } catch {
    return new Set();
  }
}

async function weekendBothDays(): Promise<boolean> {
  const days = await activityDayTypes();
  return days.has(0) && days.has(6);
}

async function activeInAllWeekdays(): Promise<boolean> {
  const days = await activityDayTypes();
  return [1, 2, 3, 4, 5].every((d) => days.has(d));
}

async function morningWeekday(): Promise<boolean> {
  try {
    const [favs, reps, comments, chat] = await Promise.all([
      getFavorites(),
      getReposts(),
      getAllComments(),
      getChatHistory(),
    ]);
    const stamps = [
      ...favs.map((f) => f.timestamp),
      ...reps.map((r) => r.timestamp),
      ...comments.map((c) => c.timestamp),
      ...chat.map((c) => c.timestamp),
    ];
    return stamps.some((t) => {
      const d = new Date(t);
      const day = d.getDay();
      return day >= 1 && day <= 5 && d.getHours() < 9;
    });
  } catch {
    return false;
  }
}

function hourAnyDay(from: number, to: number): () => Promise<boolean> {
  return async () => {
    try {
      const [favs, reps, comments, chat] = await Promise.all([
        getFavorites(),
        getReposts(),
        getAllComments(),
        getChatHistory(),
      ]);
      const stamps = [
        ...favs.map((f) => f.timestamp),
        ...reps.map((r) => r.timestamp),
        ...comments.map((c) => c.timestamp),
        ...chat.map((c) => c.timestamp),
      ];
      return stamps.some((t) => {
        const h = new Date(t).getHours();
        return h >= from && h < to;
      });
    } catch {
      return false;
    }
  };
}

async function favoriteCats(): Promise<boolean> {
  try {
    const [ids, tips] = await Promise.all([getFavoriteTipIds(), fetchTips()]);
    const catOf = new Map(tips.map((t) => [t.id, t.category]));
    const cats = new Set(ids.map((id) => catOf.get(id)).filter(Boolean));
    return cats.size >= 8;
  } catch {
    return false;
  }
}

async function longestChatRun(): Promise<number> {
  try {
    const chat = await getChatHistory();
    const sorted = chat.map((m) => m.timestamp).sort((a, b) => a - b);
    let best = 0;
    let run = 0;
    let prev = 0;
    for (const ts of sorted) {
      run = run === 0 || ts - prev <= 30 * 60 * 1000 ? run + 1 : 1;
      if (run > best) best = run;
      prev = ts;
    }
    return best;
  } catch {
    return 0;
  }
}

async function chatWithCode(): Promise<boolean> {
  try {
    const chat = await getChatHistory();
    return chat.some(
      (m) =>
        m.role === "user" &&
        (m.content.includes("def ") ||
          m.content.includes("```") ||
          m.content.includes("import ")),
    );
  } catch {
    return false;
  }
}

async function tutorMorning(): Promise<boolean> {
  try {
    const chat = await getChatHistory();
    return chat.some((m) => m.role === "user" && new Date(m.timestamp).getHours() < 8);
  } catch {
    return false;
  }
}

async function longestChatUserMessage(): Promise<number> {
  try {
    const chat = await getChatHistory();
    return chat.reduce((max, m) => (m.role === "user" ? Math.max(max, m.content.length) : max), 0);
  } catch {
    return 0;
  }
}

async function dataConsumer(): Promise<boolean> {
  const m = await getUserMeta();
  return m.views_total >= 30 && m.total_likes === 0;
}

async function repostsOnWeekend(): Promise<boolean> {
  try {
    const reps = await getReposts();
    return reps.some((r) => {
      const day = new Date(r.timestamp).getDay();
      return day === 0 || day === 6;
    });
  } catch {
    return false;
  }
}

async function routeMaster(): Promise<boolean> {
  try {
    const [meta, tips] = await Promise.all([getUserMeta(), fetchTips()]);
    if (!meta.viewed_categories?.length) return false;
    const all = new Set(tips.map((t) => t.category));
    return Array.from(all).every((c) => meta.viewed_categories.includes(c));
  } catch {
    return false;
  }
}

async function threeDayParts(): Promise<boolean> {
  try {
    const [favs, reps, comments, chat] = await Promise.all([
      getFavorites(),
      getReposts(),
      getAllComments(),
      getChatHistory(),
    ]);
    const stamps = [
      ...favs.map((f) => f.timestamp),
      ...reps.map((r) => r.timestamp),
      ...comments.map((c) => c.timestamp),
      ...chat.map((c) => c.timestamp),
    ];
    const parts = new Set(
      stamps.map((t) => {
        const h = new Date(t).getHours();
        return h < 5 ? 0 : h < 12 ? 1 : h < 17 ? 2 : 3;
      }),
    );
    return parts.size >= 3;
  } catch {
    return false;
  }
}

async function chatActiveDays(): Promise<number> {
  try {
    const chat = await getChatHistory();
    const days = new Set(
      chat
        .filter((m) => m.role === "user")
        .map((m) => new Date(m.timestamp).toDateString()),
    );
    return days.size;
  } catch {
    return 0;
  }
}

async function countTutorReplies(): Promise<number> {
  try {
    const chat = await getChatHistory();
    return chat.filter((m) => m.role === "assistant").length;
  } catch {
    return 0;
  }
}

async function chatAboutErrors(): Promise<boolean> {
  try {
    const chat = await getChatHistory();
    const mentions = chat.filter(
      (m) =>
        m.role === "user" &&
        /error|exception|traceback|bug/i.test(m.content),
    ).length;
    return mentions >= 3;
  } catch {
    return false;
  }
}

async function nightWeekend(): Promise<boolean> {
  try {
    const [favs, reps, comments, chat] = await Promise.all([
      getFavorites(),
      getReposts(),
      getAllComments(),
      getChatHistory(),
    ]);
    const stamps = [
      ...favs.map((f) => f.timestamp),
      ...reps.map((r) => r.timestamp),
      ...comments.map((c) => c.timestamp),
      ...chat.map((c) => c.timestamp),
    ];
    return stamps.some((t) => {
      const d = new Date(t);
      const day = d.getDay();
      return (day === 0 || day === 6) && (d.getHours() >= 21 || d.getHours() < 1);
    });
  } catch {
    return false;
  }
}

async function weekendMorning(): Promise<boolean> {
  try {
    const [favs, reps, comments, chat] = await Promise.all([
      getFavorites(),
      getReposts(),
      getAllComments(),
      getChatHistory(),
    ]);
    const stamps = [
      ...favs.map((f) => f.timestamp),
      ...reps.map((r) => r.timestamp),
      ...comments.map((c) => c.timestamp),
      ...chat.map((c) => c.timestamp),
    ];
    return stamps.some((t) => {
      const d = new Date(t);
      const day = d.getDay();
      return (day === 0 || day === 6) && d.getHours() < 8;
    });
  } catch {
    return false;
  }
}

async function longestDayStreak(): Promise<number> {
  try {
    const chat = await getChatHistory();
    const now = Date.now();
    const stamps = [
      ...(await getFavorites()).map((f) => f.timestamp),
      ...(await getReposts()).map((r) => r.timestamp),
      ...(await getAllComments()).map((c) => c.timestamp),
      ...chat.map((c) => c.timestamp),
      now,
    ];
    const days = Array.from(
      new Set(stamps.map((t) => new Date(t).toDateString())),
    );
    const timestamps = new Set(
      stamps.map((t) => new Date(t).setHours(0, 0, 0, 0)),
    );
    let best = 0;
    let run = 0;
    for (const day of days) {
      const midnight = new Date(day).getTime();
      if (timestamps.has(midnight - 24 * 60 * 60 * 1000)) {
        run += 1;
      } else {
        run = 1;
      }
      if (run > best) best = run;
    }
    return best;
  } catch {
    return 0;
  }
}

async function commentCats(): Promise<number> {
  try {
    const [ids, tips] = await Promise.all([getCommentedTipIds(), fetchTips()]);
    const catOf = new Map(tips.map((t) => [t.id, t.category]));
    return new Set(ids.map((id) => catOf.get(id)).filter(Boolean)).size;
  } catch {
    return 0;
  }
}

/* ── helpers for harder achievements ── */

async function longestChatSession(): Promise<number> {
  try {
    const chat = await getChatHistory();
    const sorted = chat.map((m) => m.timestamp).sort((a, b) => a - b);
    let best = 0;
    let run = 0;
    let prev = 0;
    for (const ts of sorted) {
      run = run === 0 || ts - prev <= 30 * 60 * 1000 ? run + 1 : 1;
      if (run > best) best = run;
      prev = ts;
    }
    return best;
  } catch {
    return 0;
  }
}

async function playgroundRunsToday(): Promise<number> {
  try {
    const m = await getUserMeta();
    const today = todayStr();
    if (m.last_active_date !== today) return 0;
    return m.playground_runs;
  } catch {
    return 0;
  }
}

async function allCategoriesFavorited(): Promise<boolean> {
  try {
    const [ids, tips] = await Promise.all([getFavoriteTipIds(), fetchTips()]);
    const allCats = new Set(tips.map((t) => t.category));
    const favCats = new Set(ids.map((id) => tips.find((t) => t.id === id)?.category).filter(Boolean));
    return allCats.size > 0 && favCats.size === allCats.size;
  } catch {
    return false;
  }
}

async function commentedAllCategories(): Promise<boolean> {
  try {
    const [ids, tips] = await Promise.all([getCommentedTipIds(), fetchTips()]);
    const allCats = new Set(tips.map((t) => t.category));
    const commentCats = new Set(ids.map((id) => tips.find((t) => t.id === id)?.category).filter(Boolean));
    return allCats.size > 0 && commentCats.size === allCats.size;
  } catch {
    return false;
  }
}

async function allSevenDaysActive(): Promise<boolean> {
  const days = await activityDayTypes();
  return [0, 1, 2, 3, 4, 5, 6].every((d) => days.has(d));
}

async function errorExpert(): Promise<boolean> {
  try {
    const chat = await getChatHistory();
    const mentions = chat.filter(
      (m) =>
        m.role === "user" &&
        /error|exception|traceback|bug/i.test(m.content),
    ).length;
    return mentions >= 10;
  } catch {
    return false;
  }
}

async function tutor50Session(): Promise<boolean> {
  try {
    const chat = await getChatHistory();
    const sorted = chat.map((m) => m.timestamp).sort((a, b) => a - b);
    let run = 0;
    let prev = 0;
    for (const ts of sorted) {
      run = run === 0 || ts - prev <= 30 * 60 * 1000 ? run + 1 : 1;
      if (run >= 50) return true;
      prev = ts;
    }
    return false;
  } catch {
    return false;
  }
}

async function unlockedCount(): Promise<number> {
  try {
    const all = await getAchievements();
    return all.length;
  } catch {
    return 0;
  }
}

async function longCommentCount(): Promise<number> {
  try {
    const comments = await getAllComments();
    return comments.filter((c) => c.comment_text.length >= 100).length;
  } catch {
    return 0;
  }
}

async function chatActiveDaysCount(): Promise<number> {
  try {
    const chat = await getChatHistory();
    const days = new Set(
      chat
        .filter((m) => m.role === "user")
        .map((m) => new Date(m.timestamp).toDateString()),
    );
    return days.size;
  } catch {
    return 0;
  }
}

async function socialTrifecta(): Promise<boolean> {
  try {
    const [favIds, repIds, comIds] = await Promise.all([
      getFavoriteTipIds(),
      getRepostTipIds(),
      getCommentedTipIds(),
    ]);
    return favIds.some((id) => repIds.includes(id) && comIds.includes(id));
  } catch {
    return false;
  }
}

async function repostAllCategories(): Promise<boolean> {
  try {
    const [ids, tips] = await Promise.all([getRepostTipIds(), fetchTips()]);
    const allCats = new Set(tips.map((t) => t.category));
    const repCats = new Set(ids.map((id) => tips.find((t) => t.id === id)?.category).filter(Boolean));
    return allCats.size > 0 && repCats.size === allCats.size;
  } catch {
    return false;
  }
}

export const ACHIEVEMENTS: AchievementDef[] = [
  // ---- original nine ----
  {
    id: "first_like",
    Icon: Heart,
    name: "First Like",
    description: "Liked your first tip.",
    check: atLeast(() => getUserMeta().then((m) => m.total_likes), 1),
  },
  {
    id: "liker_10",
    Icon: Flame,
    name: "Fire Streak",
    description: "Liked 10 posts in a day.",
    check: atLeast(() => getUserMeta().then((m) => m.likes_today), 10),
  },
  {
    id: "first_comment",
    Icon: MessageCircle,
    name: "Joined the Conversation",
    description: "Left your first comment.",
    check: atLeast(countAllComments, 1),
  },
  {
    id: "reposter_5",
    Icon: RefreshCcw,
    name: "Cycle Master",
    description: "Reposted 5 tips.",
    check: atLeast(() => getUserMeta().then((m) => m.total_reposts), 5),
  },
  {
    id: "scroller_30",
    Icon: Timer,
    name: "Deep End",
    description: "Doomscrolled 30 minutes in a day.",
    check: atLeast(() => getUserMeta().then((m) => m.time_spent_today), 30 * 60),
  },
  {
    id: "marathon_1h",
    Icon: Footprints,
    name: "Marathon Payer",
    description: "Spent a total of 1 hour in the app.",
    check: atLeast(() => getUserMeta().then((m) => m.total_time), 60 * 60),
  },
  {
    id: "tutor_1",
    Icon: Bot,
    name: "Tutor Session",
    description: "Asked the AI tutor a question.",
    check: atLeast(countChatUserMessages, 1),
  },
  {
    id: "explorer_10",
    Icon: Globe,
    name: "Explorer",
    description: "Viewed 10 different tips in a day.",
    check: atLeast(() => getUserMeta().then((m) => m.views_today), 10),
  },
  {
    id: "all_seen",
    Icon: Brain,
    name: "Knowledge Seeker",
    description: "Viewed 60 tips.",
    check: atLeast(() => getUserMeta().then((m) => m.views_total), 60),
  },

  // ---- like milestones ----
  ...fromMeta(
    "likes_total",
    [
      [10, "Tenfold", Heart],
      [25, "Blue Streak", Heart],
      [50, "Green Thumb", Heart],
      [100, "Purple Passion", Heart],
      [250, "Crowned", Crown],
      [500, "Heart Legend", Trophy],
      [1000, "Heart Tycoon", Award],
    ],
    (m) => m.total_likes,
    (n) => `Liked ${n} tips in total.`,
  ),
  ...fromCount(
    "likes_distinct",
    [
      [5, "Fickle Follower", Heart],
      [25, "Casanova", Heart],
      [50, "Collector", Gem],
      [100, "Curator", Library],
    ],
    () => getFavoriteTipIds().then((ids) => ids.length),
    (n) => `Favorited ${n} different tips.`,
  ),
  ...fromMeta(
    "likes_today",
    [
      [5, "Quick Trigger", Zap],
      [25, "Meteor Shower", Star],
      [50, "Jackpot", Gem],
    ],
    (m) => m.likes_today,
    (n) => `Liked ${n} tips in a single day.`,
  ),

  // ---- repost milestones ----
  ...fromMeta(
    "reposts_total",
    [
      [1, "First Echo", Target],
      [10, "Empty Store", RefreshCw],
      [25, "Magnet", Magnet],
      [50, "Pure Cycle", Tornado],
      [100, "Broadcaster", Radio],
      [250, "Signal Tower", Satellite],
    ],
    (m) => m.total_reposts,
    (n) => `Reposted ${n} tips in total.`,
  ),
  ...fromCount(
    "reposts_today",
    [[3, "Syndicator", Satellite], [10, "Rush Hour", Grid3x3]],
    countRepostsToday,
    (n) => `Reposted ${n} tips in a single day.`,
  ),
  {
    id: "double_down",
    Icon: Handshake,
    name: "Double Down",
    description: "Liked a tip you also reposted.",
    check: intersection(getFavoriteTipIds, getRepostTipIds),
  },
  {
    id: "full_circle",
    Icon: Heart,
    name: "Full Circle",
    description: "Commented on a tip you favorited.",
    check: intersection(getFavoriteTipIds, getCommentedTipIds),
  },
  {
    id: "trusted_circle",
    Icon: Sparkles,
    name: "Circle of Trust",
    description: "Commented on a tip you reposted.",
    check: intersection(getRepostTipIds, getCommentedTipIds),
  },

  // ---- comment milestones ----
  ...fromCount(
    "comments_total",
    [
      [5, "Chatty", MessagesSquare],
      [10, "Opinionated", Megaphone],
      [25, "Amplifier", Mic],
      [50, "Town Square", Landmark],
      [100, "Town Crier", List],
    ],
    countAllComments,
    (n) => `Posted ${n} comments in total.`,
  ),
  ...fromCount(
    "comments_today",
    [[5, "Daily Pundit", Waves], [15, "Comment Storm", Feather]],
    countCommentsToday,
    (n) => `Posted ${n} comments in a single day.`,
  ),
  {
    id: "essayist",
    Icon: ScrollText,
    name: "Essayist",
    description: "Wrote a comment of 100+ characters.",
    check: atLeast(getLongestCommentLength, 100),
  },

  // ---- tutor milestones ----
  ...fromCount(
    "tutor",
    [
      [3, "Curious", MessageCircleQuestion],
      [10, "Apprentice", FlaskConical],
      [25, "Sage", WandSparkles],
      [50, "Oracle", Sparkle],
      [100, "Professor", GraduationCap],
      [250, "Eminence", Medal],
    ],
    countChatUserMessages,
    (n) => `Asked the AI tutor ${n} questions.`,
  ),

  // ---- time milestones ----
  ...fromMeta(
    "time_today",
    [
      [15 * 60, "Warmed Up", Hourglass],
      [60 * 60, "One-Hour Mark", Clock],
      [3 * 60 * 60, "The Void", CircleSlash],
      [5 * 60 * 60, "The Abyss", AlarmClock],
      [8 * 60 * 60, "Sunk Cost", Mountain],
    ],
    (m) => m.time_spent_today,
    (n) => `Doomscrolled ${Math.round(n / 60)} minutes in a day.`,
  ),
  ...fromMeta(
    "total_time",
    [
      [3 * 60 * 60, "Waning Gibbous", Moon],
      [6 * 60 * 60, "Half Moon", MoonStar],
      [12 * 60 * 60, "Full Moon", Sparkles],
      [24 * 60 * 60, "Orbital", Orbit],
      [48 * 60 * 60, "Weekend of Python", Tv],
    ],
    (m) => m.total_time,
    (n) => `Spent ${Math.round(n / 3600)} hours in the app in total.`,
  ),

  // ---- scrolling milestones ----
  ...fromMeta(
    "views_today",
    [
      [5, "Peeking", Eye],
      [60, "Glutton", Microscope],
      [150, "Marathon Reader", Binoculars],
    ],
    (m) => m.views_today,
    (n) => `Viewed ${n} tips in a single day.`,
  ),
  ...fromMeta(
    "views_total",
    [
      [120, "Cartographer", MapIcon],
      [300, "Rocket Ride", Rocket],
      [600, "Stardust", Space],
      [1000, "Deep Space", Telescope],
    ],
    (m) => m.views_total,
    (n) => `Viewed ${n} tips in total.`,
  ),
  {
    id: "sprout",
    Icon: Sprout,
    name: "The Sprout",
    description: "Viewed the first 5 tips of the feed.",
    check: atLeast(() => getUserMeta().then((m) => m.views_total), 5),
  },
  {
    id: "finish_line",
    Icon: Flag,
    name: "The Finish Line",
    description: "Reached the very end of the feed.",
    check: () => getUserMeta().then((m) => m.max_tip_id_viewed >= 120).catch(() => false),
  },

  // ---- category mastery ----
  ...fromMeta(
    "categories",
    [
      [1, "First Chapter", BookOpen],
      [4, "Bookworm", BookMarked],
      [8, "Archivist", FolderOpen],
      [12, "Globe Trotter", Globe2],
      [18, "Renaissance Reader", Compass],
      [22, "Completionist", Puzzle],
    ],
    (m) => m.viewed_categories?.length ?? 0,
    (n) => `Explored ${n} different categories.`,
  ),

  // ---- clock moments ----
  {
    id: "night_owl",
    Icon: Moon,
    name: "Night Owl",
    description: "Used PyScroll between midnight and 5 AM.",
    check: () =>
      getUserMeta()
        .then((m) => {
          const h = hourOfLastAction(m);
          return h >= 0 && h < 5;
        })
        .catch(() => false),
  },
  {
    id: "early_bird",
    Icon: Bird,
    name: "Early Bird",
    description: "Used PyScroll before 9 AM.",
    check: () =>
      getUserMeta()
        .then((m) => {
          const h = hourOfLastAction(m);
          return h >= 5 && h < 9;
        })
        .catch(() => false),
  },
  {
    id: "golden_hour",
    Icon: Sunset,
    name: "Golden Hour",
    description: "Cleared the feed during sunset hours.",
    check: () =>
      getUserMeta()
        .then((m) => {
          const h = hourOfLastAction(m);
          return h >= 17 && h < 19;
        })
        .catch(() => false),
  },

  // ---- streaks & daily rituals ----
  {
    id: "daily_visit_3",
    Icon: CalendarDays,
    name: "Three-Day Habit",
    description: "Used PyScroll on 3 different calendar days.",
    check: atLeast(distinctActiveDays, 3),
  },
  {
    id: "daily_visit_7",
    Icon: CalendarDays,
    name: "Week of Python",
    description: "Used PyScroll on 7 different calendar days.",
    check: atLeast(distinctActiveDays, 7),
  },
  {
    id: "daily_visit_14",
    Icon: Milestone,
    name: "Fortnight of Focus",
    description: "Used PyScroll on 14 different calendar days.",
    check: atLeast(distinctActiveDays, 14),
  },
  {
    id: "daily_visit_30",
    Icon: Cake,
    name: "Monthly Devotion",
    description: "Used PyScroll on 30 different calendar days.",
    check: atLeast(distinctActiveDays, 30),
  },
  {
    id: "daily_visit_90",
    Icon: CalendarDays,
    name: "Quarter Century",
    description: "Used PyScroll on 90 different calendar days.",
    check: atLeast(distinctActiveDays, 90),
  },
  {
    id: "weekend_warrior",
    Icon: Sun,
    name: "Weekend Warrior",
    description: "Was active on both Saturday and Sunday.",
    check: weekendBothDays,
  },
  {
    id: "commuter",
    Icon: Coffee,
    name: "Commuter Coder",
    description: "Was active before 9 AM on a weekday.",
    check: morningWeekday,
  },
  {
    id: "happy_hour",
    Icon: CupSoda,
    name: "Happy Hour Hacker",
    description: "Coded right after work hours.",
    check: hourAnyDay(17, 19),
  },
  {
    id: "owl_late",
    Icon: Moon,
    name: "Past Midnight",
    description: "Did something past midnight into a new day.",
    check: hourAnyDay(0, 2),
  },

  // ---- content interaction deep dives ----
  {
    id: "work_week",
    Icon: CalendarDays,
    name: "Nine-to-Fiver",
    description: "Was active on all five weekdays.",
    check: activeInAllWeekdays,
  },
  {
    id: "favorite_cats",
    Icon: Stars,
    name: "Category Connoisseur",
    description: "Favorited tips from 8 different categories.",
    check: favoriteCats,
  },
  {
    id: "repost_weekend",
    Icon: Umbrella,
    name: "Weekend Binge",
    description: "Reposted a tip on a weekend day.",
    check: repostsOnWeekend,
  },
  {
    id: "topic_spread",
    Icon: Share,
    name: "Topic Spreader",
    description: "Commented on 10 different tips.",
    check: atLeast(() => getCommentedTipIds().then((ids) => ids.length), 10),
  },
  {
    id: "novelist_500",
    Icon: Feather,
    name: "Novelist",
    description: "Wrote a comment of 500+ characters.",
    check: atLeast(getLongestCommentLength, 500),
  },
  {
    id: "chat_10",
    Icon: Rss,
    name: "Deep Conversation",
    description: "Had a chat session of 10+ messages.",
    check: atLeast(longestChatRun, 10),
  },
  {
    id: "chat_code",
    Icon: Wrench,
    name: "Code Whisperer",
    description: "Asked the tutor a question containing code.",
    check: chatWithCode,
  },
  {
    id: "tutor_early",
    Icon: Sunrise,
    name: "Morning Study",
    description: "Asked the tutor a question before 8 AM.",
    check: tutorMorning,
  },
  {
    id: "grammar_lord",
    Icon: NotebookPen,
    name: "Spellweaver",
    description: "Asked the tutor a 300+ character question.",
    check: atLeast(longestChatUserMessage, 300),
  },
  {
    id: "no_like_week",
    Icon: Database,
    name: "Data Consumer",
    description: "Viewed 30 tips without liking any of them.",
    check: dataConsumer,
  },
  {
    id: "route_master",
    Icon: Route,
    name: "Route Master",
    description: "Viewed a tip in every single category.",
    check: routeMaster,
  },
  {
    id: "sun_rider",
    Icon: Sun,
    name: "Sun Rider",
    description: "Was active during three different day parts.",
    check: threeDayParts,
  },
  {
    id: "tutor_3_days",
    Icon: Bell,
    name: "Study Routine",
    description: "Asked the tutor questions on 3 different days.",
    check: atLeast(chatActiveDays, 3),
  },
  {
    id: "handled_10",
    Icon: BadgeCheck,
    name: "Documented",
    description: "Received 10 answers from the AI tutor.",
    check: atLeast(countTutorReplies, 10),
  },
  {
    id: "error_hunter",
    Icon: Bug,
    name: "Bug Hunter",
    description: "Asked the tutor 3 questions mentioning errors.",
    check: chatAboutErrors,
  },
  {
    id: "night_weekend",
    Icon: MoonStar,
    name: "Weekend Night Shift",
    description: "Was active late on a weekend night.",
    check: nightWeekend,
  },
  {
    id: "weekend_morning",
    Icon: Scroll,
    name: "Sunday Reset",
    description: "Was active on a weekend morning before 8 AM.",
    check: weekendMorning,
  },
  {
    id: "streak_7",
    Icon: Flame,
    name: "Unbroken Week",
    description: "Used PyScroll on 7 consecutive calendar days.",
    check: atLeast(longestDayStreak, 7),
  },
  {
    id: "comment_3_cats",
    Icon: Globe2,
    name: "Polyglot",
    description: "Commented in 3 different categories.",
    check: atLeast(commentCats, 3),
  },
  {
    id: "here_today",
    Icon: CalendarDays,
    name: "Here Today",
    description: "Opened PyScroll today.",
    check: () => getUserMeta().then((m) => m.last_active_date === todayStr()).catch(() => false),
  },
  {
    id: "whole_library",
    Icon: BookMarked,
    name: "Librarian",
    description: "Viewed a tip in the entire library of 920.",
    check: () => getUserMeta().then((m) => m.max_tip_id_viewed >= 920).catch(() => false),
  },

  // ---- daily streak milestones ----
  ...fromMeta(
    "daystreak",
    [
      [2, "Back for More", Flame],
      [3, "Hat Trick", Flame],
      [5, "Five-Alarm Python", Flame],
      [7, "Week on Fire", Flame],
      [10, "Double-Digit Burn", Zap],
      [14, "Fortnight Blaze", CalendarDays],
      [21, "Habit Forged", RefreshCw],
      [30, "Month Ablaze", Cake],
      [60, "Eternal Inferno", Sparkles],
      [100, "Centurion of Embers", Crown],
    ],
    (m) => m.current_streak ?? 0,
    (n) => `Kept your daily streak alive for ${n} days in a row.`,
  ),

  // ---- playground ----
  ...fromMeta(
    "playground",
    [
      [1, "Ignition", TrafficCone],
      [10, "Tinkerer", Gamepad2],
      [50, "Mad Scientist", Joystick],
      [100, "Compiler", SquareTerminal],
      [250, "Automation Engineer", FunctionSquare],
      [500, "Terminal Wizard", Gauge],
      [1000, "Machine Whisperer", Layers],
    ],
    (m) => m.playground_runs,
    (n) => `Ran Python ${n} times in the playground.`,
  ),

  // ---- harder achievements ----
  {
    id: "social_trifecta",
    Icon: Trophy,
    name: "Social Trifecta",
    description: "Liked, reposted, AND commented on the same tip.",
    check: socialTrifecta,
  },
  {
    id: "prolific_writer",
    Icon: Feather,
    name: "Prolific Writer",
    description: "Wrote 50 comments in total.",
    check: atLeast(countAllComments, 50),
  },
  {
    id: "essay_collector",
    Icon: ScrollText,
    name: "Essay Collector",
    description: "Wrote 5 comments that are 100+ characters each.",
    check: atLeast(longCommentCount, 5),
  },
  {
    id: "marathon_chat",
    Icon: MessagesSquare,
    name: "Marathon Chat",
    description: "Had a single chat session of 25+ messages.",
    check: atLeast(longestChatSession, 25),
  },
  {
    id: "tutor_50_session",
    Icon: GraduationCap,
    name: "Marathon Tutor",
    description: "Had a single chat session of 50+ messages.",
    check: tutor50Session,
  },
  {
    id: "error_expert",
    Icon: Bug,
    name: "Error Expert",
    description: "Asked the tutor 10 questions mentioning errors.",
    check: errorExpert,
  },
  {
    id: "week_7_active",
    Icon: CalendarDays,
    name: "Every Single Day",
    description: "Was active on all 7 days of the week.",
    check: allSevenDaysActive,
  },
  {
    id: "category_completionist",
    Icon: Puzzle,
    name: "Category Completionist",
    description: "Favorited at least one tip in every category.",
    check: allCategoriesFavorited,
  },
  {
    id: "comment_completionist",
    Icon: MessageCircle,
    name: "Comment Completionist",
    description: "Commented in every category.",
    check: commentedAllCategories,
  },
  {
    id: "repost_completionist",
    Icon: RefreshCcw,
    name: "Repost Completionist",
    description: "Reposted at least one tip in every category.",
    check: repostAllCategories,
  },
  {
    id: "achievement_hunter_50",
    Icon: Award,
    name: "Achievement Hunter",
    description: "Unlocked 50 achievements.",
    check: atLeast(unlockedCount, 50),
  },
  {
    id: "achievement_hunter_80",
    Icon: Crown,
    name: "Achievement Legend",
    description: "Unlocked 80 achievements.",
    check: atLeast(unlockedCount, 80),
  },
  {
    id: "playground_25_day",
    Icon: SquareTerminal,
    name: "Code Binger",
    description: "Ran Python 25 times in a single day.",
    check: atLeast(playgroundRunsToday, 25),
  },
  {
    id: "tutor_7_days",
    Icon: Bell,
    name: "Tutor Devotee",
    description: "Asked the tutor on 7 different days.",
    check: atLeast(chatActiveDaysCount, 7),
  },
  {
    id: "deep_commenter",
    Icon: NotebookPen,
    name: "Deep Commenter",
    description: "Left 20+ comments in total.",
    check: atLeast(countAllComments, 20),
  },
  {
    id: "streak_30_hard",
    Icon: Flame,
    name: "Monthly Master",
    description: "Maintained a 30-day streak.",
    check: atLeast(longestDayStreak, 30),
  },
  {
    id: "likes_500_hard",
    Icon: Heart,
    name: "Heart Collector",
    description: "Liked 500 tips in total.",
    check: atLeast(() => getUserMeta().then((m) => m.total_likes), 500),
  },
  {
    id: "time_100h",
    Icon: Orbit,
    name: "Python Monk",
    description: "Spent 100 hours in the app in total.",
    check: atLeast(() => getUserMeta().then((m) => m.total_time), 100 * 3600),
  },
  {
    id: "views_2000",
    Icon: Telescope,
    name: "Feed Destroyer",
    description: "Viewed 2000 tips in total.",
    check: atLeast(() => getUserMeta().then((m) => m.views_total), 2000),
  },
  {
    id: "night_weekend_hard",
    Icon: MoonStar,
    name: "Weekend Night Owl",
    description: "Was active past midnight on a weekend.",
    check: async () => {
      try {
        const [favs, reps, comments, chat] = await Promise.all([
          getFavorites(),
          getReposts(),
          getAllComments(),
          getChatHistory(),
        ]);
        const stamps = [
          ...favs.map((f) => f.timestamp),
          ...reps.map((r) => r.timestamp),
          ...comments.map((c) => c.timestamp),
          ...chat.map((c) => c.timestamp),
        ];
        return stamps.some((t) => {
          const d = new Date(t);
          const day = d.getDay();
          const h = d.getHours();
          return (day === 0 || day === 6) && h >= 0 && h < 4;
        });
      } catch {
        return false;
      }
    },
  },
];

export async function checkAchievements(): Promise<string[]> {
  const all = await getAchievements();
  const unlockedNames = new Set(all.map((a) => a.achievement_name));
  const fresh: string[] = [];
  for (const def of ACHIEVEMENTS) {
    if (unlockedNames.has(def.id)) continue;
    try {
      if (await def.check()) {
        await unlockAchievement(def.id);
        fresh.push(def.id);
      }
    } catch {
      // IndexedDB unavailable — ignore
    }
  }
  return fresh;
}