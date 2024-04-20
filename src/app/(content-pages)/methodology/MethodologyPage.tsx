export default function MethodologyPage() {
  return (
    <>
      <h1 className="heading-3xl font-bold my-5 md:mb-6">Our Methodology</h1>
      <div className="container mx-auto my-2">
        <h2 className="heading-2xl font-semibold mb-4">Overview</h2>

        <p className="body-md mb-4">
          Clean & Green Philly combines several public datasets in order to
          categorize Philadelphia’s vacant properties based on how important it
          is that someone intervene there and what the easiest way to do that
          is. To do this, we created a dataset based on{" "}
          <a
            href="https://www.pnas.org/doi/10.1073/pnas.1718503115"
            target="_blank"
            rel="noopener noreferrer"
            className="link"
            aria-label="Original research conducted by Dr. Eugenia South and her
                colleagues, link opens in a new window"
          >
            the original research conducted by Dr. Eugenia South and her
            colleagues
          </a>
          , as well as many conversations with stakeholders, including community
          residents, CDCs, City government offices, academic researchers, and
          more.
        </p>
        {/* Offset for clicking on learn more from filter, scrolls to section below */}
        <span id="priority-method"></span>
        <p className="body-md">
          Although we aim to simplify the decision-making process for users of
          Clean & Green Philly, we value transparency. Below, we lay out key
          aspects of our methodology. For further questions, feel free to reach
          out to us at{" "}
          <a href="mailto:cleanandgreenphl@gmail.com" className="link">
            {" "}
            cleanandgreenphl@gmail.com
          </a>
          .
        </p>

        <div className="container mx-auto md:my-12">
          <h2 className="heading-2xl font-semibold mb-4">
            How did we determine “priority"?
          </h2>

          <p className="body-md mb-4">
            Getting legal access to intervene in a property is a significant
            obstacle to cleaning and greening vacant properties. We hope to
            reduce this barrier by helping users identify the most properties
            with the simplest or most attainable routes of getting access. We
            identify these routes by considering various factors.
          </p>

          <ol className="methodology">
            <li className="methodology">
              <p>
                <span className="font-bold"> Gun violence. </span>
                We use the Philadelphia Police Department data on gun violence
                data.
              </p>
            </li>
            <li className="methodology">
              <p>
                <span className="font-bold"> Cleanliness. </span>
                We use L&I data on various kinds of unclean or hazardous
                conditions (e.g., illegal dumping or abandoned cars).
              </p>
            </li>
            <li>
              <p>
                <span className="font-bold"> Tree canopy. </span>
                We use the{" "}
                <a
                  href="https://www.treeequityscore.org/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="link"
                  aria-label="Tree Canopy, link opens in a new window"
                >
                  Tree Equity Score
                </a>{" "}
                data on tree canopy coverage.
              </p>
            </li>
            <li>
              <p>
                <span className="font-bold"> In Care. </span>
                We use the{" "}
                <a
                  href="https://phsonline.org/programs/transforming-vacant-land"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="link"
                  aria-label="Pennsylvania Horticultural Society's LandCare Program, link opens in a new window"
                >
                  Pennsylvania Horticultural Society's LandCare Program
                </a>{" "}
                data to determine if the property is either in Community
                LandCare or Philadelphia LandCare initiatives, which are
                Philadelphia’s original cleaning and greening initiatives and
                the basis for Dr. South’s research.
              </p>
            </li>
          </ol>
          <br />
          {/* Offset for clicking on learn more from filter, scrolls to section below */}
          <span id="access-method"></span>
          <p className="body-md mb-4">
            These specific datasets were chosen based on the original research
            and extensive stakeholder engagement. The decision tree below
            indicates the specific breakpoints we use in our classification.
          </p>
        </div>

        <div className="container mx-auto md:my-12">
          <h2 className="heading-2xl font-semibold mb-4">
            How did we determine "access process"?
          </h2>

          <p className="body-md mb-4">
            Getting legal access to intervene in a property is a significant
            obstacle to cleaning and greening vacant properties. We hope to
            reduce this barrier by helping users identify the most properties
            with the simplest or most attainable routes of getting access. We
            identify these routes by considering various factors.
          </p>

          <ol className="methodology">
            <li>
              <p>
                <span className="font-bold"> Owner. </span>
                Is it a private individual or the Philadelphia Land Bank?
              </p>
            </li>
            <li>
              <p>
                <span className="font-bold"> Price. </span>
                Is it expensive or affordable?
              </p>
            </li>
            <li>
              <p>
                <span className="font-bold"> Conservatorship. </span>
                Would qualify for Act 135 conservatorship?
              </p>
            </li>
          </ol>
          <br />
          <p className="body-md mb-4">
            We based our criteria on local law and land disposition policies, as
            well as the availability and applicability of data. Some of our
            guiding references include{" "}
            <a
              href="https://groundedinphilly.org/"
              target="_blank"
              rel="noopener noreferrer"
              className="link"
              aria-label="Grounded in Philly, link opens in a new window"
            >
              Grounded in Philly’s
            </a>{" "}
            work and{" "}
            <a
              href="https://k05f3c.p3cdn1.secureserver.net/wp-content/uploads/Resources/Philadelphia-Land-Bank-Disposition-Policies-2020.pdf"
              target="_blank"
              rel="noopener noreferrer"
              className="link"
              aria-label="the Philadelphia Land Bank, opens in a new window"
            >
              the Philadelphia Land Bank’s
            </a>{" "}
            disposition policies.
          </p>

          <p className="body-md mb-4">
            Additionally, we note that our access process labels are only
            suggestions. Anyone using Clean & Green Philly should verify the
            information we have provided before acting on it. When applicable,
            we encourage users to seek legal advice to ensure that they are in
            compliance with relevant laws. Please see{" "}
            <a
              href="https://www.cleanandgreenphilly.org/legal-disclaimer"
              rel="noopener noreferrer"
              className="link"
            >
              our legal disclaimer
            </a>{" "}
            for more detail.
          </p>
        </div>

        <div className="container mx-auto md:my-12">
          <h2 className="heading-2xl font-semibold mb-4">
            Gun Crime Calculations
          </h2>
          <p className="body-md mb-4">
            It is impossible to reduce the impact of a shooting to a single
            statistic, and Clean & Green Philly applauds the organizations
            throughout our city who work to give voice to the profound effect of
            this epidemic on individuals, families, and communities. With this
            in mind, we have done our best to estimate the spatial intensity of
            gun violence in Philadelphia in a way that is 1) statistically
            rigorous and 2) as sensitive to local experience as possible.
            Following Dr. South’s original research, we use a kernel density
            estimate to calculate the intensity of gun crime at any given point
            in Philadelphia. Specifically, we use an adaptive bandwidth to
            better capture the local nuances of gun crime at small spatial
            scales. (For more on this, please see this memo from the data
            analysis team at the{" "}
            <a
              href="##"
              target="_blank"
              rel="noopener noreferrer"
              className="link"
              aria-label="District Attorney’s Office, link opens in a new window"
            >
              District Attorney’s Office
            </a>
            .)
          </p>
        </div>
      </div>

      <div className="container mx-auto md:my-12 my-2">
        <h2 className="heading-2xl font-semibold mb-4">
          Protecting Community Gardens
        </h2>
        <p className="body-md mb-4">
          To protect community gardens from potential predatory development, we
          have excluded all properties listed by the Pennsylvania Horticultural
          Society and Neighborhoods Garden Trust as community gardens. If you
          believe that a property listed on Clean & Green Philly is a community
          garden, or should be removed from the site for another reason, please
          see our{" "}
          <a href="/request-removal" rel="noopener noreferrer" className="link">
            Request Removal page.
          </a>
        </p>
      </div>

      <div className="container mx-auto md:my-12 my-2">
        <h2 className="heading-2xl font-semibold mb-4">Our Code</h2>

        <p className="body-md mb-4">
          Clean & Green Philly was created by a Code for Philly team. In keeping
          with the open source ethos of Code for Philly, all of the code used to
          build this tool is available on our{" "}
          <a
            href="https://github.com/CodeForPhilly/vacant-lots-proj"
            target="_blank"
            rel="noopener noreferrer"
            className="link"
            aria-label="GitHub repository, link opens in a new window"
          >
            GitHub repository.
          </a>{" "}
          We welcome feature requests, bug reports, code contributions, and
          more.
        </p>
      </div>

      <div className="container mx-auto md:my-12 my-2">
        <h2 className="heading-2xl font-semibold mb-4">Data Sources</h2>

        <p className="body-md mb-4">
          Documentation of the data that we use is available on{" "}
          <a
            href="https://www.figma.com/exit?url=https%3A%2F%2Fgithub.com%2FCodeForPhilly%2Fvacant-lots-proj"
            target="_blank"
            rel="noopener noreferrer"
            className="link"
            aria-label="GitHub repository, link opens in a new window"
          >
            our GitHub repository
          </a>
          . We hope to continue to build out this documentation in the future.
        </p>
      </div>
    </>
  );
}
