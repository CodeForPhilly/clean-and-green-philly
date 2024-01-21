'use client';

import React, { FC } from "react";
import { NextUIProvider } from "@nextui-org/react";
import Layout from "../components/Layout";
import GetAccessPage from "../components/GetAccessPage";

const GetAccess: FC = () => {
  return (
    <NextUIProvider>
      <Layout>
        <GetAccessPage />
      </Layout>
    </NextUIProvider>
  );
};

export default GetAccess;
