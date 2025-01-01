'use client';

import { Button, NavbarItem } from '@nextui-org/react';
import { usePathname } from 'next/navigation';
import Link from 'next/link';

interface IconLinkProps {
  icon: React.ReactElement;
  text: string;
  href: string;
}

function IconLink({ icon, text, href }: IconLinkProps) {
  const pathname = usePathname();
  return (
    <NavbarItem
      isActive={pathname === href}
      aria-current={pathname === href ? 'page' : undefined}
      key={text}
      className={
        pathname === href
          ? 'active-state-nav flex items-center justify-center'
          : ''
      }
    >
      <Button
        as={Link}
        disableRipple={true}
        href={href}
        role="link"
        // *only include if there will be no text link present* aria-label={text}
        startContent={<div className="linkIcon">{icon}</div>}
        className={
          pathname === href
            ? 'active-state-nav gap-0'
            : 'iconLink bg-color-none gap-0'
        }
        // className="flex text-gray-900 items-center active:bg-[#E9FFE5] active:text-green-700 focus:text-green-700 focus:bg-[#E9FFE5] hover:gray-100 bg-color-none hover:bg-gray-10"
      >
        <span className="body-md">{text}</span>
      </Button>
    </NavbarItem>
  );
}

export default IconLink;
