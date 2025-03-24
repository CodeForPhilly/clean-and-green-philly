'use client';

import { useEffect, useRef, useState } from 'react';

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
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const menuItemsRef = useRef<HTMLButtonElement[]>([]);

  useEffect(() => {
    const handleMenuExit = (event: KeyboardEvent) => {
      if (!isMenuOpen) return;

      const { key } = event;
      if (key === 'Escape' || key === 'Tab') {
        setIsMenuOpen(false);
      }
    };

    document.addEventListener('keydown', handleMenuExit);

    () => {
      document.removeEventListener('keydown', handleMenuExit);
    };
  }, [isMenuOpen]);

  useEffect(() => {
    const handleArrowNavigation = (event: KeyboardEvent) => {
      if (!isMenuOpen) return;

      const { key } = event;
      const currentIndex = menuItemsRef.current.findIndex(
        (item) => item === document.activeElement
      );
      console.log(`Current index ${currentIndex}`);
      console.log(menuItemsRef.current);

      if (key === 'ArrowDown') {
        event.preventDefault();
        const nextIndex = (currentIndex + 1) % menuItemsRef.current.length;
        menuItemsRef.current[nextIndex]?.focus();
        console.log(document.activeElement);
      } else if (key === 'ArrowUp') {
        event.preventDefault();
        const prevIndex =
          (currentIndex - 1 + menuItemsRef.current.length) %
          menuItemsRef.current.length;
        menuItemsRef.current[prevIndex]?.focus();
      }
    };

    document.addEventListener('keydown', handleArrowNavigation);
    return () => {
      document.removeEventListener('keydown', handleArrowNavigation);
    };
  }, [isMenuOpen]);

  return (
    <Navbar
      className="min-[850px]:hidden h-24 -mx-1"
      isMenuOpen={isMenuOpen}
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
        />
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
          refFunction={(node) => {
            menuItemsRef.current[0] = node!;
          }}
        />
        <IconLink
          icon={<PiKey className="h-6 w-6" />}
          text="Get Access"
          href="/get-access"
          refFunction={(node) => {
            menuItemsRef.current[1] = node!;
          }}
        />
        <IconLink
          icon={<PiTree className="h-6 w-6" />}
          text="Transform"
          href="/transform-property"
          refFunction={(node) => {
            menuItemsRef.current[2] = node!;
          }}
        />
        <IconLink
          icon={<PiInfo className="h-6 w-6" />}
          text="About"
          href="/about"
          refFunction={(node) => {
            menuItemsRef.current[3] = node!;
          }}
        />
        <IconLink
          icon={<PiHeart className="h-6 w-6" />}
          text="Donate"
          href="/donate"
          refFunction={(node) => {
            menuItemsRef.current[4] = node!;
          }}
        />
      </NavbarMenu>
    </Navbar>
  );
};

export default MobileNav;
