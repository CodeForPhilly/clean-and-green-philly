"use client";

import { NextUIProvider } from "@nextui-org/react";
import { FC } from "react";
import AccessibilityStatementPage from "./AccessibilityStatementPage";

const AccessibilityStatement: FC = () => {
  return (
    <NextUIProvider>
      <AccessibilityStatementPage />
    </NextUIProvider>
  );
};

export default AccessibilityStatement;
