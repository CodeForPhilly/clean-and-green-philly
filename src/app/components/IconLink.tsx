import React, { FC, ReactElement } from "react";
import { Button, Link } from "@nextui-org/react";

interface IconLinkProps {
  icon: ReactElement;
  text: string;
  href: string;
}

const IconLink: FC<IconLinkProps> = ({ icon, text, href }) => (
  <Link href={href}>
    <Button
      aria-label={text}
      className="flex items-center hover:text-blue-500 hover:underline bg-white"
      startContent={<div className="w-5">{icon}</div>}
    >
      {text}
    </Button>
  </Link>
);

export default IconLink;
