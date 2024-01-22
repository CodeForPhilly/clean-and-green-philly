'use client';

import React, { FC } from "react";
import { NextUIProvider } from "@nextui-org/react";
import Layout from "../components/Layout";
import MethodologyPage from "../components/MethodologyPage";

const Methodology: FC = () => {
  return (
    <NextUIProvider>
      <Layout>
        <MethodologyPage />
      </Layout>
    </NextUIProvider>
  );
};

export default Methodology;
