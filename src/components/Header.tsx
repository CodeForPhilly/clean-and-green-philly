import { Navbar, NavbarBrand, NavbarContent } from "@nextui-org/react";
import { PiBinoculars, PiKey, PiTree, PiInfo } from "react-icons/pi";
import Image from "next/image";
import Link from "next/link";
import IconLink from "./IconLink";
import MobileNav from "./MobileNav";

// Apply multiple CSS classes using CSS Modules
// const buttonClasses = `${styles.button} ${primary ? styles.primary : ""} ${
//   large ? styles.large : ""
// }`;


const Header = () => (
  //blurred here? 
  <Navbar maxWidth="full" position="sticky" height="auto" isBordered className="max-[850px]:backdrop-blur-none">
    <MobileNav />
    <NavbarContent
      className="hidden min-[850px]:flex basis-1/5 sm:basis-full"
      style={{
        paddingTop: "16px",
        paddingBottom: "16px",
        paddingLeft: "32px"
      }}
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
    </NavbarContent>
  </Navbar>
);

export default Header;
