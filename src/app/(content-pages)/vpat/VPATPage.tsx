export default function VPATPage() {
  return (
    <>
      <h1 className="heading-3xl font-bold mb-6">
        Clean & Green Philly Accessibility Conformance Report
      </h1>
      <p className="mb-1 font-bold">
        Based on VPAT® Version 2.5 International Edition
      </p>

      <h2 className="heading-2xl font-semibold my-4">Product Information</h2>
      <p className="mb-1">
        <strong>Name of Product/Version:</strong> Clean & Green Philly
      </p>
      <p className="mb-1 font-bold">Report Date: May 31, 2024</p>
      <p className="mb-1 font-bold">
        Product Description: Free and easy to use online tool empowering
        community groups in Philadelphia to combat gun violence through the
        revitalization of vacant properties via cleaning and greening
        initiatives.
      </p>
      <p className="mb-1">
        <strong>Contact Information:</strong>{" "}
        <ul className="list-disc ml-8 my-2">
          <li>
            {" "}
            <a
              href="mailto:cleanandgreenphl@gmail.com"
              className="underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              cleanandgreenphl@gmail.com
            </a>
          </li>
        </ul>
      </p>
      <p className="mb-1">
        <strong>Notes:</strong> This report is done on May 31, 2024 version of
        the website. It has not been evaluated for mobile devices.
      </p>
      <p className="mb-1">
        <strong>Evaluation Methods Used:</strong>
        <ul className="list-disc ml-8 my-2">
          <li>
            The website is tested using automated accessibility checkers and
            manual testing by accessibility specialists. It was tested on
            desktop computers running Windows 10, and the latest version of Mac
            OS. We evaluated using the latest version of supported browsers
            Safari, Google Chrome, Mozilla Firefox & Microsoft Edge. We
            performed keyboard-only tests and screen readers, including Voice
            Over with Safari on Mac OS, the latest version of NVDA with Firefox
            and Edge, and JAWS 2024 with Chrome and Edge on Windows OS.
          </li>
        </ul>
      </p>
      <p className="mb-1 font-bold">Applicable Standards/Guidelines:</p>
      <p>
        {" "}
        This report covers the degree of conformance for the following
        accessibility standard/guidelines:
      </p>

      <table className="min-w-full bg-white border-collapse my-4">
        <thead>
          <tr>
            <th className="border px-4 py-2 text-left w-1/2 bg-zinc-200 text-zinc-500">
              Standard/Guideline
            </th>
            <th className="border px-4 py-2 text-left w-1/2 bg-zinc-200 text-zinc-500">
              Included In Report
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td className="border px-4 py-2 w-1/2">
              <a
                href="https://www.w3.org/TR/2008/REC-WCAG20-20081211/"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                Web Content Accessibility Guidelines 2.0
              </a>
            </td>
            <td className="border px-4 py-2 w-1/2">
              Level A (Yes)
              <br />
              Level AA (Yes)
              <br />
              Level AAA (No)
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/2">
              <a
                href="https://www.w3.org/TR/WCAG21/"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                Web Content Accessibility Guidelines 2.1
              </a>
            </td>
            <td className="border px-4 py-2 w-1/2">
              Level A (Yes)
              <br />
              Level AA (Yes)
              <br />
              Level AAA (No)
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/2">
              <a
                href="https://www.w3.org/TR/WCAG22/"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                Web Content Accessibility Guidelines 2.2
              </a>
            </td>
            <td className="border px-4 py-2 w-1/2">
              Level A (Yes)
              <br />
              Level AA (Yes)
              <br />
              Level AAA (No)
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/2">
              <a
                href="https://www.access-board.gov/ict/"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                Revised Section 508 standards published January 18, 2017 and
                corrected January 22, 2018
              </a>
            </td>
            <td className="border px-4 py-2 w-1/2">Yes</td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/2">
              <a
                href="https://www.etsi.org/deliver/etsi_en/301500_301599/301549/03.01.01_60/en_301549v030101p.pdf"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                EN 301 549 Accessibility requirements for ICT products and
                services - V3.1.1 (2019-11) AND EN 301 549 Accessibility
                requirements for ICT products and services - V3.2.1 (2021-03)
              </a>
            </td>
            <td className="border px-4 py-2 w-1/2">No</td>
          </tr>
        </tbody>
      </table>
      <p className="mb-1">
        <strong>Terms</strong>
        <p>
          The terms used in the Conformance Level information are defined as
          follows:
        </p>
        <ul className="list-disc ml-8 my-2">
          <li>
            <strong>Supports</strong>: The functionality of the product has at
            least one method that meets the criterion without known defects or
            meets with equivalent facilitation.
          </li>
          <li>
            <strong>Partially Supports</strong>: Some functionality of the
            product does not meet the criterion.
          </li>
          <li>
            <strong>Does Not Support</strong>: The majority of product
            functionality does not meet the criterion.
          </li>
          <li>
            <strong>Not Applicable</strong>: The criterion is not relevant to
            the product.
          </li>
          <li>
            <strong>Not Evaluated</strong>: The product has not been evaluated
            against the criterion. This can only be used in WCAG Level AAA
            criteria.
          </li>
        </ul>
      </p>

      <h2 className="heading-2xl font-semibold my-4" id="WCAG-2.2">
        WCAG 2.2 Report
      </h2>
      <p className="mb-1">
        Tables 1 and 2 also document conformance with:
        <ul className="list-disc ml-8 my-2">
          <li>
            Revised Section 508: Chapter 5 – 501.1 Scope, 504.2 Content Creation
            or Editing, and Chapter 6 – 602.3 Electronic Support Documentation.
          </li>
        </ul>
      </p>
      <p className="italic">
        Note: When reporting on conformance with the WCAG 2.x Success Criteria,
        they are scoped for full pages, complete processes, and
        accessibility-supported ways of using technology as documented in the{" "}
        <a
          href="https://www.w3.org/TR/WCAG20/#conformance-reqs"
          className="underline"
          target="_blank"
          rel="noopener noreferrer"
        >
          WCAG 2.0 Conformance Requirements
        </a>
        .
      </p>

      <h3 className="heading-xl font-semibold my-2">
        Table 1: Success Criteria, Level A
      </h3>
      <p className="mb-1">
        Notes: This conformance report applies only to the website. The mobile
        site has not been evaluated. We will periodically update this report as
        we release fixes.
      </p>
      <table className="min-w-full bg-white border-collapse my-4">
        <thead>
          <tr>
            <th className="border px-4 py-2 text-left w-1/3 bg-zinc-200 text-zinc-500">
              Criteria
            </th>
            <th className="border px-4 py-2 text-left w-1/3 bg-zinc-200 text-zinc-500">
              Conformance Level
            </th>
            <th className="border px-4 py-2 text-left w-1/3 bg-zinc-200 text-zinc-500">
              Remarks and Explanations
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#text-equiv-all"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>1.1.1 Non-text Content</strong>
              </a>{" "}
              (Level A) <br />
              Also applies to:
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>602.3 (Support Docs)</li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Partially supports</td>
            <td className="border px-4 py-2 w-1/3">
              The close button found on Property Filter pill shapes does not
              have an accessible name.{" "}
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#media-equiv-av-only-alt"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>1.2.1 Audio-only and Video-only (Prerecorded)</strong>
              </a>{" "}
              (Level A) <br />
              Also applies to:
              <br /> Revised Section 508
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>602.3 (Support Docs)</li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Not Applicable</td>
            <td className="border px-4 py-2 w-1/3">
              There are currently no audio or video media in the website{" "}
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#media-equiv-captions"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>1.2.2 Captions (Prerecorded)</strong>
              </a>{" "}
              (Level A) <br />
              Also applies to:
              <br /> Revised Section 508
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>602.3 (Support Docs)</li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Not Applicable</td>
            <td className="border px-4 py-2 w-1/3">
              There are currently no audio or video media in the website{" "}
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#media-equiv-audio-desc"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>
                  1.2.3 Audio Description or Media Alternative (Prerecorded)
                </strong>
              </a>{" "}
              (Level A) <br />
              Also applies to:
              <br /> Revised Section 508
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>602.3 (Support Docs)</li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Not Applicable</td>
            <td className="border px-4 py-2 w-1/3">
              There are currently no audio or video media in the website{" "}
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#content-structure-separation-programmatic"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>1.3.1 Info and Relationships</strong>
              </a>{" "}
              (Level A) <br />
              Also applies to:
              <br /> Revised Section 508
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>602.3 (Support Docs)</li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Partially Supports</td>
            <td className="border px-4 py-2 w-1/3">
              Some elements found in the Find Properties page, such as the
              filters, list box, & toggle buttons have known issues.{" "}
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#content-structure-separation-sequence"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>1.3.2 Meaningful Sequence</strong>
              </a>{" "}
              (Level A) <br />
              Also applies to:
              <br /> Revised Section 508
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>602.3 (Support Docs)</li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Partially Supports</td>
            <td className="border px-4 py-2 w-1/3">
              Some links that take you to a specific position on a webpage are
              not spot on.
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#content-structure-separation-understanding"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>1.3.3 Sensory Characteristics</strong>
              </a>{" "}
              (Level A) <br />
              Also applies to:
              <br /> Revised Section 508
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>
                  <strong>602.3 (Support Docs)</strong>
                </li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Supports</td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#visual-audio-contrast-without-color"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>1.4.1 Use of Color</strong>
              </a>{" "}
              (Level A) <br />
              Also applies to:
              <br /> Revised Section 508
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>
                  <strong>602.3 (Support Docs)</strong>
                </li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Partially Supports</td>
            <td className="border px-4 py-2 w-1/3">
              The interactive map currently depends on color to denote the
              priority of properties. While we actively look for avenues to
              remediate this, the Property list view serves as an alternative.
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#visual-audio-contrast-dis-audio"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>1.4.2 Audio Control</strong>
              </a>{" "}
              (Level A) <br />
              Also applies to:
              <br /> Revised Section 508
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>
                  <strong>602.3 (Support Docs)</strong>
                </li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3">
              There are currently no audio or video media in the website
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#keyboard-operation-keyboard-operable"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>2.1.1 Keyboard</strong>
              </a>{" "}
              (Level A) <br />
              Also applies to:
              <br /> Revised Section 508
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>
                  <strong>602.3 (Support Docs)</strong>
                </li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Partially Supports</td>
            <td className="border px-4 py-2 w-1/3">
              The interactive map’s properties currently can’t be navigated by
              keyboard. While we actively look for avenues to remediate this,
              the Property list view serves as an alternative.
            </td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#keyboard-operation-trapping"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>2.1.2 No Keyboard Trap</strong>
              </a>{" "}
              (Level A) <br />
              Also applies to:
              <br /> Revised Section 508
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>
                  <strong>602.3 (Support Docs)</strong>
                </li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Supports</td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG21/#character-key-shortcuts"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>2.1.4 Character Key Shortcuts</strong>
              </a>{" "}
              (Level A 2.1 and 2.2)
              <br /> Revised Section 508 – Does not apply
            </td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3">
              The website does not require any special key shortcuts
            </td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#time-limits-required-behaviors"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>2.2.1 Timing Adjustable</strong>
              </a>{" "}
              (Level A) <br />
              Also applies to:
              <br /> Revised Section 508
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>
                  <strong>602.3 (Support Docs)</strong>
                </li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#time-limits-pause"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>2.2.2 Pause, Stop, Hide</strong>
              </a>{" "}
              (Level A) <br />
              Also applies to:
              <br /> Revised Section 508
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>602.3 (Support Docs)</li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3">
              There are currently no animation, audio or video media in the
              website
            </td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#seizure-does-not-violate"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>2.3.1 Three Flashes or Below Threshold</strong>
              </a>{" "}
              (Level A) <br />
              Also applies to:
              <br /> Revised Section 508
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>
                  <strong>602.3 (Support Docs)</strong>
                </li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3">
              There are currently no animation, or video media in the website
            </td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#navigation-mechanisms-skip"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>2.4.1 Bypass Blocks</strong>
              </a>{" "}
              (Level A) <br />
              Also applies to:
              <br /> Revised Section 508
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>
                  <strong>
                    602.3 (Support Docs) – Does not apply to non-web docs
                  </strong>
                </li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Supports</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#navigation-mechanisms-title"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>2.4.2 Page Titled</strong>
              </a>{" "}
              (Level A) <br />
              Also applies to:
              <br /> Revised Section 508
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>
                  <strong>602.3 (Support Docs)</strong>
                </li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Supports</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#navigation-mechanisms-focus-order"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>2.4.3 Focus Order</strong>
              </a>{" "}
              (Level A) <br />
              Also applies to:
              <br /> Revised Section 508
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>
                  <strong>602.3 (Support Docs)</strong>
                </li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Partially supports</td>
            <td className="border px-4 py-2 w-1/3">
              Interactive map have known issues; In the Find Properties page,
              keyboard focus can get lost when toggling the Filter button;
            </td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#navigation-mechanisms-refs"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>2.4.4 Link Purpose (In Context)</strong>
              </a>{" "}
              (Level A) <br />
              Also applies to:
              <br /> Revised Section 508
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>
                  <strong>602.3 (Support Docs)</strong>
                </li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Supports</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG21/#pointer-gestures"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>2.5.1 Pointer Gestures</strong>
              </a>{" "}
              (Level A 2.1 and 2.2)
              <br />
              Revised Section 508 – Does not apply
            </td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG21/#pointer-cancellation"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>2.5.2 Pointer Cancellation</strong>
              </a>{" "}
              (Level A 2.1 and 2.2) <br />
              Also applies to:
              <br /> Revised Section 508 – Does not apply
            </td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG21/#label-in-name"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>2.5.3 Label in Name</strong>
              </a>{" "}
              (Level A 2.1 and 2.2) <br />
              Also applies to:
              <br /> Revised Section 508 – Does not apply
            </td>
            <td className="border px-4 py-2 w-1/3">Supports</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG21/#motion-actuation"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>2.5.4 Motion Actuation</strong>
              </a>{" "}
              (Level A)
              <br /> Revised Section 508 – Does not apply
            </td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#meaning-doc-lang-id"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>3.1.1 Language of Page</strong>
              </a>{" "}
              (Level A)
              <br />
              Also applies to:
              <br /> Revised Section 508
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>
                  <strong>602.3 (Support Docs)</strong>
                </li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Supports</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#consistent-behavior-receive-focus"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>3.2.1 On Focus</strong>
              </a>{" "}
              (Level A)
              <br />
              Also applies to:
              <br /> Revised Section 508
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>
                  <strong>602.3 (Support Docs)</strong>
                </li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Supports</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#consistent-behavior-unpredictable-change"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>3.2.2 On Input</strong>
              </a>{" "}
              (Level A)
              <br />
              Also applies to:
              <br /> Revised Section 508
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>
                  <strong>602.3 (Support Docs)</strong>
                </li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Supports</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG22/#consistent-help"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>3.2.6 Consistent Help</strong>
              </a>{" "}
              (Level A 2.2 only)
              <br /> Revised Section 508 – Does not apply
            </td>
            <td className="border px-4 py-2 w-1/3">Supports</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#minimize-error-identified"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>3.3.1 Error Identification</strong>
              </a>{" "}
              (Level A)
              <br />
              Revised Section 508
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>
                  <strong>602.3 (Support Docs)</strong>
                </li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Partially supports</td>
            <td className="border px-4 py-2 w-1/3">
              The interactive map’s search tool can be optimized.
            </td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#minimize-error-cues"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>3.3.2 Labels or Instructions</strong>
              </a>{" "}
              (Level A) <br />
              Also applies to:
              <br />
              Revised Section 508
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>
                  <strong>602.3 (Support Docs)</strong>
                </li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Supports</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG22/#redundant-entry"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>3.3.7 Redundant Entry</strong>
              </a>{" "}
              (Level A 2.2 only)
              <br />
              Revised Section 508 – Does not apply
            </td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#ensure-compat-parses"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>4.1.1 Parsing</strong>
              </a>{" "}
              (Level A)
              <br />
              Applies to:
              <br />
              WCAG 2.0 and 2.1 – Always answer ‘Supports’ WCAG 2.2 (obsolete and
              removed) - Does not apply Revised Section 508
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>
                  <strong>602.3 (Support Docs)</strong>
                </li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Does not apply</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#ensure-compat-rsv"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>4.1.2 Name, Role, Value</strong>
              </a>{" "}
              (Level A)
              <br />
              Also applies to:
              <br />
              Revised Section 508
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>
                  <strong>602.3 (Support Docs)</strong>
                </li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Partially supports</td>
            <td className="border px-4 py-2 w-1/3">
              Some elements found in the Find Properties page, such as the
              filters, list box, toggle buttons & pagination does not announce
              the change of state.
            </td>
          </tr>
        </tbody>
      </table>

      <h3 className="heading-xl font-semibold my-2">
        Table 2: Success Criteria, Level AA
      </h3>
      <p className="mb-1">
        Notes: This conformance report applies only to the website. The mobile
        site has not been evaluated. We will periodically update this report as
        we release fixes.
      </p>
      <table className="min-w-full bg-white border-collapse my-4">
        <thead>
          <tr>
            <th className="border px-4 py-2 text-left w-1/3">Criteria</th>
            <th className="border px-4 py-2 text-left w-1/3">
              Conformance Level
            </th>
            <th className="border px-4 py-2 text-left w-1/3">
              Remarks and Explanations
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#media-equiv-real-time-captions"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>1.2.4 Captions (Live)</strong>
              </a>{" "}
              (Level AA) <br />
              Also applies to:
              <br /> Revised Section 508
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>602.3 (Support Docs)</li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3">
              There are currently no audio or video media in the website{" "}
            </td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG20/#media-equiv-audio-desc-only"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>1.2.5 Audio Description (Prerecorded)</strong>
              </a>{" "}
              (Level AA) <br />
              Also applies to:
              <br /> Revised Section 508
              <ul className="list-disc ml-8">
                <li>501 (Web)(Software)</li>
                <li>504.2 (Authoring Tool)</li>
                <li>602.3 (Support Docs)</li>
              </ul>
            </td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3">
              There are currently no audio or video media in the website{" "}
            </td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG21/#orientation"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>1.3.4 Orientation</strong>
              </a>{" "}
              (Level AA 2.1 and 2.2) <br />
              Also applies to:
              <br /> Revised Section 508 – Does not apply
            </td>
            <td className="border px-4 py-2 w-1/3">Supports</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                href="https://www.w3.org/TR/WCAG21/#identify-input-purpose"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                <strong>1.3.5 Identify Input Purpose</strong>
              </a>{" "}
              (Level AA 2.1 and 2.2) <br />
              Also applies to:
              <br /> Revised Section 508 – Does not apply
            </td>
            <td className="border px-4 py-2 w-1/3">Supports</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>
        </tbody>

        <tr>
          <td className="border px-4 py-2 w-1/3">
            <a
              href="https://www.w3.org/TR/WCAG20/#visual-audio-contrast-contrast"
              className="underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              <strong>1.4.3 Contrast (Minimum)</strong>
            </a>{" "}
            (Level AA) <br />
            Also applies to:
            <br /> Revised Section 508
            <ul className="list-disc ml-8">
              <li>501 (Web)(Software)</li>
              <li>504.2 (Authoring Tool)</li>
              <li>
                <strong>602.3 (Support Docs)</strong>
              </li>
            </ul>
          </td>
          <td className="border px-4 py-2 w-1/3">Partially Supports</td>
          <td className="border px-4 py-2 w-1/3">
            The interactive map have colors that don’t pass the minimum
            requirement. While we actively look for avenues to remediate this,
            the Property list view serves as an alternative.
          </td>
        </tr>

        <tr>
          <td className="border px-4 py-2 w-1/3">
            <a
              href="https://www.w3.org/TR/WCAG20/#visual-audio-contrast-scale"
              className="underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              <strong>1.4.4 Resize text</strong>
            </a>{" "}
            (Level AA) <br />
            Also applies to:
            <br /> Revised Section 508
            <ul className="list-disc ml-8">
              <li>501 (Web)(Software)</li>
              <li>504.2 (Authoring Tool)</li>
              <li>
                <strong>602.3 (Support Docs)</strong>
              </li>
            </ul>
          </td>
          <td className="border px-4 py-2 w-1/3">Supports</td>
          <td className="border px-4 py-2 w-1/3"></td>
        </tr>

        <tr>
          <td className="border px-4 py-2 w-1/3">
            <a
              href="https://www.w3.org/TR/WCAG20/#visual-audio-contrast-text-presentation"
              className="underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              <strong>1.4.5 Images of Text</strong>
            </a>{" "}
            (Level AA) <br />
            Also applies to:
            <br /> Revised Section 508
            <ul className="list-disc ml-8">
              <li>501 (Web)(Software)</li>
              <li>504.2 (Authoring Tool)</li>
              <li>
                <strong>602.3 (Support Docs)</strong>
              </li>
            </ul>
          </td>
          <td className="border px-4 py-2 w-1/3">Partially Supports</td>
          <td className="border px-4 py-2 w-1/3">
            An image found in Transform page have an image of text.
          </td>
        </tr>

        <tr>
          <td className="border px-4 py-2 w-1/3">
            <a
              href="https://www.w3.org/TR/WCAG21/#reflow"
              className="underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              <strong>1.4.10 Reflow</strong>
            </a>{" "}
            (Level AA 2.1 and 2.2) <br />
            Also applies to:
            <br /> Revised Section 508 – Does not apply
          </td>
          <td className="border px-4 py-2 w-1/3">Supports</td>
          <td className="border px-4 py-2 w-1/3"></td>
        </tr>

        <tr>
          <td className="border px-4 py-2 w-1/3">
            <a
              href="https://www.w3.org/TR/WCAG21/#non-text-contrast"
              className="underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              <strong>1.4.11 Non-text Contrast</strong>
            </a>{" "}
            (Level AA 2.1 and 2.2)
            <br /> Revised Section 508 – Does not apply
          </td>
          <td className="border px-4 py-2 w-1/3">Partially Supports</td>
          <td className="border px-4 py-2 w-1/3">
            The interactive map currently uses colors to denote the priority of
            properties that are currently not optimal. While we actively look
            for avenues to remediate this, the Property list view serves as an
            alternative.
          </td>
        </tr>

        <tr>
          <td className="border px-4 py-2 w-1/3">
            <a
              href="https://www.w3.org/TR/WCAG21/#text-spacing"
              className="underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              <strong>1.4.12 Text Spacing</strong>
            </a>{" "}
            (Level AA 2.1 and 2.2)
            <br />
            Also applies to:
            <br /> Revised Section 508 – Does not apply
          </td>
          <td className="border px-4 py-2 w-1/3">Supports</td>
          <td className="border px-4 py-2 w-1/3"></td>
        </tr>

        <tr>
          <td className="border px-4 py-2 w-1/3">
            <a
              href="https://www.w3.org/TR/WCAG21/#content-on-hover-or-focus"
              className="underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              <strong>1.4.13 Content on Hover or Focus</strong>
            </a>{" "}
            (Level AA 2.1 and 2.2)
            <br /> Revised Section 508 – Does not apply
          </td>
          <td className="border px-4 py-2 w-1/3">Supports</td>
          <td className="border px-4 py-2 w-1/3"></td>
        </tr>

        <tr>
          <td className="border px-4 py-2 w-1/3">
            <a
              href="https://www.w3.org/TR/WCAG20/#navigation-mechanisms-mult-loc"
              className="underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              <strong>2.4.5 Multiple Ways</strong>
            </a>{" "}
            (Level AA)
            <br /> Revised Section 508
            <ul className="list-disc ml-8">
              <li>501 (Web)(Software) – Does not apply to non-web software</li>
              <li>504.2 (Authoring Tool)</li>
              <li>
                <strong>
                  602.3 (Support Docs) – Does not apply to non-web docs
                </strong>
              </li>
            </ul>
          </td>
          <td className="border px-4 py-2 w-1/3"></td>
          <td className="border px-4 py-2 w-1/3"></td>
        </tr>

        <tr>
          <td className="border px-4 py-2 w-1/3">
            <a
              href="https://www.w3.org/TR/WCAG20/#navigation-mechanisms-mult-loc"
              className="underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              <strong>2.4.5 Multiple Ways</strong>
            </a>{" "}
            (Level AA)
            <br /> Revised Section 508
            <ul className="list-disc ml-8">
              <li>501 (Web)(Software) – Does not apply to non-web software</li>
              <li>504.2 (Authoring Tool)</li>
              <li>
                <strong>
                  602.3 (Support Docs) – Does not apply to non-web docs
                </strong>
              </li>
            </ul>
          </td>
          <td className="border px-4 py-2 w-1/3"></td>
          <td className="border px-4 py-2 w-1/3"></td>
        </tr>

        <tr>
          <td className="border px-4 py-2 w-1/3">
            <a
              href="https://www.w3.org/TR/WCAG20/#navigation-mechanisms-descriptive"
              className="underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              <strong>2.4.6 Headings and Labels</strong>
            </a>{" "}
            (Level AA) <br />
            Also applies to:
            <br /> Revised Section 508
            <ul className="list-disc ml-8">
              <li>501 (Web)(Software)</li>
              <li>504.2 (Authoring Tool)</li>
              <li>
                <strong>602.3 (Support Docs)</strong>
              </li>
            </ul>
          </td>
          <td className="border px-4 py-2 w-1/3">Supports</td>
          <td className="border px-4 py-2 w-1/3"></td>
        </tr>

        <tr>
          <td className="border px-4 py-2 w-1/3">
            <a
              href="https://www.w3.org/TR/WCAG20/#navigation-mechanisms-focus-visible"
              className="underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              <strong>2.4.7 Focus Visible</strong>
            </a>{" "}
            (Level AA) <br />
            Also applies to:
            <br /> Revised Section 508
            <ul className="list-disc ml-8">
              <li>501 (Web)(Software)</li>
              <li>504.2 (Authoring Tool)</li>
              <li>
                <strong>602.3 (Support Docs)</strong>
              </li>
            </ul>
          </td>
          <td className="border px-4 py-2 w-1/3">Supports</td>
          <td className="border px-4 py-2 w-1/3"></td>
        </tr>

        <tr>
          <td className="border px-4 py-2 w-1/3">
            <a
              href="https://www.w3.org/TR/WCAG22/#focus-not-obscured-minimum"
              className="underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              <strong>2.4.11 Focus Not Obscured (Minimum)</strong>
            </a>{" "}
            (Level AA 2.2 only)
            <br /> Revised Section 508 – Does not apply
          </td>
          <td className="border px-4 py-2 w-1/3">Supports</td>
          <td className="border px-4 py-2 w-1/3"></td>
        </tr>

        <tr>
          <td className="border px-4 py-2 w-1/3">
            <a
              href="https://www.w3.org/TR/WCAG22/#dragging-movements"
              className="underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              <strong>2.5.7 Dragging Movements</strong>
            </a>{" "}
            (Level AA 2.2 only)
            <br /> Revised Section 508 – Does not apply
          </td>
          <td className="border px-4 py-2 w-1/3">Not applicable</td>
          <td className="border px-4 py-2 w-1/3">
            There are currently no draggable interactions found in the website.
          </td>
        </tr>

        <tr>
          <td className="border px-4 py-2 w-1/3">
            <a
              href="https://www.w3.org/TR/WCAG22/#target-size-minimum"
              className="underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              <strong>2.5.8 Target Size (Minimum)</strong>
            </a>{" "}
            (Level AA 2.2 only)
            <br /> Revised Section 508 – Does not apply
          </td>
          <td className="border px-4 py-2 w-1/3">Supports</td>
          <td className="border px-4 py-2 w-1/3"></td>
        </tr>

        <tr>
          <td className="border px-4 py-2 w-1/3">
            <a
              href="https://www.w3.org/TR/WCAG20/#meaning-other-lang-id"
              className="underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              <strong>3.1.2 Language of Parts</strong>
            </a>{" "}
            (Level AA) <br />
            Also applies to:
            <br /> Revised Section 508
            <ul className="list-disc ml-8">
              <li>501 (Web)(Software)</li>
              <li>504.2 (Authoring Tool)</li>
              <li>
                <strong>602.3 (Support Docs)</strong>
              </li>
            </ul>
          </td>
          <td className="border px-4 py-2 w-1/3">Not applicable</td>
          <td className="border px-4 py-2 w-1/3"></td>
        </tr>

        <tr>
          <td className="border px-4 py-2 w-1/3">
            <a
              href="https://www.w3.org/TR/WCAG20/#consistent-behavior-consistent-locations"
              className="underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              <strong>3.2.3 Consistent Navigation</strong>
            </a>{" "}
            (Level AA) <br />
            Also applies to:
            <br /> Revised Section 508
            <ul className="list-disc ml-8">
              <li>501 (Web)(Software) – Does not apply to non-web software</li>
              <li>504.2 (Authoring Tool)</li>
              <li>
                <strong>
                  602.3 (Support Docs) – Does not apply to non-web docs
                </strong>
              </li>
            </ul>
          </td>
          <td className="border px-4 py-2 w-1/3">Supports</td>
          <td className="border px-4 py-2 w-1/3"></td>
        </tr>

        <tr>
          <td className="border px-4 py-2 w-1/3">
            <a
              href="https://www.w3.org/TR/WCAG20/#consistent-behavior-consistent-functionality"
              className="underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              <strong>3.2.4 Consistent Identification</strong>
            </a>{" "}
            (Level AA) <br />
            Also applies to:
            <br /> Revised Section 508
            <ul className="list-disc ml-8">
              <li>501 (Web)(Software) – Does not apply to non-web software</li>
              <li>504.2 (Authoring Tool)</li>
              <li>
                <strong>
                  602.3 (Support Docs) – Does not apply to non-web docs
                </strong>
              </li>
            </ul>
          </td>
          <td className="border px-4 py-2 w-1/3">Supports</td>
          <td className="border px-4 py-2 w-1/3"></td>
        </tr>

        <tr>
          <td className="border px-4 py-2 w-1/3">
            <a
              href="https://www.w3.org/TR/WCAG20/#minimize-error-suggestions"
              className="underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              <strong>3.3.3 Error Suggestion</strong>
            </a>{" "}
            (Level AA)
            <br /> Revised Section 508
            <ul className="list-disc ml-8">
              <li>501 (Web)(Software)</li>
              <li>504.2 (Authoring Tool)</li>
              <li>
                <strong>602.3 (Support Docs)</strong>
              </li>
            </ul>
          </td>
          <td className="border px-4 py-2 w-1/3"></td>
          <td className="border px-4 py-2 w-1/3"></td>
        </tr>

        <tr>
          <td className="border px-4 py-2 w-1/3">
            <a
              href="https://www.w3.org/TR/WCAG20/#minimize-error-reversible"
              className="underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              <strong>3.3.4 Error Prevention (Legal, Financial, Data)</strong>
            </a>{" "}
            (Level AA)
            <br /> Revised Section 508
            <ul className="list-disc ml-8">
              <li>501 (Web)(Software)</li>
              <li>504.2 (Authoring Tool)</li>
              <li>
                <strong>602.3 (Support Docs)</strong>
              </li>
            </ul>
          </td>
          <td className="border px-4 py-2 w-1/3">Not applicable</td>
          <td className="border px-4 py-2 w-1/3"></td>
        </tr>

        <tr>
          <td className="border px-4 py-2 w-1/3">
            <a
              href="https://www.w3.org/TR/WCAG22/#accessible-authentication-minimum"
              className="underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              <strong>3.3.8 Accessible Authentication (Minimum)</strong>
            </a>{" "}
            (Level AA 2.2 only)
            <br /> Revised Section 508 – Does not apply
          </td>
          <td className="border px-4 py-2 w-1/3">Not applicable</td>
          <td className="border px-4 py-2 w-1/3"></td>
        </tr>

        <tr>
          <td className="border px-4 py-2 w-1/3">
            <a
              href="https://www.w3.org/TR/WCAG21/#status-messages"
              className="underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              <strong>4.1.3 Status Messages</strong>
            </a>{" "}
            (Level AA 2.1 and 2.2)
            <br /> Revised Section 508 – Does not apply
          </td>
          <td className="border px-4 py-2 w-1/3">Partially supports</td>
          <td className="border px-4 py-2 w-1/3">
            We currently don’t announce the change of state on some behaviors
            found on the Find Properties page, such as the pagination and when
            properties yield no results.
          </td>
        </tr>
      </table>

      <h2 className="heading-2xl font-semibold my-4 bg-zinc-200">
        Revised Section 508 Report
      </h2>
      <p className="mb-1">
        Notes: This conformance report applies only to the website. The mobile
        site has not been evaluated. We will periodically update this report as
        we release fixes.
      </p>

      <h3 className="heading-xl font-semibold my-2">
        Chapter 3:{" "}
        <a
          href="https://www.access-board.gov/ict/#chapter-3-functional-performance-criteria"
          className="underline"
          target="_blank"
          rel="noopener noreferrer"
        >
          {" "}
          Functional Performance Criteria
        </a>{" "}
        (FPC)
      </h3>
      <p className="mb-1">
        Notes: The interactive map needs better accessibility support and
        optimization. We are actively looking to improve this.
      </p>
      <table className="min-w-full bg-white border-collapse my-4">
        <thead>
          <tr>
            <th className="border px-4 py-2 text-left w-1/3">Criteria</th>
            <th className="border px-4 py-2 text-left w-1/3">
              Conformance Level
            </th>
            <th className="border px-4 py-2 text-left w-1/3">
              Remarks and Explanations
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td className="border px-4 py-2 w-1/3">302.1 Without Vision</td>
            <td className="border px-4 py-2 w-1/3">Partially supports</td>
            <td className="border px-4 py-2 w-1/3">
              The interactive map current doesn’t support keyboard navigation to
              the properties. While we actively look for avenues to remediate
              this, the Property list view serves as an alternative.
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              302.2 With Limited Vision
            </td>
            <td className="border px-4 py-2 w-1/3">Supports</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              302.3 Without Perception of Color
            </td>
            <td className="border px-4 py-2 w-1/3">Partially supports</td>
            <td className="border px-4 py-2 w-1/3">
              The interactive map currently depends on color to denote the
              priority of properties. While we actively look for avenues to
              remediate this, the Property list view serves as an alternative.
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">302.4 Without Hearing</td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3">
              There are currently no audio or video media in the website
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              302.5 With Limited Hearing
            </td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3">
              There are currently no audio or video media in the website
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">302.6 Without Speech</td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3">
              No speech input required in the website
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              302.7 With Limited Manipulation
            </td>
            <td className="border px-4 py-2 w-1/3">Partially supports</td>
            <td className="border px-4 py-2 w-1/3">
              The interactive map current doesn’t support keyboard navigation to
              the properties. While we actively look for avenues to remediate
              this, the Property list view serves as an alternative.
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              302.8 With Limited Reach and Strength
            </td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              302.9 With Limited Language, Cognitive, and Learning Abilities
            </td>
            <td className="border px-4 py-2 w-1/3">Supports</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>
        </tbody>
      </table>

      <h3 className="heading-xl font-semibold my-2">
        Section 508 Chapter 4:{" "}
        <a
          href="https://www.access-board.gov/ict/#chapter-4-hardware"
          className="underline"
          target="_blank"
          rel="noopener noreferrer"
        >
          Hardware
        </a>
      </h3>
      <p className="mb-1">
        Notes: Not applicable to Clean & Green Philly website.
      </p>

      <h3 className="heading-xl font-semibold my-2">
        {" "}
        Chapter 5:{" "}
        <a
          href="https://www.access-board.gov/ict/#chapter-5-software"
          className="underline"
          target="_blank"
          rel="noopener noreferrer"
        >
          Software
        </a>
      </h3>
      <p className="mb-1">Notes:</p>
      <table className="min-w-full bg-white border-collapse my-4">
        <thead>
          <tr>
            <th className="border px-4 py-2 text-left w-1/3">Criteria</th>
            <th className="border px-4 py-2 text-left w-1/3">
              Conformance Level
            </th>
            <th className="border px-4 py-2 text-left w-1/3">
              Remarks and Explanations
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              501.1 Scope – Incorporation of WCAG 2.2 AA
            </td>
            <td className="border px-4 py-2 w-1/3">
              See{" "}
              <a
                href="#WCAG-2.2"
                className="underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                WCAG 2.2 section
              </a>
            </td>
            <td className="border px-4 py-2 w-1/3">
              See information in WCAG 2.2 section
            </td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3">
              <a
                className="underline italic font-bold"
                href="https://www.access-board.gov/ict/#502-interoperability-assistive-technology"
                target="_blank"
                rel="noopener noreferrer"
              >
                {" "}
                502 Interoperability with Assistive Technology
              </a>
            </td>
            <td className="border px-4 py-2 w-1/3"></td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              502.2.1 User Control of Accessibility Features
            </td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3">
              We do not have specific accessibility features in the website. We
              support the accessibility features of user agents (ex. supported
              browsers & screen readers)
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              502.2.2 No Disruption of Accessibility Features
            </td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3">
              We do not have specific accessibility features in the website. We
              support the accessibility features of user agents (ex. supported
              browsers & screen readers)
            </td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3 italic font-bold bg-zinc-200">
              502.3 Accessibility Services
            </td>
            <td className="border px-4 py-2 w-1/3 bg-zinc-200"></td>
            <td className="border px-4 py-2 w-1/3 bg-zinc-200"></td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              502.3.1 Object Information
            </td>
            <td className="border px-4 py-2 w-1/3">Partially supports</td>
            <td className="border px-4 py-2 w-1/3">
              Some elements found in the Find Properties page, such as the
              filters, list box, toggle buttons & pagination does not announce
              the change of state.
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              502.3.2 Modification of Object Information
            </td>
            <td className="border px-4 py-2 w-1/3">Partially supports</td>
            <td className="border px-4 py-2 w-1/3">
              Some elements found in the Find Properties page, such as the
              filters, list box, toggle buttons, pagination & zero search
              results have known issues.
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              502.3.3 Row, Column, and Headers
            </td>
            <td className="border px-4 py-2 w-1/3">Supports</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">502.3.4 Values</td>
            <td className="border px-4 py-2 w-1/3">Supports</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              502.3.5 Modification of Values
            </td>
            <td className="border px-4 py-2 w-1/3">Supports</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              502.3.6 Label Relationships
            </td>
            <td className="border px-4 py-2 w-1/3">Supports</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              502.3.7 Hierarchical Relationships
            </td>
            <td className="border px-4 py-2 w-1/3">Supports</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">502.3.8 Text</td>
            <td className="border px-4 py-2 w-1/3">Supports</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              502.3.9 Modification of Text
            </td>
            <td className="border px-4 py-2 w-1/3">Supports</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">502.3.10 List of Actions</td>
            <td className="border px-4 py-2 w-1/3">Supports</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              502.3.11 Actions on Objects
            </td>
            <td className="border px-4 py-2 w-1/3">Supports</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">502.3.12 Focus Cursor</td>
            <td className="border px-4 py-2 w-1/3">Supports</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              502.3.13 Modification of Focus Cursor
            </td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3">
              We don’t have custom focus indicator; we make use of the user
              agent’s focus indicator.
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              502.3.14 Event Notification
            </td>
            <td className="border px-4 py-2 w-1/3">Partially supports</td>
            <td className="border px-4 py-2 w-1/3">
              We currently don’t announce the change of state on some behaviors
              found on the Find Properties page, such as the pagination and when
              properties yield no results.
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              502.4 Platform Accessibility Features
            </td>
            <td className="border px-4 py-2 w-1/3"></td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3 bg-zinc-200">
              <a
                className="underline italic font-bold"
                href="https://www.access-board.gov/ict/#503-applications"
                target="_blank"
                rel="noopener noreferrer"
              >
                503 Applications
              </a>
            </td>
            <td className="border px-4 py-2 w-1/3 bg-zinc-200"></td>
            <td className="border px-4 py-2 w-1/3 bg-zinc-200"></td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">503.2 User Preferences</td>
            <td className="border px-4 py-2 w-1/3">Supports</td>
            <td className="border px-4 py-2 w-1/3"></td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              503.3 Alternative User Interfaces
            </td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3">
              We do not have alternative user interface.
            </td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3 bg-zinc-200 italic font-bold">
              503.4 User Controls for Captions and Audio Description
            </td>
            <td className="border px-4 py-2 w-1/3 bg-zinc-200"></td>
            <td className="border px-4 py-2 w-1/3 bg-zinc-200"></td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">503.4.1 Caption Controls</td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3">
              There are currently no audio or video media in the website
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              503.4.2 Audio Description Controls
            </td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3">
              There are currently no audio or video media in the website
            </td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3 bg-zinc-200">
              <a
                className="underline italic font-bold"
                href="https://www.access-board.gov/ict/#504-authoring-tools"
                target="_blank"
                rel="noopener noreferrer"
              >
                504 Authoring Tools
              </a>
            </td>
            <td className="border px-4 py-2 w-1/3 bg-zinc-200"></td>
            <td className="border px-4 py-2 w-1/3 bg-zinc-200"></td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              504.2 Content Creation or Editing
            </td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3">
              The website is not a content creation or an editing tool
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              504.2.1 Preservation of Information Provided for Accessibility in
              Format Conversion
            </td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3">
              The website is not a content creation or an editing tool
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">504.2.2 PDF Export</td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3">
              The website doesn’t offer PDF exports
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">504.3 Prompts</td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3">
              The website is not a content creation or an editing tool
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">504.4 Templates</td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3">
              The website is not a content creation or an editing tool
            </td>
          </tr>
        </tbody>
      </table>

      <h3 className="heading-xl font-semibold my-2">
        Chapter 6:{" "}
        <a
          className="underline"
          href="https://www.access-board.gov/ict/#chapter-6-support-documentation-and-services"
          target="_blank"
          rel="noopener noreferrer"
        >
          Support Documentation and Services
        </a>
      </h3>
      <p className="mb-1">Notes:</p>
      <table className="min-w-full bg-white border-collapse my-4">
        <thead>
          <tr>
            <th className="border px-4 py-2 text-left w-1/3">Criteria</th>
            <th className="border px-4 py-2 text-left w-1/3">
              Conformance Level
            </th>
            <th className="border px-4 py-2 text-left w-1/3">
              Remarks and Explanations
            </th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td className="border px-4 py-2 w-1/3 bg-zinc-200 italic font-bold">
              601.1 Scope
            </td>
            <td className="border px-4 py-2 w-1/3 bg-zinc-200"></td>
            <td className="border px-4 py-2 w-1/3 bg-zinc-200"></td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3 bg-zinc-200">
              <a
                className="underline italic font-bold"
                href="https://www.access-board.gov/ict/#602-support-documentation"
                target="_blank"
                rel="noopener noreferrer"
              >
                602 Support Documentation
              </a>
            </td>
            <td className="border px-4 py-2 w-1/3 bg-zinc-200"></td>
            <td className="border px-4 py-2 w-1/3 bg-zinc-200"></td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              602.2 Accessibility and Compatibility Features
            </td>
            <td className="border px-4 py-2 w-1/3">Does not support</td>
            <td className="border px-4 py-2 w-1/3">
              We do not have documentation that outlines the built-in
              accessibility and compatibility with assistive technology.
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              602.3 Electronic Support Documentation
            </td>
            <td className="border px-4 py-2 w-1/3">
              See{" "}
              <a className="underline" href="#WCAG-2.2">
                WCAG 2.2 section
              </a>
            </td>
            <td className="border px-4 py-2 w-1/3">
              See information in WCAG 2.2 section
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              602.4 Alternate Formats for Non- Electronic Support Documentation
            </td>
            <td className="border px-4 py-2 w-1/3">Not applicable</td>
            <td className="border px-4 py-2 w-1/3">
              The website doesn’t have nonelectronic support documentation
            </td>
          </tr>

          <tr>
            <td className="border px-4 py-2 w-1/3 bg-zinc-200">
              <a
                className="underline italic font-bold"
                href="https://www.access-board.gov/ict/#603-support-services"
                target="_blank"
                rel="noopener noreferrer"
              >
                603 Support Services
              </a>
            </td>
            <td className="border px-4 py-2 w-1/3 bg-zinc-200"></td>
            <td className="border px-4 py-2 w-1/3 bg-zinc-200"></td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              603.2 Information on Accessibility and Compatibility Features
            </td>
            <td className="border px-4 py-2 w-1/3">Does not support</td>
            <td className="border px-4 py-2 w-1/3">
              We currently don’t have accessibility information in the website
            </td>
          </tr>
          <tr>
            <td className="border px-4 py-2 w-1/3">
              603.3 Accommodation of Communication Needs
            </td>
            <td className="border px-4 py-2 w-1/3">Does not support</td>
            <td className="border px-4 py-2 w-1/3">
              We currently don’t have support contact for accessibility feedback
            </td>
          </tr>
        </tbody>
      </table>
      <br></br>
    </>
  );
}
