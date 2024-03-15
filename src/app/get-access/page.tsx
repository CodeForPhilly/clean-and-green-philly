"use client";

import React, { FC } from "react";
import { NextUIProvider } from "@nextui-org/react";
import Layout from "../../components/Layout";
import GetAccessPage from "../../components/GetAccessPage";

const GetAccess: FC = () => {
  return (
    <NextUIProvider>
      <Layout>
        <title>Get Access - Clean and Green Philly</title>
        <GetAccessPage />
      </Layout>
    </NextUIProvider>
  );
};

export default GetAccess;
