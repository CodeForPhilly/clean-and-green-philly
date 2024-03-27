"use client";

import { NextUIProvider } from "@nextui-org/react";
import { FC } from "react";
import MethodologyPage from "./MethodologyPage";

const Methodology: FC = () => {
  return (
    <NextUIProvider>
      <MethodologyPage />
    </NextUIProvider>
  );
};

export default Methodology;
