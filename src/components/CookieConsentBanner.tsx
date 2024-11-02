'use client';

import { ThemeButton } from './ThemeButton';
import { Check, X } from '@phosphor-icons/react';
import { useCookieContext } from '@/context/CookieContext';
import { useEffect, useState, useRef } from 'react';

const CookieConsentBanner = () => {
  const { shouldShowBanner, setShouldAllowCookies, setShouldShowBanner } =
    useCookieContext();

  const bannerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const [isClientSide, setIsClientSide] = useState(false);

  useEffect(() => {
    // Ensure accessing localStorage only runs on the client side.
    setIsClientSide(true);
  }, []);

  const onClickButton = (shouldSaveCookies: boolean) => {
    setShouldAllowCookies(shouldSaveCookies);
    setShouldShowBanner(false);
  };

  useEffect(() => {
    // Focus on the banner when it becomes visible
    if (shouldShowBanner && bannerRef.current) {
      // Use setTimeout to ensure focus is applied after DOM updates
      setTimeout(() => {
        bannerRef.current?.focus();
      }, 0);
    }
  }, [shouldShowBanner]); // Trigger focus when shouldShowBanner changes

  if (!isClientSide) return null;

  return (
    <div
      role="region"
      tabIndex={-1} // Make the div focusable
      ref={bannerRef} // Attach the ref to the banner
      aria-labelledby="cookie_heading"
      className={`${
        shouldShowBanner
          ? 'md:flex fixed inset-x-0 bottom-0 z-20 justify-between bg-blue-200 p-4 sm:p-6'
          : 'hidden'
      }`}
    >
      <div>
        <h2 className="heading-md" id="cookie_heading">
          Can we store cookies to your browser?
        </h2>
        <div className="body-sm">
          <p>
            This provides you a nice experience preserving your filtering, your
            position on the map and your property saved list.
          </p>
        </div>
      </div>

      <div className="flex justify-end gap-2 pt-4 sm:pt-0">
        <div className="flex flex-none items-center gap-x-2">
          <ThemeButton
            tabIndex={1}
            color="tertiary"
            label="Decline"
            startContent={<X />}
            onPress={() => onClickButton(false)}
          />

          <ThemeButton
            tabIndex={2}
            color="primary"
            label="Accept"
            startContent={<Check />}
            onPress={() => onClickButton(true)}
          />
        </div>
      </div>
    </div>
  );
};

export default CookieConsentBanner;
