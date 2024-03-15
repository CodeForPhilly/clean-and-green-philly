"use client";

import React, { FC } from "react";
import { NextUIProvider } from "@nextui-org/react";
import Layout from "../../components/Layout";
import LegalDisclaimerPage from "../../components/LegalDisclaimerPage";

const LegalDisclaimer: FC = () => {
  return (
    <NextUIProvider>
      <Layout>
        <title>Legal Disclaimer - Clean and Green Philly</title>
        <LegalDisclaimerPage />
      </Layout>
    </NextUIProvider>
  );
};

export default LegalDisclaimer;
