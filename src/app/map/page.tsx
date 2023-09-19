"use client";

import React, { FC, useState } from "react";
import { NextUIProvider, Button } from "@nextui-org/react";
import Header from "../components/Header";
import PropertyMap from "../components/PropertyMap";
import PropertyDetailSection from "../components/PropertyDetailSection";

const Page: FC = () => {
  const [featuresInView, setFeaturesInView] = useState<any[]>([]);
  return (
    <NextUIProvider>
      <div className="h-screen overflow-hidden">
        <Header />
        <div className="flex h-full relative">
          <div className="flex-grow h-full">
            <PropertyMap setFeaturesInView={setFeaturesInView} />
          </div>
          <PropertyDetailSection featuresInView={featuresInView} />
        </div>
      </div>
    </NextUIProvider>
  );
};

export default Page;
