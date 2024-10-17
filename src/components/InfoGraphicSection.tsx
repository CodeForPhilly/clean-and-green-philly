import Image, { StaticImageData } from 'next/image';
import type { IconType } from 'react-icons';
import { ThemeButtonLink } from './ThemeButton';
import './components-css/InfoGraphicSection.css';

interface InfoGraphicBase {
  id?: string;
  header: {
    text: string | JSX.Element;
    as?: 'h2' | 'div';
  };
  body: { text: string | JSX.Element; className?: string };
  link?: {
    icon: IconType;
    label: string;
    href: string;
    color?: 'primary' | 'secondary' | 'tertiary';
  };
}

interface InfoGraphicWithImage extends InfoGraphicBase {
  image: {
    data: StaticImageData;
    alt?: string;
    className?: string;
    priority?: boolean;
  };
}

interface InfoGraphicWithComponent extends InfoGraphicBase {
  component: JSX.Element;
}

type InfoGraphicProps = InfoGraphicWithImage | InfoGraphicWithComponent;

/**
 * Renders an info graphic section with a header, body text, and optional link and graphic content,
 * depending on the usage of the 'image' or 'component' prop.
 *
 * Initially developed for use on the 'pitch deck' landing page.
 */
export const InfoGraphicSection = (props: InfoGraphicProps) => {
  const {
    id,
    header: { text: headerText, as: headerAs },
    body,
    link,
  } = props;
  const HeaderTag = headerAs || 'h2';

  // Dynamically renders the graphic content based on prop type.
  const renderGraphicContent = () => {
    if ('image' in props) {
      return (
        <div className={'p-5'}>
          <Image
            src={props.image.data}
            alt={props.image.alt || ''}
            className={`w-full rounded-[20px] info-graphic ${
              props.image.className && props.image.className
            }`}
            priority={(props.image.priority && props.image.priority) || false}
            placeholder={'blur'}
          />
        </div>
      );
    } else if ('component' in props) {
      return props.component;
    }
  };

  return (
    <div className="grid lg:grid-cols-2 gap-[60px] items-center">
      <div className="space-y-5">
        <HeaderTag id={id} className="heading-2xl text-pretty">
          {headerText}
        </HeaderTag>
        <div className={body.className || ''}>
          <p className="body-md text-balance">{body.text}</p>
          {link && (
            <ThemeButtonLink
              href={link.href}
              label={link.label}
              color={link.color}
              startContent={<link.icon />}
              className="max-w-min mt-5"
            />
          )}
        </div>
      </div>
      <div>{renderGraphicContent()}</div>
    </div>
  );
};
