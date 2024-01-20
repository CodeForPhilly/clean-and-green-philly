"use client";

import React, { FC } from "react";
import { NextUIProvider } from "@nextui-org/react";
import Header from "../components/Header";
import MethodologyPage from "../components/MethodologyPage";
import Footer from "../components/Footer";

const Methodology: FC = () => {
  return (
    <NextUIProvider>
      <div className="h-screen">
        <Header />
        <MethodologyPage />
        <Footer />
      </div>
    </NextUIProvider>
  );
};

export default Methodology;