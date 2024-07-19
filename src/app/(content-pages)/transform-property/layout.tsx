import { generateMetadata } from '@/utilities/generateMetaData';

const title = 'Transform a Property';
const description =
  'After gaining access to the property, you can transform a property to improve the quality of life in the neighborhood.';
const url = '/transform-property';

export const metadata = generateMetadata({
  title,
  description,
  url,
});

const TransformPropertyLayout = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  return <>{children}</>;
};
export default TransformPropertyLayout;
