import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "HMRC Tax Advisor — MindFizz",
  description: "AI-powered UK tax guidance based on official HMRC manuals",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
