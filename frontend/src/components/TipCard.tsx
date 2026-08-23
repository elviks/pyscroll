"use client";

import { memo, useEffect, useState } from "react";
import { motion } from "framer-motion";
import type { Tip } from "@/lib/types";
import { PythonCode } from "@/lib/highlight";
import {
     CommentIcon,
     HeartIcon,
     RepostIcon,
} from "./icons";

interface Props {
     tip: Tip;
     liked: boolean;
     reposted: boolean;
     likeCount: number;
     commentCount: number;
     highlighted?: boolean;
     onLike: (tip: Tip) => void;
     onComment: (tip: Tip) => void;
     onRepost: (tip: Tip) => void;
}

function TipCardInner({
     tip,
     liked,
     reposted,
     likeCount,
     commentCount,
     highlighted,
     onLike,
     onComment,
     onRepost,
}: Props) {
     return (
          <section
               data-tip-id={tip.id}
               className="relative h-full w-full snap-start snap-always overflow-hidden bg-bg"
          >
               <motion.div
                    initial={{ opacity: 0, y: 24 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ amount: 0.3, once: false }}
                    transition={{
                         duration: 0.5,
                         ease: [0.22, 1, 0.36, 1],
                    }}
                    className="relative flex h-full flex-col"
               >
                    {/* card body */}
                    <div className="min-h-0 flex-1 overflow-y-auto no-scrollbar">
                         <div className="flex min-h-full flex-col justify-center gap-4 px-5 py-6 sm:px-8">
                              <motion.span
                                   initial={{
                                        opacity: 0,
                                        y: -8,
                                   }}
                                   animate={{
                                        opacity: 1,
                                        y: 0,
                                   }}
                                   transition={{
                                        delay: 0.1,
                                        duration: 0.3,
                                   }}
                                   className={`inline-flex items-center gap-1.5 w-fit rounded-full border bg-accentsoft px-3 py-1 font-mono text-[10px] uppercase tracking-widest transition-colors ${
                                        highlighted
                                             ? "border-accent text-accent shadow-[0_0_0_1px_var(--accent)]"
                                             : "border-accent/30 text-accent/90"
                                   }`}
                              >
                                   {tip.category}
                              </motion.span>

                              <motion.h2
                                   initial={{
                                        opacity: 0,
                                        y: 8,
                                   }}
                                   animate={{
                                        opacity: 1,
                                        y: 0,
                                   }}
                                   transition={{
                                        delay: 0.15,
                                        duration: 0.35,
                                   }}
                                   className="text-xl font-semibold leading-snug tracking-tight text-fg sm:text-2xl"
                              >
                                   {tip.title}
                              </motion.h2>

                              <motion.div
                                   initial={{
                                        opacity: 0,
                                        y: 8,
                                   }}
                                   animate={{
                                        opacity: 1,
                                        y: 0,
                                   }}
                                   transition={{
                                        delay: 0.2,
                                        duration: 0.35,
                                   }}
                              >
                                   <SectionLabel>
                                        what & why
                                   </SectionLabel>
                                   <p className="mt-1.5 text-[14px] leading-relaxed text-fg/90 sm:text-base">
                                        {tip.definition}
                                   </p>
                              </motion.div>

                              <motion.div
                                   initial={{
                                        opacity: 0,
                                        y: 8,
                                   }}
                                   animate={{
                                        opacity: 1,
                                        y: 0,
                                   }}
                                   transition={{
                                        delay: 0.25,
                                        duration: 0.35,
                                   }}
                              >
                                   <SectionLabel>
                                        example
                                   </SectionLabel>
                                   <div className="mt-2 relative">
                                        <div
                                             className={`rounded-2xl border bg-bgsoft/80 p-4 transition-all duration-200 ${
                                                  highlighted
                                                       ? "border-accent/50 ring-1 ring-accent/20 shadow-[0_0_30px_-10px_var(--accentsoft)]"
                                                       : "border-line/50"
                                             }`}
                                        >
                                             <PythonCode
                                                  code={
                                                       tip.example
                                                  }
                                             />
                                        </div>
                                   </div>
                              </motion.div>

                              <motion.div
                                   initial={{
                                        opacity: 0,
                                        y: 8,
                                   }}
                                   animate={{
                                        opacity: 1,
                                        y: 0,
                                   }}
                                   transition={{
                                        delay: 0.3,
                                        duration: 0.35,
                                   }}
                              >
                                   <SectionLabel>
                                        real world
                                   </SectionLabel>
                                   <p className="mt-1.5 text-[14px] leading-relaxed text-muted/80 sm:text-base">
                                        {tip.usecase}
                                   </p>
                              </motion.div>
                         </div>
                    </div>

                    {/* action rail */}
                    <div className="absolute bottom-5 right-4 flex flex-col items-center gap-5">
                         <RailButton
                              label={String(likeCount)}
                              active={liked}
                              activeClass="text-red-400"
                              onClick={() => onLike(tip)}
                              ariaLabel="Like"
                         >
                              <HeartIcon filled={liked} />
                         </RailButton>
                         <RailButton
                              label={String(commentCount)}
                              onClick={() => onComment(tip)}
                              ariaLabel="Comments"
                         >
                              <CommentIcon />
                         </RailButton>
                         <RailButton
                              active={reposted}
                              activeClass="text-accent"
                              onClick={() => onRepost(tip)}
                              ariaLabel="Repost"
                         >
                              <RepostIcon />
                         </RailButton>
                    </div>
               </motion.div>
          </section>
     );
}

