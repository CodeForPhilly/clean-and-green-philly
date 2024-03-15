"use client";

import React, { FC } from "react";
import { NextUIProvider } from "@nextui-org/react";
import Layout from "../../components/Layout";
import TakeActionOverviewPage from "../../components/TakeActionOverviewPage";

const TakeActionOverview: FC = () => {
  return (
    <NextUIProvider>
      <Layout>
        <title>Overview - Clean and Green Philly</title>
        <TakeActionOverviewPage />
      </Layout>
    </NextUIProvider>
  );
};

export default TakeActionOverview;
