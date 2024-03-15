"use client";

import React, { FC } from "react";
import { NextUIProvider } from "@nextui-org/react";
import Layout from "../../components/Layout";
import TransformPropertyPage from "../../components/TransformPropertyPage";

const TransformProperty: FC = () => {
  return (
    <NextUIProvider>
      <Layout>
        <title>Transform a Property - Clean and Green Philly</title>
        <TransformPropertyPage />
      </Layout>
    </NextUIProvider>
  );
};

export default TransformProperty;
