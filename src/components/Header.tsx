import { Navbar, NavbarBrand, NavbarContent } from "@nextui-org/react";
import { PiBinoculars, PiKey, PiTree, PiInfo } from "react-icons/pi";
import { ThemeButton, ThemeButtonLink } from "./ThemeButton";
import Image from "next/image";
import Link from "next/link";
import IconLink from "./IconLink";
import MobileNav from "./MobileNav";

// Apply multiple CSS classes using CSS Modules
// const buttonClasses = `${styles.button} ${primary ? styles.primary : ""} ${
//   large ? styles.large : ""
// }`;

const Header = () => (
  <>
    <MobileNav />
    <Navbar className="px-1" maxWidth="full" position="sticky" height="auto" as="div" isBordered>
      <NavbarContent
        as="div"
        className="hidden min-[850px]:flex basis-1/5 sm:basis-full py-4"
        justify="start"
      >
        <NavbarBrand>
          <Link href="/">
            <Image
              src="/logo.svg"
              alt="Clean &amp; Green Philly Logo"
              width={112}
              height={67}
            />
          </Link>
        </NavbarBrand>
      </NavbarContent>

      <NavbarContent
        className="hidden min-[850px]:flex basis-1/5 sm:basis-full"
        justify="end"
        as="nav"
        aria-label="primary"
      >
        <ul className="flex flex-row">
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
        </ul>
      </NavbarContent>
    </Navbar>
  </>
);

export default Header;
