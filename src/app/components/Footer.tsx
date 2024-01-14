import { Navbar, NavbarContent, NavbarBrand, NavbarItem } from "@nextui-org/react";

const Footer = () => (
  <div className="flex flex-col min-h-screen">
    <div className="flex-grow"></div>
    <Navbar maxWidth="full">
      <NavbarContent className="flex justify-between items-center w-full">
        <NavbarItem>
          <span className="text-sm text-gray-600">
            © 2024 Clean & Green Philly
          </span>
        </NavbarItem>

        <NavbarItem className="text-sm underline text-gray-600 mx-auto">
          <a href="/legal-disclaimer" className="hover:text-gray-800">
            Legal Disclaimer
          </a>
        </NavbarItem>

        <NavbarItem>
          <a href="mailto:cleangreenphilly@gmail.com" className="text-sm underline text-gray-600 hover:text-gray-800">
            Contact Us
          </a>
        </NavbarItem>
      </NavbarContent>
    </Navbar>
  </div>
);

export default Footer;