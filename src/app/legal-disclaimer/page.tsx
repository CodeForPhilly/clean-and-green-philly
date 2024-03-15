"use client";

import { NextUIProvider } from "@nextui-org/react";
import { FC } from "react";
import LegalDisclaimerPage from "./LegalDisclaimerPage";

const LegalDisclaimer: FC = () => {
  return (
    <NextUIProvider>
      <LegalDisclaimerPage />
    </NextUIProvider>
  );
};

export default LegalDisclaimer;
