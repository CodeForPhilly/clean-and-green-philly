const Footer = () => (
  <div className="flex flex-col">
    <footer className="px-6 h-16 flex flex-grow w-full items-center">
      <nav className="w-full" aria-label="content info">
        <ul className="flex justify-between items-center w-full backdrop-saturate-150 bg-background/70">
          <li>
            <span className="base-sm text-gray-600">
              © 2024 Clean & Green Philly
            </span>
          </li>

          <li className="base-sm underline text-gray-600 mx-auto">
            <a href="/legal-disclaimer" className="hover:text-gray-800">
              Legal Disclaimer
            </a>
          </li>

          <li>
            <a
              href="mailto:cleanandgreenphl@gmail.com"
              className="base-sm underline text-gray-600 hover:text-gray-800"
            >
              Contact Us
            </a>
          </li>
        </ul>
      </nav>
    </footer>
  </div>
);

export default Footer;
