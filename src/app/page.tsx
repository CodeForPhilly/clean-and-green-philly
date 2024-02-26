"use client";

import React, { FC } from "react";
import { NextUIProvider } from "@nextui-org/react";
import Header from "./components/Header";
import LandingPage from "./components/LandingPage";
import Footer from "./components/Footer";
import Hotjar from "./components/Hotjar";

const Page: FC = () => {
  return (
    <NextUIProvider>
      <div className="flex flex-col min-h-screen overflow-hidden">
      <a className="font-bold border-solid border-black bg-white transition left-0 absolute p-3 m-3 -translate-y-16 focus:translate-y-0 z-50" href="#main" tabIndex={0}>Skip to main content</a>
        <Header />
        <main id="main" className="flex-grow">
          <LandingPage />
        </main>
        <Footer />
        <Hotjar />
      </div>
    </NextUIProvider>
  );
};

export default Page;
