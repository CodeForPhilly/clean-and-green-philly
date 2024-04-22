import { Footer, Header, Hotjar } from "@/components";

const ContentPagesLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <>
      <Header />
      <main id="main">
        <div className="max-w-[68.75rem] mx-auto pb-[30px] pt-[60px] w-[90%]">
            {children}
        </div>
      </main>
      <Footer />
      <Hotjar />
    </>
  );
};
export default ContentPagesLayout;
