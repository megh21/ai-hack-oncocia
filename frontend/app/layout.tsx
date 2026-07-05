import type { Metadata } from "next";
import { DM_Sans, Fraunces } from "next/font/google";
import "./globals.css";

const dmSans = DM_Sans({
  variable: "--font-dm-sans",
  subsets: ["latin"],
});

const fraunces = Fraunces({
  variable: "--font-fraunces",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "OncoAccess | Financial Relief",
  description: "Find financial support and alternatives for your medication.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${dmSans.variable} ${fraunces.variable} antialiased text-xl`}
    >
      <body className="min-h-screen bg-[#F7F5F0] text-[#2C352A] font-sans">
        {children}
      </body>
    </html>
  );
}
