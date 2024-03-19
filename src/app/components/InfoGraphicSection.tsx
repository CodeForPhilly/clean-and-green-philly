import { Button } from "@nextui-org/react";
import { Icon } from "@phosphor-icons/react";
import Image, { StaticImageData } from "next/image";
import Link from "next/link";

interface InfoGraphicBase {
  id?: string;
  header: {
    text: string | JSX.Element;
    as?: "h2" | "div";
  };
  body: { text: string | JSX.Element; className?: string };
  link?: {
    icon: Icon;
    label: string;
    href: string;
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
  const HeaderTag = headerAs || "h2";

  // Dynamically renders the graphic content based on prop type.
  const renderGraphicContent = () => {
    if ("image" in props) {
      return (
        <Image
          src={props.image.data}
          alt={props.image.alt || ""}
          className={`w-full rounded-[8px] ${
            props.image.className && props.image.className
          }`}
          priority={(props.image.priority && props.image.priority) || false}
          placeholder={"blur"}
        />
      );
    } else if ("component" in props) {
      return props.component;
    }
  };

  return (
    <div className="grid lg:grid-cols-2 gap-[60px] items-center">
      <div className="space-y-5">
        <HeaderTag id={id} className="heading-2xl text-pretty">
          {headerText}
        </HeaderTag>
        <div className={body.className || ""}>
          <p className="body-md text-balance">{body.text}</p>
          {link && (
            <Button
              role="link"
              href={link.href}
              as={Link}
              className="bg-gray-200 iconLink mt-5"
            >
              <link.icon className="w-5 h-5" />
              <span className="body-md">{link.label}</span>
            </Button>
          )}
        </div>
      </div>
      <div>{renderGraphicContent()}</div>
    </div>
  );
};
