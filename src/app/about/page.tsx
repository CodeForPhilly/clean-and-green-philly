"use client";

import React, { FC } from "react";
import { NextUIProvider } from "@nextui-org/react";
import Header from "../components/Header";
import AboutPage from "../components/AboutPage";

const About: FC = () => {
  return (
    <NextUIProvider>
      <div className="h-screen">
        <Header />
        <AboutPage />
      </div>
    </NextUIProvider>
  );
};

export default About;
