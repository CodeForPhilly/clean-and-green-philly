"use client";

import { NextUIProvider } from "@nextui-org/react";
import { FC } from "react";
import LandingPage from "./components/LandingPage";
import Layout from "./components/Layout";

const Page: FC = () => {
  return (
    <NextUIProvider>
      <Layout>
        <title>Clean and Green Philly</title>
        <LandingPage />
      </Layout>
    </NextUIProvider>
  );
};

export default Page;
