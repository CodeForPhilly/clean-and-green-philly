import { Footer, Header, Hotjar } from "@/components";

const ContentPagesLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <>
      <Header />
      <main id="main">{children}</main>
      <Footer />
      <Hotjar />
    </>
  );
};
export default ContentPagesLayout;
