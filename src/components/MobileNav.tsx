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
      className="min-[850px]:hidden bg-white h-24"
      isBlurred={false}
      onMenuOpenChange={setIsMenuOpen}
      maxWidth="full"
    >
      <NavbarContent className="max-sm:px-0">
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
              <>
              <PiList className="h-6 w-6 linkIcon" /> Menu
              </>
          }
        > </NavbarMenuToggle>
      </NavbarContent>
      
      {/* 181.1 (width of menu) + 48px offset padding + 6px = 235.1 */}
      <NavbarMenu className="top-20 left-[calc(100vw-235.1px)] z-75 px-0 w-fit mobileIconLinkNav">
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
