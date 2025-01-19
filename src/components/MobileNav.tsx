'use client';

import {
  Link,
  Navbar,
  NavbarBrand,
  NavbarContent,
  NavbarMenu,
  NavbarMenuToggle,
} from '@nextui-org/react';
import {
  PiBinoculars,
  PiKey,
  PiTree,
  PiInfo,
  PiList,
  PiHeart,
} from 'react-icons/pi';
import Image from 'next/image';
import React, { FC } from 'react';
import IconLink from './IconLink';
const MobileNav: FC = () => {
  const [isMenuOpen, setIsMenuOpen] = React.useState(false);

  return (
    <Navbar
      className="min-[850px]:hidden h-24 -mx-1"
      onMenuOpenChange={setIsMenuOpen}
      as="div"
      maxWidth="full"
    >
      <NavbarContent as="div" className="max-sm:px-0">
        <NavbarBrand as="div">
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
          as="nav"
          aria-label={isMenuOpen ? 'Close menu' : 'Open menu'}
          className="min-[850px]:hidden flex-end w-fit"
          tabIndex={0}
          icon={
            <>
              <PiList className="h-6 w-6 linkIcon" /> Menu
            </>
          }
        >
          {' '}
        </NavbarMenuToggle>
      </NavbarContent>

      {/* (181.1 (width of menu) + 48px offset padding = 235.1) - 12px */}
      <NavbarMenu
        className="top-20 left-[calc(100vw-223.1px)] z-75 px-0 w-fit mobileIconLinkNav"
        as="nav"
        aria-label="primary"
      >
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
        <IconLink
          icon={<PiHeart className="h-6 w-6" />}
          text="Donate"
          href="/donate"
        />
      </NavbarMenu>
    </Navbar>
  );
};

export default MobileNav;
