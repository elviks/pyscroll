import { openDB, type DBSchema, type IDBPDatabase } from "idb";

export interface Favorite {
  id?: number;
  tip_id: number;
  timestamp: number;
}

export interface Repost {
  id?: number;
  tip_id: number;
  timestamp: number;
}

export interface Comment {
  id?: number;
  tip_id: number;
  comment_text: string;
  timestamp: number;
}

export interface Achievement {
  id?: number;
  achievement_name: string;
  unlocked: boolean;
  timestamp: number;
}

export interface ChatMessage {
  id?: number;
  role: "user" | "assistant";
  content: string;
  timestamp: number;
}

export interface UserMeta {
  id: string;
  name: string;
  time_spent_today: number;
  total_time: number;
  likes_today: number;
  total_likes: number;
  total_reposts: number;
  views_total: number;
  views_today: number;
  last_active_date: string;
  theme: "dark" | "light";
  last_action_ts: number;
  max_tip_id_viewed: number;
  viewed_categories: string[];
  playground_runs: number;
  feed_category: string;
  current_streak: number;
  longest_streak: number;
}

interface PyScrollDB extends DBSchema {
  favorites: { key: number; value: Favorite; indexes: { "by-tip": number } };
  reposts: { key: number; value: Repost; indexes: { "by-tip": number } };
  comments: { key: number; value: Comment; indexes: { "by-tip": number } };
  achievements: { key: number; value: Achievement };
  chat_history: { key: number; value: ChatMessage };
  user_meta: { key: string; value: UserMeta };
}

const DB_NAME = "pyscroll";
const DB_VERSION = 1;

let dbPromise: Promise<IDBPDatabase<PyScrollDB>> | null = null;

export function getDB() {
  if (!dbPromise) {
    dbPromise = openDB<PyScrollDB>(DB_NAME, DB_VERSION, {
      upgrade(db) {
        const fav = db.createObjectStore("favorites", {
          keyPath: "id",
          autoIncrement: true,
        });
        fav.createIndex("by-tip", "tip_id");
        const rep = db.createObjectStore("reposts", {
          keyPath: "id",
          autoIncrement: true,
        });
        rep.createIndex("by-tip", "tip_id");
        const com = db.createObjectStore("comments", {
          keyPath: "id",
          autoIncrement: true,
        });
        com.createIndex("by-tip", "tip_id");
        db.createObjectStore("achievements", {
          keyPath: "id",
          autoIncrement: true,
        });
        db.createObjectStore("chat_history", {
          keyPath: "id",
          autoIncrement: true,
        });
        db.createObjectStore("user_meta", { keyPath: "id" });
      },
    });
  }
  return dbPromise;
}

const DEFAULT_META: UserMeta = {
  id: "main",
  name: "Pythonista",
  time_spent_today: 0,
  total_time: 0,
  likes_today: 0,
  total_likes: 0,
  total_reposts: 0,
  views_total: 0,
  views_today: 0,
  last_active_date: todayStr(),
  theme: "dark",
  last_action_ts: 0,
  max_tip_id_viewed: 0,
  viewed_categories: [],
  playground_runs: 0,
  feed_category: "python",
  current_streak: 1,
  longest_streak: 1,
};

export function todayStr(): string {
  return new Date().toISOString().slice(0, 10);
}

export async function getUserMeta(): Promise<UserMeta> {
  const db = await getDB();
  const meta = await db.get("user_meta", "main");
  if (!meta) {
    await db.put("user_meta", DEFAULT_META);
    return { ...DEFAULT_META };
  }
  const today = todayStr();
  let m: UserMeta = { ...DEFAULT_META, ...meta };
  if (m.last_active_date !== today) {
    const yesterday = new Date(Date.now() - 86_400_000).toISOString().slice(0, 10);
    const streak = m.last_active_date === yesterday ? (m.current_streak || 0) + 1 : 1;
    m = {
      ...m,
      last_active_date: today,
      time_spent_today: 0,
      likes_today: 0,
      views_today: 0,
      current_streak: streak,
      longest_streak: Math.max(m.longest_streak || 0, streak),
    };
    await db.put("user_meta", m);
  }
  return m;
}

export async function setUserMeta(
  patch: Partial<UserMeta> | ((m: UserMeta) => Partial<UserMeta>),
): Promise<UserMeta> {
  const db = await getDB();
  const current = await getUserMeta();
  const resolved = typeof patch === "function" ? patch(current) : patch;
  const next = { ...current, ...resolved };
  await db.put("user_meta", next);
  return next;
}

// ---------- favorites ----------

export async function addFavorite(tip_id: number): Promise<void> {
  const db = await getDB();
  const existing = await db.getAllFromIndex("favorites", "by-tip", tip_id);
  if (existing.length === 0) {
    await db.add("favorites", { tip_id, timestamp: Date.now() });
  }
}

export async function removeFavorite(tip_id: number): Promise<void> {
  const db = await getDB();
  const existing = await db.getAllFromIndex("favorites", "by-tip", tip_id);
  for (const f of existing) if (f.id !== undefined) await db.delete("favorites", f.id);
}

