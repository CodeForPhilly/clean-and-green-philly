"use client";

import { NextUIProvider } from "@nextui-org/react";
import { FC } from "react";
import AccessibilityStatementPage from "./AccessibilityStatementPage";

const LegalDisclaimer: FC = () => {
  return (
    <NextUIProvider>
      <AccessibilityStatementPage />
    </NextUIProvider>
  );
};

export default LegalDisclaimer;
