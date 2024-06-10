import { generateMetadata } from "@/utilities/generateMetaData";

const title = "Overview";
const description =
  "Clean & Green Philly can help you prioritize vacant properties to return to productive use.";
const url = "/take-action-overview";

export const metadata = generateMetadata({
  title,
  description,
  url,
});

const OverviewLayout = ({ children }: { children: React.ReactNode }) => {
  return <>{children}</>;
};
export default OverviewLayout;
