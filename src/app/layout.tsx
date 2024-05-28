import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default:
      "Clean & Green Philly - Helping communities clean vacant properties",
    template: "%s - Clean & Green Philly",
  },
  description:
    "The ultimate toolkit to help community groups clean and green vacant properties to reduce gun violence in Philadelphia.",
  icons: {
    icon: "/favicon.ico",
  },
  openGraph: {
    type: "website",
    url: "https://59a4-71-168-133-113.ngrok-free.app/", // Replace
    title: "Clean & Green Philly - Helping communities clean vacant properties",
    description:
      "The ultimate toolkit to help community groups clean and green vacant properties to reduce gun violence in Philadelphia.",
    images: [
      {
        url: "/thumbnail.png", // Path to the image in the public directory
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
        <head>
          <meta property="og:image" content="/thumbnail.png" />
          <meta property="og:image:type" content="image/png" />
          <meta property="og:image:width" content="1200" />
          <meta property="og:image:height" content="630" />
        </head>
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
