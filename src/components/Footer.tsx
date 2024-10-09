"use client";

import { useCookieContext } from "@/context/CookieContext";
import CookieConsentBanner from "./CookieConsentBanner";
import { ThemeButton } from "./ThemeButton";
import Link from "next/link";

const Footer = () => {
  let { setShouldShowBanner } = useCookieContext();

  const onClickCookieSettings = () => {
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
              <ThemeButton
                color="tertiary"
                label="Cookie Settings"
                onPress={onClickCookieSettings}
                className="hover:text-gray-800 cursor-pointer text-gray-600"
              />
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

            <span className="max-sm:hidden">—</span>

            <li className="base-sm underline text-gray-600 mx-auto">
              <Link
                href="/accessibility-statement"
                className="hover:text-gray-800"
              >
                Accessibility Statement
              </Link>
            </li>
          </ul>
        </nav>

        <CookieConsentBanner />
      </footer>
    </div>
  );
};

export default Footer;
