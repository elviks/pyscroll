"use client";

export function HeartIcon({
     filled,
     className,
     ...props
}: {
     filled?: boolean;
     className?: string;
} & React.SVGProps<SVGSVGElement>) {
     return (
          <svg
               viewBox="0 0 24 24"
               className={className ?? "h-7 w-7"}
               fill={filled ? "currentColor" : "none"}
               stroke="currentColor"
               strokeWidth={1.8}
               strokeLinecap="round"
               strokeLinejoin="round"
               {...props}
          >
               <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z" />
          </svg>
     );
}

export function CommentIcon({
     className,
     ...props
}: React.SVGProps<SVGSVGElement>) {
     return (
          <svg
               viewBox="0 0 24 24"
               className={className ?? "h-7 w-7"}
               fill="none"
               stroke="currentColor"
               strokeWidth={1.8}
               strokeLinecap="round"
               strokeLinejoin="round"
               {...props}
          >
               <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5Z" />
          </svg>
     );
}

export function RepostIcon({
     className,
     ...props
}: React.SVGProps<SVGSVGElement>) {
     return (
          <svg
               viewBox="0 0 24 24"
               className={className ?? "h-7 w-7"}
               fill="none"
               stroke="currentColor"
               strokeWidth={1.8}
               strokeLinecap="round"
               strokeLinejoin="round"
               {...props}
          >
               <path d="M17 1l4 4-4 4" />
               <path d="M3 11V9a4 4 0 0 1 4-4h14" />
               <path d="M7 23l-4-4 4-4" />
               <path d="M21 13v2a4 4 0 0 1-4 4H3" />
          </svg>
     );
}

export function HomeIcon({
     className,
     ...props
}: React.SVGProps<SVGSVGElement>) {
     return (
          <svg
               viewBox="0 0 24 24"
               className={className ?? "h-6 w-6"}
               fill="none"
               stroke="currentColor"
               strokeWidth={1.7}
               strokeLinecap="round"
               strokeLinejoin="round"
               {...props}
          >
               <path d="M3 10.182 12 3l9 7.182M5 9v11a1 1 0 0 0 1 1h4v-6h4v6h4a1 1 0 0 0 1-1V9" />
          </svg>
     );
}

export function ChatNavIcon({
     className,
     ...props
}: React.SVGProps<SVGSVGElement>) {
     return (
          <svg
               viewBox="0 0 24 24"
               className={className ?? "h-6 w-6"}
               fill="none"
               stroke="currentColor"
               strokeWidth={1.7}
               strokeLinecap="round"
               strokeLinejoin="round"
               {...props}
          >
               <path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z" />
               <path
                    d="M8 12h.01M12 12h.01M16 12h.01"
                    strokeWidth={2.4}
               />
          </svg>
     );
}

export function UserIcon({
     className,
     ...props
}: React.SVGProps<SVGSVGElement>) {
     return (
          <svg
               viewBox="0 0 24 24"
               className={className ?? "h-6 w-6"}
               fill="none"
               stroke="currentColor"
               strokeWidth={1.7}
               strokeLinecap="round"
               strokeLinejoin="round"
               {...props}
          >
               <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
               <circle cx="12" cy="7" r="4" />
          </svg>
     );
}

export function SettingsNavIcon({
     className,
     ...props
}: React.SVGProps<SVGSVGElement>) {
     return (
          <svg
               viewBox="0 0 24 24"
               className={className ?? "h-6 w-6"}
               fill="none"
               stroke="currentColor"
               strokeWidth={1.7}
               strokeLinecap="round"
               strokeLinejoin="round"
               {...props}
          >
               <circle cx="12" cy="12" r="3" />
               <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1Z" />
          </svg>
     );
}

export function PythonLogo({
     className,
     icon,
     ...props
}: React.ImgHTMLAttributes<HTMLImageElement> & { icon?: boolean }) {
     return (
          <img
               src="/pyscroll.png"
               alt="PyScroll"
               className={className ?? "h-5 w-5"}
                style={icon ? { objectFit: "cover", objectPosition: "center" } : { objectFit: "contain" }}
               draggable={false}
               {...props}
          />
     );
}

