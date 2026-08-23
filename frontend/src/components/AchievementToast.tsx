"use client";

import { AnimatePresence, motion } from "framer-motion";
import { ACHIEVEMENTS } from "@/lib/achievements";
import { TrophyIcon } from "./icons";

export default function AchievementToast({
     unlockId,
     onDone,
}: {
     unlockId: string | null;
     onDone: () => void;
}) {
     const def = ACHIEVEMENTS.find(
          (a) => a.id === unlockId,
     );
     return (
          <AnimatePresence>
               {def && (
                    <motion.div
                         key={def.id}
                         initial={{
                              y: -80,
                              opacity: 0,
                              scale: 0.95,
                         }}
                         animate={{
                              y: 0,
                              opacity: 1,
                              scale: 1,
                         }}
                         exit={{
                              y: -80,
                              opacity: 0,
                              scale: 0.95,
                         }}
                         transition={{
                              type: "spring",
                              stiffness: 400,
                              damping: 28,
                         }}
                         onAnimationComplete={() =>
                              setTimeout(onDone, 3500)
                         }
                         className="fixed left-1/2 top-4 z-50 -translate-x-1/2"
                    >
                         <motion.div
                              initial={{ opacity: 0 }}
                              animate={{ opacity: 1 }}
                              transition={{ delay: 0.1 }}
                              className="flex items-center gap-3 rounded-2xl border border-accent/40 bg-bgro/90 px-4 py-3.5 shadow-xl shadow-black/40 backdrop-blur-xl"
                         >
                              <motion.div
                                   animate={{
                                        scale: [1, 1.15, 1],
                                        rotate: [0, 5, 0],
                                   }}
                                   transition={{
                                        duration: 1.2,
                                        repeat: Infinity,
                                        ease: "easeInOut",
                                   }}
                                   className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-linear-to-br from-accent/30 to-accent/10"
                              >
                                   <TrophyIcon className="h-5 w-5 text-accent" />
                              </motion.div>
                              <div className="min-w-0">
                                   <p className="text-[10px] font-medium uppercase tracking-widest text-accent/90">
                                        Achievement unlocked
                                   </p>
                                   <motion.p
                                        initial={{
                                             opacity: 0,
                                             x: -10,
                                        }}
                                        animate={{
                                             opacity: 1,
                                             x: 0,
                                        }}
                                        transition={{
                                             delay: 0.1,
                                             duration: 0.2,
                                        }}
                                        className="flex items-center gap-2 text-sm font-semibold text-fg"
                                   >
                                        <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-accentsoft text-accent">
                                             <def.Icon
                                                  className="h-3.5 w-3.5"
                                                  strokeWidth={
                                                       2.2
                                                  }
                                             />
                                        </span>
                                        <span>
                                             {def.name}
                                        </span>
                                   </motion.p>
                              </div>
                              <motion.div
                                   animate={{
                                        width: ["100%", 0],
                                   }}
                                   transition={{
                                        duration: 3.5,
                                        ease: "linear",
                                   }}
                                   className="absolute bottom-0 left-0 h-1 bg-accent/50 rounded-bl-2xl rounded-br-2xl"
                              />
                         </motion.div>
                    </motion.div>
               )}
          </AnimatePresence>
     );
}
