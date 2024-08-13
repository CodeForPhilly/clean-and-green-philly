'use client';

import { useCookieContext } from '@/context/CookieContext';
import CookieConsentBanner from './CookieConsentBanner';
import Link from 'next/link';

const Footer = () => {
  const { setShouldShowBanner } = useCookieContext();

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
              <span className="max-sm:hidden pl-2 pr-1" aria-hidden="true">
                —
              </span>
            </li>

            <li className="base-sm  text-gray-600 mx-auto">
              <a
                className="hover:text-gray-800 cursor-pointer underline"
                onClick={onClickCookieSettings}
              >
                Cookie Settings
              </a>
              <span className="max-sm:hidden pl-2 pr-1" aria-hidden="true">
                —
              </span>
            </li>

            <li className="base-sm text-gray-600 mx-auto">
              <Link
                href="/legal-disclaimer"
                className="hover:text-gray-800 underline"
              >
                Legal Disclaimer
              </Link>
              <span className="max-sm:hidden pl-2 pr-1" aria-hidden="true">
                —
              </span>
            </li>

            <li>
              <a
                href="mailto:cleanandgreenphl@gmail.com"
                className="base-sm underline text-gray-600 hover:text-gray-800"
              >
                Contact Us
              </a>
              <span className="max-sm:hidden pl-2 pr-1" aria-hidden="true">
                —
              </span>
            </li>

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
