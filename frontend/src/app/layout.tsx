import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "BirdPicks NHL Predictor",
  description: "Web app for NHL game and player predictions",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <header className="bg-blue-600 text-white p-4">
          <h1 className="text-2xl font-bold">BirdPicks NHL Predictor</h1>
        </header>
        <main className="p-4">{children}</main>
      </body>
    </html>
  );
}