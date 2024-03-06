import React, { FC, ReactElement } from "react";
import { Button, Link } from "@nextui-org/react";

interface IconLinkProps {
  icon: ReactElement;
  text: string;
  href: string;
}

const IconLink: FC<IconLinkProps> = ({ icon, text, href }) => (
  <Button
    as={Link}
    href={href}
    aria-label={text}
    className="flex items-center focus:text-blue-500 focus:underline hover:text-blue-500 hover:underline bg-white"
    startContent={<div className="w-5">{icon}</div>}
  >
    <span className="body-md">{text}</span>
  </Button>
);

export default IconLink;
