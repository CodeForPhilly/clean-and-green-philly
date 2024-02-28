"use client";

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
      <a className="font-bold border-solid border-black bg-white transition left-0 absolute p-3 m-3 -translate-y-16 focus:translate-y-0 z-50" href="#main" tabIndex={0}>Skip to main content</a>
      <Header />
      <main id="main">
        {children}
      </main>
      <Footer />
      <Hotjar />
    </div>
  );
};

export default Layout;
