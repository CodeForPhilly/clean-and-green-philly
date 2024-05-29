import type { Metadata } from "next";
import "./globals.css";

const defaultTitle =
  "Clean & Green Philly - Helping communities clean vacant properties";
const description =
  "The ultimate toolkit to help community groups clean and green vacant properties to reduce gun violence in Philadelphia.";
const siteUrl = new URL("https://59a4-71-168-133-113.ngrok-free.app/"); //REPLACE

export const metadata: Metadata = {
  title: {
    default: defaultTitle,
    template: "%s - Clean & Green Philly",
  },
  description: description,
  icons: {
    icon: "/favicon.ico",
  },
  metadataBase: siteUrl,
  openGraph: {
    type: "website",
    url: "/",
    title: defaultTitle,
    description: description,
    images: [
      {
        url: "/thumbnail.png",
        width: 1200,
        height: 630,
        alt: "Clean & Green Philly",
      },
    ],
    siteName: "Clean & Green Philly",
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
