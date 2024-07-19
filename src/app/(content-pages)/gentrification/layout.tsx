import { generateMetadata } from '@/utilities/generateMetaData';

const title = 'Gentrification';
const url = '/gentrification';
const description =
  'At Clean & Green Philly, we try to avoid contributing to green gentrification here in Philadelphia.';

export const metadata = generateMetadata({
  title,
  url,
  description,
});

const GentrificationLayout = ({ children }: { children: React.ReactNode }) => {
  return <>{children}</>;
};
export default GentrificationLayout;
