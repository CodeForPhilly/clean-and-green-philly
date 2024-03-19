"use client";

import { NextUIProvider } from "@nextui-org/react";
import { FC } from "react";
import TakeActionOverviewPage from "./TakeActionOverviewPage";

const TakeActionOverview: FC = () => {
  return (
    <NextUIProvider>
      <TakeActionOverviewPage />
    </NextUIProvider>
  );
};

export default TakeActionOverview;
