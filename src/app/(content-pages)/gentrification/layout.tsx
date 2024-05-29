import { generateMetadata } from "@/utilities/generateMetaData";

const title = "Gentrification";
const url = "/gentrification";
//add description?

export const metadata = generateMetadata({
  title,
  url,
});

const GentrificationLayout = ({ children }: { children: React.ReactNode }) => {
  return <>{children}</>;
};
export default GentrificationLayout;
