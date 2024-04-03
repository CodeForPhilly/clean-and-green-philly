import { Footer, Header, Hotjar } from "@/components";

export const metadata = {
  title: "Find Properties",
};

const MapLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="overflow-hidden">
      <Header />
      <main id="main">{children}</main>
      <Hotjar />
    </div>
  );
};
export default MapLayout;
