import { Header, Hotjar } from "@/components";
import CookieConsentBanner from "@/components/CookieConsentBanner";

export const metadata = {
  title: "Find Properties",
};

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
