'use client';

import React, { FC } from "react";
import { NextUIProvider } from "@nextui-org/react";
import Layout from "../components/Layout";
import TransformPropertyPage from "../components/TransformPropertyPage";

const TransformProperty: FC = () => {
  return (
    <NextUIProvider>
      <Layout>
        <TransformPropertyPage />
      </Layout>
    </NextUIProvider>
  );
};

export default TransformProperty;
