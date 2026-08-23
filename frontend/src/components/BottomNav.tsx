"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import {
     ChatNavIcon,
     HomeIcon,
     TerminalIcon,
     TrophyIcon,
     UserIcon,
} from "./icons";

const LINKS = [
     { href: "/feed", label: "Feed", Icon: HomeIcon },
     {
          href: "/messages",
          label: "Tutor",
          Icon: ChatNavIcon,
     },
     {
          href: "/playground",
          label: "Try it",
          Icon: TerminalIcon,
     },
     {
          href: "/notifications",
          label: "Achievements",
          Icon: TrophyIcon,
     },
     { href: "/profile", label: "Profile", Icon: UserIcon },
];

export default function BottomNav() {
     const pathname = usePathname();
     const [mounted, setMounted] = useState(false);
     useEffect(() => {
          const id = requestAnimationFrame(() =>
               setMounted(true),
          );
          return () => cancelAnimationFrame(id);
     }, []);
     if (mounted && pathname === "/") return null;
     return (
          <nav className="shrink-0 border-t border-line bg-bgro/80 backdrop-blur-xl pb-[env(safe-area-inset-bottom)]">
               <div className="mx-auto flex max-w-3xl items-stretch justify-between px-2">
                    {LINKS.map(({ href, label, Icon }) => {
                         const active =
                              href === "/"
                                   ? pathname === "/"
                                   : pathname.startsWith(
                                          href,
                                     );
                         return (
                              <Link
                                   key={href}
                                   href={href}
                                   className={`relative flex flex-1 flex-col items-center gap-1 py-2.5 transition-colors ${
                                        active
                                             ? "text-accent"
                                             : "text-muted hover:text-fg/80"
                                   }`}
                              >
                                   <span className="relative flex h-8 w-12 items-center justify-center">
                                        <span className="relative z-10 flex h-7 w-7 items-center justify-center">
                                             <Icon />
                                        </span>
                                   </span>
                                   <span className="relative z-10 text-[9px] font-medium uppercase tracking-wider">
                                        {label}
                                   </span>
                              </Link>
                         );
                    })}
               </div>
          </nav>
     );
}
