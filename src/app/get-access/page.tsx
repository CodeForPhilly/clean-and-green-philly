"use client";

import React, { FC } from "react";
import { NextUIProvider } from "@nextui-org/react";
import Header from "../components/Header";
import GetAccessPage from "../components/GetAccessPage";
import Footer from "../components/Footer";

const GetAccess: FC = () => {
  return (
    <NextUIProvider>
      <div className="h-screen">
        <Header />
        <GetAccessPage />
        <Footer />
      </div>
    </NextUIProvider>
  );
};

export default GetAccess;
