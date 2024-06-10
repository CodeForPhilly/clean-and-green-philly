import { generateMetadata } from "@/utilities/generateMetaData";

const title = "Legal Disclaimer";
const description = "Acceptance of Terms and Conditions of Use";
const url = "/legal-disclaimer";

export const metadata = generateMetadata({
  title,
  description,
  url,
});

const LegalDisclaimerLayout = ({ children }: { children: React.ReactNode }) => {
  return <>{children}</>;
};
export default LegalDisclaimerLayout;
