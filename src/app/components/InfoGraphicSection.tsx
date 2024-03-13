import { Button } from "@nextui-org/react";
import { Icon } from "@phosphor-icons/react";
import Image, { StaticImageData } from "next/image";
import Link from "next/link";

interface InfoGraphicBase {
  header: string | JSX.Element;
  body: string;
  link?: {
    icon: Icon;
    label: string;
    href: string;
  };
}

interface InfoGraphicWithImage extends InfoGraphicBase {
  image: {
    data: StaticImageData;
    alt: string;
    className?: string;
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
  const { header, body, link } = props;

  // Dynamically renders the graphic content based on prop type.
  const renderGraphicContent = () => {
    if ("image" in props) {
      return (
        <Image
          src={props.image.data}
          alt={props.image.alt}
          className={`max-w-full lg:max-w-[550px] rounded-[8px] ${
            props.image.className && props.image.className
          }`}
        />
      );
    } else if ("component" in props) {
      return props.component;
    }
  };

  return (
    <div className="flex flex-col lg:flex-row gap-[60px] items-center">
      <div className="space-y-5">
        <h2 className="heading-2xl text-pretty">{header}</h2>
        <p className="body-md text-balance">{body}</p>
        {link && (
          <Button
            href={link.href}
            as={Link}
            size="lg"
            className="bg-gray-100 text-black gap-1"
          >
            <link.icon className="w-5 h-5" />
            <span className="body-md">{link.label}</span>
          </Button>
        )}
      </div>
      <div>{renderGraphicContent()}</div>
    </div>
  );
};
