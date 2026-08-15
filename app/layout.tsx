import type { Metadata } from "next";
import { IBM_Plex_Sans, Newsreader } from "next/font/google";
import "./globals.css";

const body = Newsreader({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-body",
});

const heading = IBM_Plex_Sans({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-heading",
  weight: ["400", "500", "600"],
});

export const metadata: Metadata = {
  title: "Signals Before Movement | Ranking Signal Analysis",
  description:
    "An observational study of content and search signals associated with subsequent organic position movement.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body className={`${body.variable} ${heading.variable}`}>{children}</body>
    </html>
  );
}
