import type { Metadata } from "next";
// Use next/font/local to load your local font files
import localFont from "next/font/local";
// Change the import path for globals.css to use the root alias
import "@/globals.css";

// Set up the local Geist font from your /src/app/fonts/ directory
const geist = localFont({
  src: './fonts/GeistVF.woff',
  variable: '--font-geist'
});

export const metadata: Metadata = {
  title: "BirdPicks App",
  description: "NHL Data Analysis & Predictions",
};

// This is the root layout. It should be simple and should NOT
// contain your sidebar. It just sets up the basic HTML structure.
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      {/* Apply the local font className here */}
      <body className={geist.className}>{children}</body>
    </html>
  );
}

