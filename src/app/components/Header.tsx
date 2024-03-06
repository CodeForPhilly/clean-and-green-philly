import {
  Navbar,
  NavbarContent,
  NavbarBrand,
  NavbarItem,
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownItem,
  Button,
} from "@nextui-org/react";
import IconLink from "./IconLink";
import Link from "next/link";
import Image from "next/image";
import { MapPin, Hand, Info } from "@phosphor-icons/react";

const Header = () => (
  <Navbar maxWidth="full" position="sticky" height="auto" isBordered>
    <NavbarContent
      className="hidden sm:flex basis-1/5 sm:basis-full"
      style={{ paddingTop: "16px", paddingBottom: "16px", paddingLeft: "32px" }}
      justify="start"
    >
      <NavbarBrand>
        <Link href="/">
          <Image
            src="/logo.svg"
            alt="Clean & Green Philly Logo"
            width={112}
            height={67}
          />
        </Link>
      </NavbarBrand>
    </NavbarContent>

    <NavbarContent
      className="hidden sm:flex basis-1/5 sm:basis-full"
      justify="end"
    >
      <NavbarItem key="Find Properties">
        <IconLink
          icon={<MapPin className="h-6 w-6" />}
          text="Find Properties"
          href="/map"
        />
      </NavbarItem>

      {/* Dropdown for Take Action */}
      <Dropdown>
        <DropdownTrigger>
          <Button
            size="md"
            className="flex items-center focus:text-blue-500 focus:underline hover:text-blue-500 hover:underline bg-white"
          >
            <Hand className="h-6 w-6" aria-hidden="true" />
            <span className="body-md">Take Action</span>
          </Button>
        </DropdownTrigger>
        <DropdownMenu aria-label="Take Action">
          <DropdownItem href="/take-action-overview">Overview</DropdownItem>
          <DropdownItem href="/get-access">Get Access</DropdownItem>
          <DropdownItem href="/transform-property">
            Transform a Property
          </DropdownItem>
        </DropdownMenu>
      </Dropdown>

      {/* Dropdown for About */}
      <Dropdown>
        <DropdownTrigger>
          <Button
            size="md"
            className="flex items-center focus:text-blue-500 focus:underline hover:text-blue-500 hover:underline bg-white"
          >
            <Info className="h-6 w-6" aria-hidden="true" />
            <span className="body-md">About</span>
          </Button>
        </DropdownTrigger>
        <DropdownMenu aria-label="Overview">
          <DropdownItem href="/about">Overview</DropdownItem>
          <DropdownItem href="/methodology">Methodology</DropdownItem>
        </DropdownMenu>
      </Dropdown>
    </NavbarContent>
  </Navbar>
);

export default Header;