export default memo(TipCardInner);

function SectionLabel({
     children,
}: {
     children: React.ReactNode;
}) {
     return (
          <span className="mb-2 block font-mono text-[10px] uppercase tracking-[0.2em] text-muted/70">
               {children}
          </span>
     );
}

function RailButton({
     label,
     active,
     activeClass = "text-accent",
     onClick,
     ariaLabel,
     children,
}: {
     label?: string;
     active?: boolean;
     activeClass?: string;
     onClick: () => void;
     ariaLabel: string;
     children: React.ReactNode;
}) {
     const isRed = activeClass.includes("red");
     const [pulseKey, setPulseKey] = useState(0);
     useEffect(() => {
          if (!active) return;
          const id = requestAnimationFrame(() =>
               setPulseKey((k) => k + 1),
          );
          return () => cancelAnimationFrame(id);
     }, [active]);
     return (
          <div className="flex flex-col items-center gap-1.5">
               <motion.button
                    whileHover={{ scale: 1.08 }}
                    whileTap={{ scale: 0.85 }}
                    onClick={onClick}
                    aria-label={ariaLabel}
                    className={`relative flex h-12 w-12 items-center justify-center rounded-full border bg-bgro/60 backdrop-blur-md transition-all duration-200 ${
                         active
                              ? `${activeClass} border-${isRed ? "red-500/50" : "accent/50"} bg-${isRed ? "red-500/10" : "accentsoft"}`
                              : "border-line/50 text-fg/80 hover:border-accent/50 hover:bg-accentsoft hover:text-accent"
                    }`}
               >
                    {children}
                    {active && (
                         <motion.span
                              key={pulseKey}
                              initial={{
                                   scale: 1,
                                   opacity: 1,
                              }}
                              animate={{
                                   scale: [1, 1.3, 1],
                                   opacity: [1, 0.5, 1],
                              }}
                              transition={{
                                   duration: 0.8,
                                   repeat: 0,
                              }}
                              className="absolute inset-0 rounded-full"
                              style={{
                                   background: isRed
                                        ? "radial-gradient(circle, #ef4444 0%, transparent 70%)"
                                        : "radial-gradient(circle, var(--accent) 0%, transparent 70%)",
                              }}
                         />
                    )}
               </motion.button>
               {label && (
                    <span className="font-mono text-[10px] tabular-nums text-muted/60">
                         {label}
                    </span>
               )}
          </div>
     );
}