export function SendIcon({
     className,
     ...props
}: React.SVGProps<SVGSVGElement>) {
     return (
          <svg
               viewBox="0 0 24 24"
               className={className ?? "h-5 w-5"}
               fill="none"
               stroke="currentColor"
               strokeWidth={1.8}
               strokeLinecap="round"
               strokeLinejoin="round"
               {...props}
          >
               <path d="M22 2 11 13" />
               <path d="M22 2 15 22l-4-9-9-4Z" />
          </svg>
     );
}

export function SunIcon({
     className,
     ...props
}: React.SVGProps<SVGSVGElement>) {
     return (
          <svg
               viewBox="0 0 24 24"
               className={className ?? "h-5 w-5"}
               fill="none"
               stroke="currentColor"
               strokeWidth={1.7}
               strokeLinecap="round"
               {...props}
          >
               <circle cx="12" cy="12" r="4" />
               <path d="M12 2v2m0 16v2M4.93 4.93l1.41 1.41m11.32 11.32 1.41 1.41M2 12h2m16 0h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41" />
          </svg>
     );
}

export function MoonIcon({
     className,
     ...props
}: React.SVGProps<SVGSVGElement>) {
     return (
          <svg
               viewBox="0 0 24 24"
               className={className ?? "h-5 w-5"}
               fill="none"
               stroke="currentColor"
               strokeWidth={1.7}
               strokeLinecap="round"
               strokeLinejoin="round"
               {...props}
          >
               <path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z" />
          </svg>
     );
}

export function TrashIcon({
     className,
     ...props
}: React.SVGProps<SVGSVGElement>) {
     return (
          <svg
               viewBox="0 0 24 24"
               className={className ?? "h-5 w-5"}
               fill="none"
               stroke="currentColor"
               strokeWidth={1.7}
               strokeLinecap="round"
               strokeLinejoin="round"
               {...props}
          >
               <path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2m3 0v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6" />
          </svg>
     );
}

export function TrophyIcon({
     className,
     ...props
}: React.SVGProps<SVGSVGElement>) {
     return (
          <svg
               viewBox="0 0 24 24"
               className={className ?? "h-6 w-6"}
               fill="none"
               stroke="currentColor"
               strokeWidth={1.7}
               strokeLinecap="round"
               strokeLinejoin="round"
               {...props}
          >
               <path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6m12 5h1.5a2.5 2.5 0 0 0 0-5H18" />
               <path d="M4 22h16M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22m7-7.34V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22" />
               <path d="M18 2H6v7a6 6 0 0 0 12 0V2Z" />
          </svg>
     );
}

export function SparkIcon({
     className,
     ...props
}: React.SVGProps<SVGSVGElement>) {
     return (
          <svg
               viewBox="0 0 24 24"
               className={className ?? "h-5 w-5"}
               fill="currentColor"
               {...props}
          >
               <path d="M12 2l1.9 5.7L19.6 9.6l-5.7 1.9L12 17.2l-1.9-5.7L4.4 9.6l5.7-1.9zM19 14l.9 2.6 2.6.9-2.6.9L19 21l-.9-2.6-2.6-.9 2.6-.9z" />
          </svg>
     );
}

export function AskIcon({
     className,
     ...props
}: React.SVGProps<SVGSVGElement>) {
     return (
          <svg
               viewBox="0 0 24 24"
               className={className ?? "h-7 w-7"}
               fill="none"
               stroke="currentColor"
               strokeWidth={1.7}
               strokeLinecap="round"
               strokeLinejoin="round"
               {...props}
          >
               <path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z" />
               <path d="M12 17h.01" strokeWidth={2.4} />
               <path d="M9.5 11a3.5 3.5 0 0 1 5 0" />
          </svg>
     );
}

export function PlayIcon({
     className,
     ...props
}: React.SVGProps<SVGSVGElement>) {
     return (
          <svg
               viewBox="0 0 24 24"
               className={className ?? "h-5 w-5"}
               fill="currentColor"
               {...props}
          >
               <path d="M8 5.14v14l11-7-11-7z" />
          </svg>
     );
}

export function TerminalIcon({
     className,
     ...props
}: React.SVGProps<SVGSVGElement>) {
     return (
          <svg
               viewBox="0 0 24 24"
               className={className ?? "h-6 w-6"}
               fill="none"
               stroke="currentColor"
               strokeWidth={1.7}
               strokeLinecap="round"
               strokeLinejoin="round"
               {...props}
          >
               <polyline points="4 17 10 11 4 5" />
               <line x1="12" y1="19" x2="20" y2="19" />
          </svg>
     );
}
