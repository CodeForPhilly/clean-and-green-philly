'use client';

import React, { FC } from "react";
import { NextUIProvider } from "@nextui-org/react";
import Layout from "../components/Layout";
import RequestRemovalPage from "../components/RequestRemovalPage";

const RequestRemoval: FC = () => {
  return (
    <NextUIProvider>
      <Layout>
        <RequestRemovalPage />
      </Layout>
    </NextUIProvider>
  );
};

export default RequestRemoval;
