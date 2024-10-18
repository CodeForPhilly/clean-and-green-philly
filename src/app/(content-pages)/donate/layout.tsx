import { generateMetadata } from '@/utilities/generateMetaData';

const title = 'Donate';
const description = 'Donate to support Clean & Green Philly';
const url = '/donate';

export const metadata = generateMetadata({
  title,
  description,
  url,
});

const DonateLayout = ({ children }: { children: React.ReactNode }) => {
  return <>{children}</>;
};
export default DonateLayout;
