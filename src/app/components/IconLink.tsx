"use client";
import { usePathname } from "next/navigation";
import React, { FC, ReactElement } from "react";
import { Button, Link, NavbarItem } from "@nextui-org/react";
import { useRouter } from "next/navigation";

interface IconLinkProps {
  icon: ReactElement;
  text: string;
  href: string;
}

function IconLink({ icon, text, href }: any) {
  const pathname = usePathname();
  return (
    <NavbarItem
      isActive={pathname === href}
      aria-current={pathname === href ? "true" : undefined}
      key={text}
      className={pathname === href ? "active-state-nav" : ""}
    >
      <Button
        as={Link}
        disableRipple={true}
        href={href}
        role="link"
        // *only include if there will be no text link present* aria-label={text}
        startContent={<div className="linkIcon">{icon}</div>}
        className={
          pathname === href ? "active-state-nav" : "iconLink bg-color-none"
        }
        // className="flex text-gray-900 items-center active:bg-[#E9FFE5] active:text-green-700 focus:text-green-700 focus:bg-[#E9FFE5] hover:gray-100 bg-color-none hover:bg-gray-10"
      >
        <span className="body-md">{text}</span>
      </Button>
    </NavbarItem>
  );
}

export default IconLink;
