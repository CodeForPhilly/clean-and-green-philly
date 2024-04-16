"use client";

import {
  Link,
  Navbar,
  NavbarBrand,
  NavbarContent,
  NavbarMenu,
  NavbarMenuToggle,
} from "@nextui-org/react";
import { PiBinoculars, PiKey, PiTree, PiInfo, PiList } from "react-icons/pi";
import Image from "next/image";
import React, { FC } from "react";
import IconLink from "./IconLink";
const MobileNav: FC = () => {
  const [isMenuOpen, setIsMenuOpen] = React.useState(false);

  return (
    <Navbar
      className="min-[850px]:hidden h-24"
      isBlurred={false}
      onMenuOpenChange={setIsMenuOpen}
      maxWidth="full"
    >
      <NavbarContent>
        <NavbarBrand>
          <Link href="/">
            <Image
              src="/logo.svg"
              alt="Clean &amp; Green Philly Logo"
              width={100}
              height={65}
            />
          </Link>
        </NavbarBrand>

        <NavbarMenuToggle
          aria-label={isMenuOpen ? "Close menu" : "Open menu"}
          className="min-[850px]:hidden flex-end w-fit"
          icon={
            <div className="flex">
              <PiList className="h-6 w-6" /> Menu
            </div>
          }
        ></NavbarMenuToggle>
      </NavbarContent>

      <NavbarMenu className="left-2/4 z-75 px-0 w-fit mobileIconLinkNav">
        <IconLink
          icon={<PiBinoculars className="h-6 w-6" />}
          text="Find Properties"
          href="/find-properties"
        />
        <IconLink
          icon={<PiKey className="h-6 w-6" />}
          text="Get Access"
          href="/get-access"
        />
        <IconLink
          icon={<PiTree className="h-6 w-6" />}
          text="Transform"
          href="/transform-property"
        />
        <IconLink
          icon={<PiInfo className="h-6 w-6" />}
          text="About"
          href="/about"
        />
      </NavbarMenu>
    </Navbar>
  );
};

export default MobileNav;
