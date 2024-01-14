"use client";

import React, { FC } from "react";
import { NextUIProvider } from "@nextui-org/react";
import Header from "../components/Header";
import LegalDisclaimerPage from "../components/LegalDisclaimerPage";
import Footer from "../components/Footer";

const GetAccess: FC = () => {
  return (
    <NextUIProvider>
      <div className="h-screen">
        <Header />
        <LegalDisclaimerPage />
        <Footer />
      </div>
    </NextUIProvider>
  );
};

export default GetAccess;
