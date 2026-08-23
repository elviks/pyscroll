import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/lib/theme";
import TopBar from "@/components/TopBar";
import BottomNav from "@/components/BottomNav";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "PyScroll — doomscrolling for Python",
  description:
    "A TikTok-style doomscrolling feed of Python tips, with an AI Python tutor.",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  themeColor: "#061410",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="bg-bg font-sans text-fg">
        <ThemeProvider>
          <div className="flex h-dvh min-h-0 flex-col">
            <TopBar />
            <div className="min-h-0 flex-1 overflow-hidden">{children}</div>
            <BottomNav />
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}