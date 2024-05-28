"use client";

import { useCookieContext } from "@/context/CookieContext";
import CookieConsentBanner from "./CookieConsentBanner";
import Link from "next/link";

const Footer = () => {
  let { setShouldShowBanner } = useCookieContext();

  const onClickCookieSettings = () => {
    // TODO: Add logic for showing cookie consent banner. See issue 597.
    setShouldShowBanner(true);
  };

  return (
    <div className="flex flex-col">
      <footer className="px-6 h-16 flex flex-grow justify-center items-center">
        <nav aria-label="content info">
          <ul className="flex flex-wrap gap-x-2 justify-between items-center w-full backdrop-saturate-150 bg-background/70">
            <li>
              <span className="base-sm text-gray-600">
                © 2024 Clean & Green Philly
              </span>
            </li>

            <span className="max-sm:hidden">—</span>

            <li className="base-sm underline text-gray-600 mx-auto">
              <a
                className="hover:text-gray-800 cursor-pointer"
                onClick={onClickCookieSettings}
              >
                Cookie Settings
              </a>
            </li>

            <span className="max-sm:hidden">—</span>

            <li className="base-sm underline text-gray-600 mx-auto">
              <Link href="/legal-disclaimer" className="hover:text-gray-800">
                Legal Disclaimer
              </Link>
            </li>

            <span className="max-sm:hidden">—</span>

            <li>
              <a
                href="mailto:cleanandgreenphl@gmail.com"
                className="base-sm underline text-gray-600 hover:text-gray-800"
              >
                Contact Us
              </a>
            </li>
          </ul>
        </nav>

        <CookieConsentBanner />
      </footer>
    </div>
  );
};

export default Footer;
