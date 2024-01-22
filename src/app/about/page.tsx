'use client';

import React, { FC } from "react";
import { NextUIProvider } from "@nextui-org/react";
import Layout from "../components/Layout";
import AboutPage from "../components/AboutPage";

const About: FC = () => {
  return (
    <NextUIProvider>
      <Layout>
        <AboutPage />
      </Layout>
    </NextUIProvider>
  );
};

export default About;
