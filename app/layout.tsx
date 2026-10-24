import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "BusTracker",
  description: "Self-hosted school-bus tracking, attendance, and parent alerts.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