export async function getFavorites(): Promise<Favorite[]> {
  const db = await getDB();
  const all = await db.getAll("favorites");
  return all.sort((a, b) => b.timestamp - a.timestamp);
}

// ---------- reposts ----------

export async function addRepost(tip_id: number): Promise<void> {
  const db = await getDB();
  const existing = await db.getAllFromIndex("reposts", "by-tip", tip_id);
  if (existing.length === 0) {
    await db.add("reposts", { tip_id, timestamp: Date.now() });
    await setUserMeta({ total_reposts: (await getUserMeta()).total_reposts + 1 });
  }
}

export async function removeRepost(tip_id: number): Promise<void> {
  const db = await getDB();
  const existing = await db.getAllFromIndex("reposts", "by-tip", tip_id);
  for (const r of existing) if (r.id !== undefined) await db.delete("reposts", r.id);
}

export async function getReposts(): Promise<Repost[]> {
  const db = await getDB();
  const all = await db.getAll("reposts");
  return all.sort((a, b) => b.timestamp - a.timestamp);
}

// ---------- comments ----------

export async function addComment(tip_id: number, comment_text: string): Promise<Comment> {
  const db = await getDB();
  const c: Comment = { tip_id, comment_text, timestamp: Date.now() };
  const id = await db.add("comments", c);
  return { ...c, id };
}

export async function getCommentsByTip(tip_id: number): Promise<Comment[]> {
  const db = await getDB();
  const all = await db.getAllFromIndex("comments", "by-tip", tip_id);
  return all.sort((a, b) => a.timestamp - b.timestamp);
}

export async function getAllComments(): Promise<Comment[]> {
  const db = await getDB();
  return (await db.getAll("comments")).sort((a, b) => a.timestamp - b.timestamp);
}

export async function countAllComments(): Promise<number> {
  const db = await getDB();
  return (await db.getAll("comments")).length;
}

export async function countCommentsToday(): Promise<number> {
  const db = await getDB();
  const all = await db.getAll("comments");
  const start = Date.parse(`${todayStr()}T00:00:00`);
  return all.filter((c) => c.timestamp >= start).length;
}

export async function getFavoriteTipIds(): Promise<number[]> {
  const db = await getDB();
  const all = await db.getAll("favorites");
  return [...new Set(all.map((f) => f.tip_id))];
}

export async function getRepostTipIds(): Promise<number[]> {
  const db = await getDB();
  const all = await db.getAll("reposts");
  return [...new Set(all.map((r) => r.tip_id))];
}

export async function getCommentedTipIds(): Promise<number[]> {
  const db = await getDB();
  const all = await db.getAll("comments");
  return [...new Set(all.map((c) => c.tip_id))];
}

export async function getLongestCommentLength(): Promise<number> {
  const db = await getDB();
  const all = await db.getAll("comments");
  return all.reduce((max, c) => Math.max(max, c.comment_text.length), 0);
}

export async function countRepostsToday(): Promise<number> {
  const db = await getDB();
  const all = await db.getAll("reposts");
  const start = Date.parse(`${todayStr()}T00:00:00`);
  return all.filter((r) => r.timestamp >= start).length;
}

// ---------- achievements ----------

export async function getAchievements(): Promise<Achievement[]> {
  const db = await getDB();
  return db.getAll("achievements");
}

export async function unlockAchievement(name: string): Promise<Achievement | null> {
  const db = await getDB();
  const all = await db.getAll("achievements");
  const existing = all.find((a) => a.achievement_name === name);
  if (existing?.unlocked) return null;
  if (existing) {
    const updated: Achievement = { ...existing, unlocked: true, timestamp: Date.now() };
    await db.put("achievements", updated);
    return updated;
  }
  const created: Achievement = {
    achievement_name: name,
    unlocked: true,
    timestamp: Date.now(),
  };
  const id = await db.add("achievements", created);
  return { ...created, id };
}

// ---------- chat ----------

export async function addChatMessage(
  role: "user" | "assistant",
  content: string,
): Promise<ChatMessage> {
  const db = await getDB();
  const m: ChatMessage = { role, content, timestamp: Date.now() };
  const id = await db.add("chat_history", m);
  return { ...m, id };
}

export async function getChatHistory(): Promise<ChatMessage[]> {
  const db = await getDB();
  const all = await db.getAll("chat_history");
  return all.sort((a, b) => a.timestamp - b.timestamp);
}

export async function clearChatHistory(): Promise<void> {
  const db = await getDB();
  await db.clear("chat_history");
}

export async function countChatUserMessages(): Promise<number> {
  const db = await getDB();
  const all = await db.getAll("chat_history");
  return all.filter((m) => m.role === "user").length;
}

// ---------- wipe ----------

export async function clearAllData(): Promise<void> {
  const db = await getDB();
  await Promise.all([
    db.clear("favorites"),
    db.clear("reposts"),
    db.clear("comments"),
    db.clear("achievements"),
    db.clear("chat_history"),
    db.clear("user_meta"),
  ]);
}