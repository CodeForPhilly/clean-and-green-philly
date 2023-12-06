import {
  Navbar,
  NavbarContent,
  NavbarBrand,
  NavbarItem,
} from "@nextui-org/react";
import IconLink from "./IconLink";
import Link from 'next/link';
import {
  HomeIcon,
  MapIcon,
  QuestionMarkCircleIcon,
  InformationCircleIcon,
  BoltIcon,
} from "@heroicons/react/20/solid";

const navbarButtons = [
  {
    icon: <HomeIcon />,
    text: "Intro",
    href: "/",
  },
  {
    icon: <MapIcon />,
    text: "Map",
    href: "/map",
  },
  {
    icon: <BoltIcon />,
    text: "Take Action",
    href: "/actions",
  },
  {
    icon: <InformationCircleIcon />,
    text: "About",
    href: "/about",
  },
];

const Header = () => (
  <Navbar maxWidth="full" position="sticky">
    <NavbarContent className="basis-1/5 sm:basis-full" justify="start">
      <NavbarBrand>
        <Link href="/"> 
          <span className="font-bold text-3xl">
            Clean & Green Philly
          </span>
        </Link>
        <span className="text-sm text-gray-600 ml-4">
          Clean and green vacant properties
          <br /> to reduce gun crime.
        </span>
      </NavbarBrand>
    </NavbarContent>

    <NavbarContent
      className="hidden sm:flex basis-1/5 sm:basis-full"
      justify="end"
    >
      {navbarButtons.map(({ icon, text, href }) => (
        <NavbarItem key={text}>
          <IconLink icon={icon} text={text} href={href} />
        </NavbarItem>
      ))}
    </NavbarContent>
  </Navbar>
);

export default Header;
