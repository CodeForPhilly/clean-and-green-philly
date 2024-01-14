"use client";

import React, { FC } from "react";
import { NextUIProvider } from "@nextui-org/react";
import Header from "./components/Header";
import LandingPage from "./components/LandingPage";
import Footer from "./components/Footer";

const Page: FC = () => {
  return (
    <NextUIProvider>
      <div className="h-screen overflow-hidden">
        <Header />
        <LandingPage />
        <Footer />
      </div>
    </NextUIProvider>
  );
};

export default Page;
