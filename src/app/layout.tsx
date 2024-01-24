import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Clean & Green Philly",
  description:
    "Reduce the gun violence in Philadelphia by finding vacant properties to clean and green them.",
  icons: {
    icon: "/favicon.ico",
  },
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
