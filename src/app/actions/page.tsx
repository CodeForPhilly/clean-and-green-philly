"use client";

import React, { FC } from "react";
import { NextUIProvider } from "@nextui-org/react";
import Header from "../components/Header";
import RecommendedActions from "../components/RecommendedActions";

const Actions: FC = () => {
  return (
    <NextUIProvider>
      <div className="h-screen">
        <Header />
        <RecommendedActions />
      </div>
    </NextUIProvider>
  );
};

export default Actions;
