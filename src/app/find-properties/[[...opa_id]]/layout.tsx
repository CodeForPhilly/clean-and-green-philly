import { Header, Hotjar } from "@/components";
import { generateMetadata } from "@/utilities/generateMetaData";
import CookieConsentBanner from "@/components/CookieConsentBanner";

const title = "Find Properties";
const url = "/find-properties";
const description =
  "You can search and find vacant properties that match your goals. Use our data to understand those properties and how to take action."; //?

export const metadata = generateMetadata({
  title,
  url,
  description,
});
const MapLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="overflow-hidden">
      <Header />
      <main id="main">{children}</main>
      <Hotjar />
      <CookieConsentBanner />
    </div>
  );
};
export default MapLayout;
