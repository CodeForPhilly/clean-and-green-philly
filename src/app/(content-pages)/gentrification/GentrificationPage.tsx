export default function GentrificationPage() {
  const fairClothUrl =
    "https://www.brookings.edu/articles/four-reasons-why-more-public-housing-isnt-the-solution-to-affordability-concerns/";

  return (
    <>
      <h1 className="heading-3xl font-bold mb-6">Gentrification</h1>
      <p className="body-md mb-4">
        In cities around the world, new green infrastructure often comes with an
        unwanted tradeoff: as property values rise in response to the new
        amenities, long-term residents are displaced. At Clean &amp; Green
        Philly, we try to avoid contributing to this problem here in
        Philadelphia.As a group explicitly working on cleaning and greening in
        Philly, we recognize that our efforts can inadvertently contribute to
        the displacement of already-marginalized Philadelphians. We also
        recognize that tools like Act 135 conservatorship can lead to negative
        outcomes for poor, Black and brown property owners in particular. This
        is an outcome that we want to avoid. At Clean &amp; Green Philly, we try
        to mitigate the potential harms of our work, such as by holding
        extensive stakeholder engagement with grassroots organizations to get
        their perspectives, or removing known community garden locations from
        our list of properties. That said, there are limits to our knowledge,
        and we welcome constructive suggestions for how we can make Clean &amp;
        Green Philly a more equitable, just tool.
        {/* link for feedback needed after constructive suggestions */}
      </p>
      <p className="body-md mb-4">
        Furthermore, although much can be achieved through better planning and
        design, economic inequality—not green infrastructure—is the root cause
        of displacement. Our work exists within the economic and regulatory
        frameworks of federal, state, and local governments. These frameworks
        impose certain limitation on us—limitations that cannot be overcome
        through planning and design alone. Therefore, in addition to cleaning
        and greening, we encourage people to consider and advocate for solutions
        such as:
      </p>
      <ul className="body-md mb-4 list-disc pl-5 space-y-2">
        <li>
          Zoning reform to address unnecessarily restrictive zoning policies,
          such as those that prohibit structures other than single-family
          housing in most U.S. cities and suburbs{" "}
        </li>
        <li>
          Mandatory citywide affordability laws, which led to a fivefold
          increase in the availability of social housing in France’s wealthiest
          cities
        </li>
        <li>
          City-owned affordable housing, which accounts for 25% of Vienna’s
          housing stock, a system that the Department of Housing and Urban
          Development calls “an effective and innovative model for providing
          superior, affordable housing to the city’s residents.”
        </li>
        <li>
          Meaningful increases in federal funding for public housing (and
          repealing{" "}
          <a
            target="_blank"
            rel="noopener noreferrer nofollow"
            href={fairClothUrl}
            className="link"
          >
            the Faircloth Amendment
          </a>
          )
        </li>
      </ul>
      <p className="body-md mb-4">
        Finally, we emphasize again that displacement is caused by economic
        inequality—not by green infrastructure—and that, without meaningfully
        addressing these underlying inequalities, displacement will continue
        with or without cleaning and greening. Simply put, continuing to neglect
        the quality of life in already-marginalized communities is not a
        solution to displacement. Rather, we advocate for a world in which we
        improve quality of life while also pushing for necessary reforms to the
        economic and regulatory systems that are the root causes of inequality
        and displacement.
      </p>
    </>
  );
}
