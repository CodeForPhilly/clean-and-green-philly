"use client";

import React, { FC } from "react";
import { NextUIProvider } from "@nextui-org/react";
import Layout from "../components/Layout";
import TakeActionOverviewPage from "../components/TakeActionOverviewPage";

const TakeActionOverview: FC = () => {
  return (
    <NextUIProvider>
      <Layout>
        <TakeActionOverviewPage />
      </Layout>
    </NextUIProvider>
  );
};

export default TakeActionOverview;
