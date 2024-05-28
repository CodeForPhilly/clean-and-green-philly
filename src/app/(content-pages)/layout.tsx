"use client";

import { Footer, Header, Hotjar } from "@/components";
import { CookieProvider } from "@/context/CookieContext";

const ContentPagesLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <>
      <CookieProvider>
        <Header />
        <main id="main">
          <div className="max-w-[68.75rem] mx-auto pb-[30px] pt-[60px] w-[90%]">
            {children}
          </div>
        </main>
        <Footer />
        <Hotjar />
      </CookieProvider>
    </>
  );
};
export default ContentPagesLayout;
