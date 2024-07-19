import { generateMetadata } from '@/utilities/generateMetaData';

const title = 'Get Access';
const description =
  'In order to intervene in a property, you need to have some kind of legal access to do so.';
const url = '/get-access';

export const metadata = generateMetadata({
  title,
  description,
  url,
});

const GetAccessLayout = ({ children }: { children: React.ReactNode }) => {
  return <>{children}</>;
};
export default GetAccessLayout;
