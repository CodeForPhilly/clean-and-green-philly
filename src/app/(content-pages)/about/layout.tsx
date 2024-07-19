import { generateMetadata } from '@/utilities/generateMetaData';

const title = 'About';
const description =
  'Philadelphia has a gun violence problem. Clean & Green Philly empowers Philadelphians to take action to solve it.';
const url = '/about';

export const metadata = generateMetadata({
  title,
  description,
  url,
});

const AboutLayout = ({ children }: { children: React.ReactNode }) => {
  return <>{children}</>;
};
export default AboutLayout;
