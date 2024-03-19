"use client";

import {
  Link,
  Navbar,
  NavbarBrand,
  NavbarContent,
  NavbarMenu,
  NavbarMenuToggle
} from "@nextui-org/react";
import { Hand, Info, List, MapPin } from "@phosphor-icons/react";
import Image from "next/image";
import React, { FC } from "react";
import IconLink from "./IconLink";
const MobileNav: FC = () => {
  const [isMenuOpen, setIsMenuOpen] = React.useState(false);

  return (
    <Navbar
      className="sm:hidden h-24"
      isBlurred={false}
      onMenuOpenChange={setIsMenuOpen}
    >
      <NavbarContent>
        <NavbarBrand>
          <Link href="/">
            <Image
              src="/logo.svg"
              alt="Clean & Green Philly Logo"
              width={100}
              height={65}
            />
          </Link>
        </NavbarBrand>

        <NavbarMenuToggle
          aria-label={isMenuOpen ? "Close menu" : "Open menu"}
          className="sm:hidden flex-end w-fit"
          icon={
            <div className="flex">
              <List className="h-6 w-6" /> Menu
            </div>
          }
        ></NavbarMenuToggle>
      </NavbarContent>

      <NavbarMenu className="left-2/4 z-50 px-0 w-fit mobileIconLinkNav">
        <IconLink
          icon={<MapPin className="h-6 w-6" />}
          text="Find Properties"
          href="/map"
        />

        <IconLink
          icon={<Hand className="h-6 w-6" />}
          text="Take Action"
          href="/take-action-overview"
        />

        <IconLink
          icon={<Info className="h-6 w-6" />}
          text="About"
          href="/about"
        />
      </NavbarMenu>
    </Navbar>
  );
};

export default MobileNav;
