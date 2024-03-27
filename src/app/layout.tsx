import { Footer, Header, Hotjar } from "@/components";
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "Clean & Green Philly",
    template: "%s - Clean & Green Philly",
  },
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
      <body>
        <a
          className="font-bold border-solid border-black bg-white transition left-0 absolute p-3 m-3 -translate-y-16 focus:translate-y-0 z-50"
          href="#main"
          tabIndex={0}
        >
          Skip to main content
        </a>
        {children}
      </body>
    </html>
  );
}
