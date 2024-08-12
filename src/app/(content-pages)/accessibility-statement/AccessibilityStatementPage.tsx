import Link from 'next/link';

export default function AccessibilityStatementPage() {
  return (
    <>
      <h1 className="heading-3xl font-bold mb-6">
        Accessibility at Clean & Green Philly
      </h1>
      <p>
        Clean & Green Philly makes accessibility a priority. Our dedicated team
        of volunteers is committed to creating accessible & inclusive
        experiences for all. We believe that everyone should have the
        opportunity to participate and use our website, regardless of their
        physical or cognitive abilities.
      </p>
      <h2 className="heading-2xl font-semibold mt-8">
        Measures to Support Accessibility
      </h2>
      <p>Our team prioritizes accessibility by:</p>
      <ul className="list-disc ml-8 my-2">
        <li>Integrating accessibility as part of the design process</li>
        <li>Integrating accessibility in the development process</li>
        <li>Utilizing automated accessibility tools as part of our testing</li>
        <li>
          Designating an Accessibility Specialist that serves as a resource for
          our contributors
        </li>
      </ul>
      <h2 className="heading-2xl font-semibold mt-8">Conformance Status</h2>
      <p>
        The Clean & Green Philly website has been evaluated using the Web
        Content Accessibility Guidelines (WCAG) 2.2 for Level AA conformance.
        While we strive for full accessibility, the site is currently partially
        conformant with WCAG 2.2 Level AA, meaning some aspects of the content
        do not yet fully meet these standards.
      </p>
      <h2 className="heading-2xl font-semibold mt-8"> Feedback & Contact</h2>
      <p>
        We welcome your feedback on any accessibility issues you may encounter,
        or any questions. you may have about the accessibility of this website.
        We appreciate your input on improving our services. We can be reached
        at:
      </p>
      <ul className="list-disc ml-8 my-2">
        <li>cleanandgreenphl@gmail.com</li>
        <li>
          Submit an issue through our{' '}
          <a
            href="https://github.com/CodeForPhilly/clean-and-green-philly/issues"
            className="link"
            target="_blank"
            rel="noopener noreferrer"
          >
            Github
          </a>
        </li>
      </ul>
      <h2 className="heading-2xl font-semibold mt-8">Compatibility</h2>
      <p>
        Clean and Green Philly is compatible and tested with the latest version
        of modern browsers and the following assistive technologies:
      </p>
      <ul className="list-disc ml-8 my-2">
        <li>Safari with VoiceOver on Mac OS </li>
        <li>
          Mozilla Firefox, Google Chrome, Microsoft Edge with NVDA on Windows
        </li>
        <li> Google Chrome, Microsoft Edge with JAWS 2024 on Windows</li>
      </ul>
      <p>
        At the time of this writing, Clean and Green Philly website has not been
        tested on mobile devices.
      </p>
      <h2 className="heading-2xl font-semibold mt-8">
        Limitations & Alternatives
      </h2>
      <p>
        While Clean and Green Philly constantly aims to ensure accessibility of
        our web pages, there are currently some limitations:
      </p>
      <ol className="list-decimal ml-8 my-2">
        <li>
          <span className="font-bold">Find Property Filters</span>: While it is
          usable, the overall screen reader experience of selecting, deselecting
          and clearing of filter options isn’t optimized. We currently have open
          issues to resolve this.
        </li>
        <li>
          <span className="font-bold">Announcing change of state</span>: Find
          Property filters and pagination may not always announce the change,
          such as if a new content has loaded, or when an option has been
          removed.
        </li>
        <li>
          <span className="font-bold">Interactive Map</span>: Despite our best
          efforts, some elements in our interactive maps, particularly the
          properties, may not be fully accessible. Although we selected the most
          accessible map library available, some criteria couldn’t be met
          without compromising the essential purpose and meaning of what we
          represent in the map. We are actively researching ways to enhance its
          accessibility. In the meantime, we recommend using the property list
          as an alternative.
        </li>
      </ol>
      <p>
        This project is an open-source initiative run by dedicated volunteers.
        While we strive to address issues as quickly and thoroughly as possible,
        our capacity is limited. We are committed to doing our best and greatly
        appreciate your patience and understanding as we work within these
        constraints.
      </p>
      <h2 className="heading-2xl font-semibold mt-8">Evaluation Report</h2>
      <p>
        You can find our full evaluation report in VPAT®️ format. (
        <Link href="/vpat" className="link">
          link
        </Link>
        )
      </p>
      <hr className="my-6 border-gray-300" />

      <p>This statement was created on June 10, 2024.</p>
    </>
  );
}
