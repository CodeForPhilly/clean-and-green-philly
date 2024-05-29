import { metadata as globalMetadata } from "../../layout";

const description =
  "Philadelphia has a gun violence problem. Clean & Green Philly empowers Philadelphians to take action to solve it.";
const title = "About";
const ogTitle = `${title} - Clean & Green Philly`;
const url = "/about";

export const metadata = {
  ...globalMetadata,
  title: title,
  description: description,
  openGraph: {
    ...globalMetadata.openGraph,
    title: ogTitle,
    description: description,
    url: url,
  },
};

const AboutLayout = ({ children }: { children: React.ReactNode }) => {
  return <>{children}</>;
};
export default AboutLayout;
