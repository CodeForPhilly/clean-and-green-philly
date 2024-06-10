import { generateMetadata } from "@/utilities/generateMetaData";

const title = "Request Removal";
const description = "Request to Remove a Property Listing";
const url = "/request-removal";

export const metadata = generateMetadata({
  title,
  description,
  url,
});

const RequestRemovalLayout = ({ children }: { children: React.ReactNode }) => {
  return <>{children}</>;
};
export default RequestRemovalLayout;
