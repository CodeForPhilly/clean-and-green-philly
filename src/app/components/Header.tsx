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
      className="hidden sm:flex  sm:basis-full md:w-16"
      justify="end"
    >
      <NavbarItem key="Find Properties">
        <Link href="/map">
          <Button size="md" className="mb-2 text-grey bg-white hover:bg-slate-300  focus:outline-none  font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" className="w-6 h-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
              <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z" />
            </svg>
            <text>
            Find properties
            </text>
          </Button>
        </Link>
      </NavbarItem>

      {/* Dropdown for Take Action */}
      <Dropdown>
        <DropdownTrigger>
          <Button
            size="md"
            className="flex items-center hover:text-grey-500 hover:bg-slate-300 bg-white"
          >
            <Hand className="h-6 w-6" aria-hidden="true" />
            Take Action
          </Button>
        </DropdownTrigger>
        <DropdownMenu aria-label="Take Action">
          <DropdownItem key="overview">
            <Link href="/take-action-overview">Overview</Link>
          </DropdownItem>
          <DropdownItem key="get-access">
            <Link href="/get-access">Get Access</Link>
          </DropdownItem>
          <DropdownItem key="transform-property">
            <Link href="/transform-property">Transform a Property</Link>
          </DropdownItem>
        </DropdownMenu>
      </Dropdown>

      {/* Dropdown for About */}
      <Dropdown>
        <DropdownTrigger>
          <Button
            size="md"
            className="flex items-center hover:text-grey-500 hover:bg-slate-300 bg-white"
          >
            <Info className="h-6 w-6" aria-hidden="true" />
            About
          </Button>
        </DropdownTrigger>
        <DropdownMenu aria-label="Overview">
          <DropdownItem key="about">
            <Link href="/about">Overview</Link>
          </DropdownItem>
          <DropdownItem key="methodology">
            <Link href="/methodology">Methodology</Link>
          </DropdownItem>
        </DropdownMenu>
      </Dropdown>
    </NavbarContent>
  </Navbar>
);

export default Header;
