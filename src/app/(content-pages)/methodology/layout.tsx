import { generateMetadata } from '@/utilities/generateMetaData';

const title = 'Methodology';
const description =
  'Clean & Green Philly combines several public datasets to categorize Philadelphia’s vacant properties based on how important it is that someone intervene there.';
const url = '/methodology';

export const metadata = generateMetadata({
  title,
  description,
  url,
});

const MethodologyLayout = ({ children }: { children: React.ReactNode }) => {
  return <>{children}</>;
};
export default MethodologyLayout;
