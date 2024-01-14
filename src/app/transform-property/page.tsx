"use client";

import React, { FC } from "react";
import { NextUIProvider } from "@nextui-org/react";
import Header from "../components/Header";
import TransformPropertyPage from "../components/TransformPropertyPage";
import Footer from "../components/Footer";

const TransformProperty: FC = () => {
  return (
    <NextUIProvider>
      <div className="h-screen">
        <Header />
        <TransformPropertyPage />
        <Footer />
      </div>
    </NextUIProvider>
  );
};

export default TransformProperty;
