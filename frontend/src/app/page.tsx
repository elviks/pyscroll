"use client";

import Link from "next/link";
import { useRef } from "react";
import {
     motion,
     useScroll,
     useTransform,
} from "framer-motion";
import {
     Bot,
     Flame,
     Layers,
     Play,
     Sparkles,
     Terminal,
     Heart,
     MessageCircle,
} from "lucide-react";
import { PythonLogo } from "@/components/icons";

export default function LandingPage() {
     const scrollRef = useRef<HTMLDivElement>(null);
     const { scrollYProgress } = useScroll({
          container: scrollRef,
     });
     const heroParallax = useTransform(
          scrollYProgress,
          [0, 0.3],
          [0, -40],
     );
     const cardsParallax = useTransform(
          scrollYProgress,
          [0, 0.3],
          [0, -20],
     );

     return (
          <main
               ref={scrollRef}
               className="h-full overflow-y-auto bg-bg no-scrollbar"
          >
               <div className="relative min-h-full overflow-hidden">
                    {/* nav */}
                    <nav className="relative z-20 mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
                         <div className="flex items-center gap-2.5">
                              <div className="flex h-10 items-center justify-center rounded-xl">
                                   <PythonLogo
                                        className="h-20"
                                        icon
                                   />
                              </div>
                         </div>
                         <Link
                              href="/feed"
                              className="rounded-full border border-line/50 bg-bgsoft/60 px-4 py-1.5 text-xs font-medium text-fg backdrop-blur-sm transition-colors duration-150 hover:border-accent/30 hover:bg-accentsoft/40"
                         >
                              Open app
                         </Link>
                    </nav>

                    {/* hero - split with graphic */}
                    <div className="relative z-10 mx-auto max-w-6xl px-6 pb-10">
                         <div className="grid items-center gap-10 py-8 sm:py-12 lg:grid-cols-[1.05fr_0.95fr]">
                              {/* left: text */}
                              <motion.div
                                   style={{
                                        y: heroParallax,
                                   }}
                                   className="text-left"
                              >
                                   <motion.h1
                                        initial={{
                                             opacity: 0,
                                             y: 14,
                                        }}
                                        animate={{
                                             opacity: 1,
                                             y: 0,
                                        }}
                                        transition={{
                                             duration: 0.5,
                                             delay: 0.07,
                                        }}
                                        className=" text-4xl font-semibold leading-[0.95] tracking-tight text-fg sm:text-5xl lg:text-[56px]"
                                   >
                                        Doomscroll
                                        <br />
                                        <span className="bg-linear-to-r from-accent via-accent to-accent/50 bg-clip-text text-transparent">
                                             Python.
                                        </span>
                                        <br />
                                        Actually learn.
                                   </motion.h1>

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
                                             duration: 0.4,
                                             delay: 0.14,
                                        }}
                                        className="mt-4 max-w-md text-[15px] leading-6 text-muted"
                                   >
                                        Real code. Zero
                                        fluff.
                                   </motion.p>

                                   <motion.div
                                        initial={{
                                             opacity: 0,
                                             y: 10,
                                        }}
                                        animate={{
                                             opacity: 1,
                                             y: 0,
                                        }}
                                        transition={{
                                             duration: 0.4,
                                             delay: 0.22,
                                        }}
                                        className="mt-7 flex items-center gap-3"
                                   >
                                        <Link
                                             href="/feed"
                                             className="group inline-flex items-center gap-2 rounded-full bg-accent px-7 py-3.5 text-sm font-semibold text-white transition-all hover:opacity-85"
                                        >
                                             Try for
                                             free{" "}
                                        </Link>
                                   </motion.div>
                              </motion.div>

                              {/* right: phone mock with parallax */}
                              <motion.div
                                   style={{
                                        y: cardsParallax,
                                   }}
                                   className="relative mx-auto w-full max-w-90 lg:mx-0 lg:ml-auto"
                              >
                                   {/* glow behind phone */}
                                   <div className="absolute left-1/2 top-1/2 h-80 w-[320px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-accent/15 blur-[50px]" />

                                   {/* phone */}
                                   <motion.div
                                        initial={{
                                             opacity: 0,
                                             y: 24,
                                             rotate: 2,
                                        }}
                                        animate={{
                                             opacity: 1,
                                             y: 0,
                                             rotate: 2,
                                        }}
                                        transition={{
                                             duration: 0.7,
                                             delay: 0.3,
                                             ease: [
                                                  0.22, 1,
                                                  0.36, 1,
                                             ],
                                        }}
                                        whileHover={{
                                             rotate: 0,
                                             y: -4,
                                             transition: {
                                                  type: "spring",
                                                  stiffness: 500,
                                                  damping: 30,
                                                  mass: 0.6,
                                             },
                                        }}
                                        className="relative rounded-[2.2rem] border border-line/60 bg-bgsoft p-3 shadow-[0_20px_60px_-20px_rgba(0,0,0,0.6),0_0_0_1px_rgba(0,0,0,0.1)] will-change-transform"
                                   >
                                        <div className="rounded-[1.6rem] border border-line/40 bg-bg p-4">
                                             {/* phone header */}
                                             <div className="mb-4 flex items-center justify-between">
                                                  <div className="h-2 w-12 rounded-full bg-line" />
                                                  <div className="flex gap-1">
                                                       <span className="h-2 w-2 rounded-full bg-line" />
                                                       <span className="h-2 w-2 rounded-full bg-line" />
                                                       <span className="h-2 w-2 rounded-full bg-accent/40" />
                                                  </div>
                                             </div>
                                             {/* stacked cards */}
                                             <div className="space-y-3">
                                                  {[
                                                       {
                                                            cat: "python",
                                                            title: "Walrus operator",
                                                            code: "while chunk := f.read(1024):",
                                                            accent: true,
                                                       },
                                                       {
                                                            cat: "django",
                                                            title: "select_related",
                                                            code: "Book.objects.select_related()",
                                                            accent: false,
                                                       },
                                                       {
                                                            cat: "flask",
                                                            title: "Route guard",
                                                            code: "@app.get('/api')",
                                                            accent: false,
                                                       },
                                                  ].map(
                                                       (
                                                            c,
                                                            i,
                                                       ) => (
                                                            <motion.div
                                                                 key={
                                                                      c.title
                                                                 }
                                                                 initial={{
                                                                      opacity: 0,
                                                                      y: 12,
                                                                 }}
                                                                 animate={{
                                                                      opacity: 1,
                                                                      y: 0,
                                                                 }}
                                                                 transition={{
                                                                      delay:
                                                                           0.55 +
                                                                           i *
                                                                                0.1,
                                                                      duration: 0.4,
                                                                 }}
                                                                 className={`rounded-2xl border p-3 ${c.accent ? "border-accent/30 bg-accentsoft/40 shadow-[0_0_20px_-10px_var(--accentsoft)]" : "border-line/40 bg-bgsoft/60"}`}
                                                                 style={{
                                                                      transform: `translateY(${i * -2}px)`,
                                                                 }}
                                                            >
                                                                 <div className="flex items-center justify-between">
                                                                      <span className="rounded-full bg-accentsoft px-2 py-0.5 font-mono text-[9px] uppercase tracking-widest text-accent">
                                                                           {
                                                                                c.cat
                                                                           }
                                                                      </span>
                                                                      <span className="flex gap-1">
                                                                           <Heart className="h-3 w-3 text-muted/40" />
                                                                           <MessageCircle className="h-3 w-3 text-muted/40" />
                                                                      </span>
                                                                 </div>
                                                                 <p className="mt-2 text-xs font-medium text-fg">
                                                                      {
                                                                           c.title
                                                                      }
                                                                 </p>
                                                                 <pre className="mt-1.5 rounded-lg bg-bg px-2 py-1.5 font-mono text-[10px] leading-3 text-accent">
                                                                      {
                                                                           c.code
                                                                      }
                                                                 </pre>
                                                            </motion.div>
                                                       ),
                                                  )}
                                             </div>
                                             {/* fake action bar */}
                                             <div className="mt-4 flex justify-around border-t border-line/30 pt-3">
                                                  <Layers className="h-4 w-4 text-muted/30" />
                                                  <Bot className="h-4 w-4 text-accent" />
                                                  <Terminal className="h-4 w-4 text-muted/30" />
                                             </div>
                                        </div>
                                   </motion.div>

                                   {/* floating badges parallax */}
                                   <motion.div
                                        animate={{
                                             y: [0, -8, 0],
                                        }}
                                        transition={{
                                             duration: 3.5,
                                             repeat: Infinity,
                                             ease: "easeInOut",
                                        }}
                                        className="absolute -right-2 top-6 flex items-center gap-1.5 rounded-full border border-line/50 bg-bgsoft px-3 py-1.5 text-[11px] font-medium shadow-lg"
                                   >
                                        <Heart className="h-3 w-3 fill-accent text-accent" />
                                        Liked
                                   </motion.div>
                                   <motion.div
                                        animate={{
                                             y: [0, 8, 0],
                                        }}
                                        transition={{
                                             duration: 4,
                                             repeat: Infinity,
                                             ease: "easeInOut",
                                             delay: 0.5,
                                        }}
                                        className="absolute -left-3 bottom-16 flex items-center gap-1.5 rounded-full border border-line/50 bg-bgsoft px-3 py-1.5 text-[11px] font-medium shadow-lg"
                                   >
                                        <Flame className="h-3 w-3 text-accent" />
                                        7 day streak
                                   </motion.div>
                              </motion.div>
                         </div>

                         {/* feature strip - visual icons, minimal text */}
                         <div className="mt-6 grid grid-cols-2 gap-3 lg:grid-cols-4">
                              {[
                                   {
                                        icon: Layers,
                                        label: "Infinite",
                                        sub: "Endless swipe",
                                   },
                                   {
                                        icon: Bot,
                                        label: "AI Tutor",
                                        sub: "Ask anything",
                                   },
                                   {
                                        icon: Terminal,
                                        label: "Playground",
                                        sub: "Run now",
                                   },
                                   {
                                        icon: Flame,
                                        label: "Streaks",
                                        sub: "100+ badges",
                                   },
                              ].map((f, i) => (
                                   <motion.div
                                        key={f.label}
                                        initial={{
                                             opacity: 0,
                                             y: 12,
                                        }}
                                        whileInView={{
                                             opacity: 1,
                                             y: 0,
                                        }}
                                        viewport={{
                                             once: true,
                                        }}
                                        transition={{
                                             delay:
                                                  i * 0.06,
                                             duration: 0.35,
                                        }}
                                        className="group relative overflow-hidden rounded-2xl border border-line/50 bg-bgsoft/40 p-4 backdrop-blur-sm transition-colors duration-150 hover:border-accent/30 hover:bg-accentsoft/10"
                                   >
                                        <div className="absolute -right-6 -top-6 h-16 w-16 rounded-full bg-accent/5 blur-xl transition-colors group-hover:bg-accent/10" />
                                        <f.icon
                                             className="h-5 w-5 text-accent"
                                             strokeWidth={
                                                  1.7
                                             }
                                        />
                                        <p className="mt-3 text-sm font-semibold text-fg">
                                             {f.label}
                                        </p>
                                        <p className="text-xs text-muted/60">
                                             {f.sub}
                                        </p>
                                   </motion.div>
                              ))}
                         </div>

                         {/* code preview graphic */}
                         <div className="mx-auto mt-10 max-w-5xl">
                              <motion.div
                                   initial={{
                                        opacity: 0,
                                        y: 16,
                                   }}
                                   whileInView={{
                                        opacity: 1,
                                        y: 0,
                                   }}
                                   viewport={{
                                        once: true,
                                        margin: "-40px",
                                   }}
                                   transition={{
                                        duration: 0.5,
                                   }}
                                   className="relative overflow-hidden rounded-3xl border border-line/50 bg-bgsoft/60 backdrop-blur-sm"
                              >
                                   <div className="flex items-center gap-2 border-b border-line/50 px-4 py-3">
                                        <span className="h-3 w-3 rounded-full bg-red-500/70" />
                                        <span className="h-3 w-3 rounded-full bg-yellow-500/70" />
                                        <span className="h-3 w-3 rounded-full bg-accent/70" />
                                        <span className="ml-3 font-mono text-xs text-muted">
                                             playground.py —
                                        </span>
                                        <span className="ml-auto hidden items-center gap-1.5 font-mono text-[11px] text-muted/60 sm:flex">
                                             <Sparkles className="h-3 w-3 text-accent" />{" "}
                                             minimal • fast
                                             • free
                                        </span>
                                   </div>
                                   <div className="grid gap-0 sm:grid-cols-[1.1fr_0.9fr]">
                                        <pre className="p-5 font-mono text-xs leading-5 text-fg/90">
                                             <span className="text-muted">
                                                  #
                                                  one-liner
                                                  magic
                                             </span>
                                             {"\n"}
                                             <span className="text-accent">
                                                  def
                                             </span>{" "}
                                             <span className="text-fg">
                                                  greet
                                             </span>
                                             (name):
                                             {"\n"}{" "}
                                             <span className="text-accent">
                                                  return
                                             </span>{" "}
                                             <span className="text-(--syn-string)">
                                                  f&quot;Hello,{" "}
                                                  {"{name}"}
                                                  !&quot;
                                             </span>
                                             {"\n\n"}
                                             <span className="text-(--syn-builtin)">
                                                  print
                                             </span>
                                             (greet(
                                             <span className="text-(--syn-string)">
                                                  &quot;you&quot;
                                             </span>
                                             ))
                                             {"\n"}
                                             <span className="text-muted">
                                                  # → Hello,
                                                  you!
                                             </span>
                                        </pre>
                                        <div className="border-t border-line/40 bg-bg p-4 sm:border-l sm:border-t-0">
                                             <p className="font-mono text-[11px] uppercase tracking-widest text-muted">
                                                  Output
                                             </p>
                                             <div className="mt-2 rounded-xl border border-accent/20 bg-accentsoft/30 p-3 font-mono text-xs text-accent">
                                                  Hello,
                                                  you!
                                             </div>
                                             <div className="mt-4 flex gap-2">
                                                  <span className="rounded-full bg-bgsoft px-2.5 py-1 text-[11px] text-muted">
                                                       No
                                                       setup
                                                  </span>
                                                  <span className="rounded-full bg-bgsoft px-2.5 py-1 text-[11px] text-muted">
                                                       Runs
                                                       in
                                                       browser
                                                  </span>
                                             </div>
                                        </div>
                                   </div>
                              </motion.div>
                         </div>

                         {/* final CTA compact */}
                         <div className="mx-auto mt-12 max-w-2xl text-center">
                              <h2 className="text-xl font-semibold tracking-tight text-fg">
                                   Ready to scroll smarter?
                              </h2>
                              <Link
                                   href="/feed"
                                   className="mt-4 inline-flex items-center gap-2 rounded-full bg-accent px-8 py-3.5 text-sm font-semibold text-white shadow-[0_10px_30px_-10px_var(--accent)] transition-all hover:opacity-90"
                              >
                                   <Play className="h-4 w-4 fill-white" />{" "}
                                   Try for free
                              </Link>
                         </div>

                         <p className="mt-10 text-center font-mono text-[11px] tracking-widest text-muted/40">
                              pyscroll • doomscrolling for
                              Python
                         </p>
                    </div>
               </div>
          </main>
     );
}
