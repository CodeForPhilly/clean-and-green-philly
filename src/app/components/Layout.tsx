'use client';

import React, { FC, ReactNode } from "react";
import Header from "./Header";
import Footer from "./Footer";
import Hotjar from "./Hotjar";

interface LayoutProps {
  children: ReactNode;
}

const Layout: FC<LayoutProps> = ({ children }) => {
  return (
    <div className="h-screen">
      <Header />
      {children}
      <Footer />
      <Hotjar />
    </div>
  );
};

export default Layout;
