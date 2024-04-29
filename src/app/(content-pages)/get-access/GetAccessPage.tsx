import { Handshake, Money, Gavel, Tag, XCircle } from "@phosphor-icons/react";

export default function GetAccessPage() {
  return (
    <>
      <h1 className="heading-3xl font-bold mb-6">Get Access to a Property</h1>
      <h2 className="body-lg font-normal mb-6">
        In order to intervene in a property, you need to have some kind of legal
        access to do so.
      </h2>
      <p className="body-md mb-12">
        This means either becoming the owner of the property yourself or
        reaching a legal agreement with the owner to allow you to transform the
        property. For every vacant property in Philadelphia, Clean &amp; Green
        Philly highlights what we think the legal options are to get access to
        it. Below, we explain in more detail what these options are and how you
        can get help with each.
      </p>

      <h2 className="heading-2xl font-bold mb-6">Methods</h2>
      <p className="body-md mb-6">
        Although there are other possible ways to get access to a property (see
        below), these four routes are the most common and the only ones that we
        can infer from publicly-available data. Remember also that each of these
        options depends on your specific context. For example, Act 135
        conservatorship can be a very complicated process and is not necessarily
        suitable for a small community organization that doesn’t have legal
        support. Our goal is to help you understand which of these options is
        best suited for you and, based on that information, identify the
        property or properties where you can have the biggest impact.
      </p>

      <div
        id="private-land-use"
        className="bg-[#E5F8FF] rounded-lg p-8 mt-8 flex items-start"
      >
        <div className="mr-6 flex-shrink-0">
          <Handshake size={60} aria-hidden="true" />
        </div>
        <div>
          <h3 className="heading-xl font-bold mb-4">
            Get Permission from Owner
          </h3>
          <p>
            A private land use agreement can be a fast and easy way to get
            access to a property, provided that you are able to find the owner
            of the property. When creating such an agreement, you must define
            the rights and responsibilities of yourself and the property owner.
            Grounded in Philly provides{" "}
            <a
              href="https://groundedinphilly.org/make-agreement-private-landowner/"
              target="_blank"
              rel="noopener noreferrer"
              className="link"
            >
              a good list of key considerations
            </a>{" "}
            as well as sample agreement language.
          </p>
        </div>
      </div>

      <div
        id="buy-from-owner"
        className="bg-[#E5F8FF] rounded-lg p-8 mt-8 flex items-start"
      >
        <div className="mr-6 flex-shrink-0">
          <Money size={60} aria-hidden="true" />
        </div>
        <div>
          <h3 className="heading-xl font-bold mb-4">Buy from Owner</h3>
          <p>
            Buying a property outright can often be the simplest, fastest way to
            get access to it. However, we recognize that not all properties are
            affordable to grassroots organizations or private individuals. Based
            on our stakeholder research, we mark vacant properties with an
            estimated market value of $1,000 or less as worth buying.
          </p>
        </div>
      </div>

      <div
        id="conservatorship"
        className="bg-[#E5F8FF] rounded-lg p-8 mt-8 flex items-start"
      >
        <div className="mr-6 flex-shrink-0">
          <Gavel size={60} aria-hidden="true" />
        </div>
        <div>
          <h3 className="heading-xl font-bold mb-4">
            Get through Conservatorship
          </h3>
          <p>
            Act 135 conservatorship can potentially be a faster route than other
            legal options but is complicated and requires a lot of resources. In
            short, if a property meets certain specific criteria, it can be
            turned over to a court-appointed conservator for remediation.
            According to the law, it must be unoccupied, abandoned by its owner,
            and unsafe and unhealthy. (For more information, consult{" "}
            <a
              href="https://www.vanderslicelaw.com/service_index/real-estate/act-135/"
              target="_blank"
              rel="noopener noreferrer"
              className="link"
            >
              this explanation of Act 135
            </a>
            .) If those criteria are met, a private individual can petition a
            judge to appoint them as the conservator of the property. The
            conservator is then the owner of the property and can improve it as
            they see fit. However, as mentioned, taking this approach requires
            legal support and significant financial resources. It is therefore
            not an ideal route for small organizations, but may be an option for
            better-resourced organizations such as affordable housing
            developers.
          </p>
        </div>
      </div>

      <div
        id="land-bank"
        className="bg-[#E5F8FF] rounded-lg p-8 mt-8 flex items-start"
      >
        <div className="mr-6 flex-shrink-0">
          <Tag size={60} aria-hidden="true" />
        </div>
        <div>
          <h3 className="heading-xl font-bold mb-4">Get through Land Bank</h3>
          <p className="mb-4">
            The{" "}
            <a
              href="https://phdcphila.org/"
              target="_blank"
              rel="noopener noreferrer"
              className="link"
            >
              Philadelphia Land Bank
            </a>{" "}
            is part of the Philadelphia Housing Development Corporation. It
            works to redistribute publicly-owned land and return vacant
            properties to productive use. Vacant properties owned by the Land
            Bank can often be acquired for nominal or discounted prices for
            certain kinds of uses or projects.
          </p>
          <p>
            The advantage of this process is that it enables grassroots
            organizations and other community-oriented groups to get access to
            land through a non-competitive disposition process at little to no
            cost. However, one is still required to go through the Land Bank’s
            process, which also requires the support of the City Council member
            in whose district the property falls. Grounded in Philly provides a
            good overview of how to{" "}
            <a
              href="https://groundedinphilly.org/get-permission-to-use-land-city/"
              target="_blank"
              rel="noopener noreferrer"
              className="link"
            >
              get permission to use City land
            </a>
            .
          </p>
        </div>
      </div>

      <div
        id="do-nothing"
        className="bg-[#E5F8FF] rounded-lg p-8 mt-8 flex items-start"
      >
        <div className="mr-6 flex-shrink-0">
          <XCircle size={60} aria-hidden="true" />
        </div>
        <div>
          <h3 className="heading-xl font-bold mb-4">Do Nothing </h3>
          <p>
            Although most properties have at least one reasonable way to get
            access to them, in some cases, a property may have a particular
            combination of factors that make it difficult or even impossible to
            get access to. For example, it may be a valuable property owned by a
            company that is planning to develop the property at a later date. If
            the company is unwilling to sell the property or negotiate a private
            land use agreement, there is basically no way to legally get access
            to the property. In these cases, we suggest that a more productive
            use of your time would be to focus on other properties where you can
            more easily pursue an intervention.
          </p>
        </div>
      </div>

      <h2 id="other-methods" className="heading-2xl font-bold mt-8 mb-6">
        Other Methods
      </h2>
      <p className="body-md mb-6">
        The four options mentioned above are not a complete list of ways to get
        access to a vacant property in Philadelphia. There are several others
        worth considering. However, the criteria for these options depend
        completely on your individual circumstances. Since Clean &amp; Green
        Philly only uses public data, we have no way of knowing whether you
        specifically qualify for these programs. However, if you think you might
        qualify for one of these options, we encourage you to consult a tool
        like{" "}
        <a
          href="https://groundedinphilly.org/#pathways"
          target="_blank"
          rel="noopener noreferrer"
          className="link"
        >
          Grounded in Philly’s pathways quiz
        </a>
        , which can better help you understand if you qualify.
      </p>

      <div id="tangled-titles" className="bg-gray-100 rounded-lg p-8 mt-8">
        <h3 className="heading-xl font-bold mb-4">Tangled Titles</h3>
        <p>
          A tangled title is a situation in which the deed to a property lists
          the name of someone other than the apparent owner. This often happens
          when children or grandchildren live in homes that are still listed in
          the name of a deceased parent or grandparent, for example. Tangled
          titles are a major issue in Philadelphia, affecting at least 10,000
          properties, and can contribute to issues of vacancy and neglect. They
          are also difficult to resolve without legal support. If you are the
          rightful owner of a property with a tangled title, or if you believe
          that a vacant property in your neighborhood is the result of a tangled
          title, consider reaching out to{" "}
          <a
            href="https://philalegal.org/services/tangled-title"
            target="_blank"
            rel="noopener noreferrer"
            className="link"
          >
            Philadelphia Legal Assistance
          </a>{" "}
          for help.
        </p>
      </div>

      <div id="adverse-possession" className="bg-gray-100 rounded-lg p-8 mt-8">
        <h3 className="heading-xl font-bold mb-4">Adverse Possession</h3>
        <p>
          If you have been using a specific vacant property for a long time
          against the wishes of the property’s owner, you may qualify for
          adverse possession. This can be a good way to get full legal ownership
          of a property that has been neglected by someone else if you have
          invested effort in maintaining the property yourself (for example, as
          a member of a community garden). However, be aware that this is a very
          complicated process. It usually requires a lawyer and can require
          taking on years of unpaid property taxes. If you believe you may
          qualify for adverse possession, we recommend reaching out to the{" "}
          <a
            href="https://groundedinphilly.org/press/"
            target="_blank"
            rel="noopener noreferrer"
            className="link"
          >
            Garden Justice Legal Initiative
          </a>{" "}
          for help.
        </p>
      </div>

      <div id="side-yard" className="bg-gray-100 rounded-lg p-8 mt-8">
        <h3 className="heading-xl font-bold mb-4">The Side Yard Program</h3>
        <p>
          If you live next to a vacant property, you may be able to buy it from
          the Land Bank to use as a side or rear yard. This is potentially a
          quick and easy way to make productive use of a vacant property, and we
          indicate in our dashboard whether or not a property is eligible for
          this program. If you believe you have the opportunity to acquire a
          vacant property through the side yard program, please consult the{" "}
          <a
            href="https://phdcphila.org/land/buy-land/side-or-rear-yards/"
            target="_blank"
            rel="noopener noreferrer"
            className="link"
          >
            Land Bank’s guide to the side yard acquisition process
          </a>
          .
        </p>
      </div>
    </>
  );
}
