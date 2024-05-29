import { Header, Hotjar } from "@/components";
import { generateMetadata } from "@/utilities/generateMetaData";

const title = "Find Properties";
const url = "/find-properties";
//descrption?

export const metadata = generateMetadata({
  title,
  url,
});
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
