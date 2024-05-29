import { generateMetadata } from "@/utilities/generateMetaData";

const title = "Methodology";
const description =
  "Clean & Green Philly combines several public datasets in order to categorize Philadelphia’s vacant properties."; //thoughts?
const url = "/methodology";

export const metadata = generateMetadata({
  title,
  description,
  url,
});

const MethodologyLayout = ({ children }: { children: React.ReactNode }) => {
  return <>{children}</>;
};
export default MethodologyLayout;
