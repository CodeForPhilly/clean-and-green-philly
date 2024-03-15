"use client";

import { NextUIProvider } from "@nextui-org/react";
import { FC } from "react";
import TransformPropertyPage from "./TransformPropertyPage";

const TransformProperty: FC = () => {
  return (
    <NextUIProvider>
      <TransformPropertyPage />
    </NextUIProvider>
  );
};

export default TransformProperty;
