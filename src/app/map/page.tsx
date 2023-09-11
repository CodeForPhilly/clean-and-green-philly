"use client";

import React, { FC } from "react";
import { NextUIProvider } from "@nextui-org/react";
import Header from "../components/Header";
import PropertyMap from "../components/PropertyMap";

const Page: FC = () => {
  return (
    <NextUIProvider>
      <div className="h-screen overflow-hidden">
        <Header />
        <PropertyMap />
      </div>
    </NextUIProvider>
  );
};

export default Page;
