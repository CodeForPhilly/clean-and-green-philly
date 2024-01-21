"use client";

import React, { FC } from "react";
import { NextUIProvider } from "@nextui-org/react";
import Header from "../components/Header";
import RequestRemovalPage from "../components/RequestRemovalPage";
import Footer from "../components/Footer";

const RequestRemoval: FC = () => {
  return (
    <NextUIProvider>
      <div className="h-screen">
        <Header />
        <RequestRemovalPage />
        <Footer />
      </div>
    </NextUIProvider>
  );
};

export default RequestRemoval;
