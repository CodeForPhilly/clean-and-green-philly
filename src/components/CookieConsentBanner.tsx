"use client";

import { useState } from "react";
import { ThemeButton } from "./ThemeButton";
import { Check, X } from "@phosphor-icons/react";

const CookieConsentBanner = () => {
  const [cookieConsent, setCookieConsent] = useState(false);

  const onClickButton = (shouldAllowCookies: boolean) => {
    setCookieConsent(true);

    // TODO: Add logic for accepting or declining cookies. See issue 597.
    console.log("shouldAllowCookies", shouldAllowCookies);
  };

  return (
    <div
      className={`${
        cookieConsent
          ? "hidden"
          : "md:flex fixed inset-x-0 bottom-0 z-20 justify-between bg-blue-200 p-4 sm:p-6"
      }`}
    >
      <div>
        <div className="heading-md">Can we store cookies to your browser?</div>
        <div className="body-sm">
          This provides you a nice experience preserving your filtering, your
          position on the map and your property saved list.
        </div>
      </div>

      <div className="flex justify-end gap-2 pt-4 sm:pt-0">
        <div className="flex flex-none items-center gap-x-2">
          <ThemeButton
            color="tertiary"
            label="Decline"
            startContent={<X />}
            onPress={() => onClickButton(false)}
          />

          <ThemeButton
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
