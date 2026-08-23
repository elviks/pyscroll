"use client";

import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { getUserMeta, setUserMeta } from "@/lib/db";

type Theme = "dark" | "light";

interface ThemeCtx {
  theme: Theme;
  toggle: () => void;
}

const ThemeContext = createContext<ThemeCtx>({ theme: "dark", toggle: () => {} });

function readStored(): Theme {
  if (typeof window === "undefined") return "dark";
  const stored = localStorage.getItem("pyscroll-theme");
  return stored === "light" || stored === "dark" ? stored : "dark";
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>(readStored);

  useEffect(() => {
    document.documentElement.classList.toggle("light", theme === "light");
  }, [theme]);

  useEffect(() => {
    getUserMeta()
      .then((m) => {
        if (m.theme && m.theme !== readStored()) setTheme(m.theme);
      })
      .catch(() => {});
  }, []);

  function toggle() {
    const next: Theme = theme === "dark" ? "light" : "dark";
    setTheme(next);
    localStorage.setItem("pyscroll-theme", next);
    setUserMeta({ theme: next }).catch(() => {});
  }

  return <ThemeContext.Provider value={{ theme, toggle }}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  return useContext(ThemeContext);
}