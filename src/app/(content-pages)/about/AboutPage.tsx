import { InfoGraphicSection } from '@/components/InfoGraphicSection';
import imageLots from '@/images/Graphic-Lots-Streets.png';
import imageShootings from '@/images/Graphic-Map-Shootings.png';
import imageMerge from '@/images/Graphic-Merge-Data.png';
import imageResearch from '@/images/Graphic-Research-about.png';
import imageSkills from '@/images/Graphic-Skills.png';
import { PiArrowRight } from 'react-icons/pi';

export default function AboutPage() {
  return (
    <>
      <h1 className="heading-3xl font-bold mb-6">About This Project</h1>
      <p className="body-lg mb-6">
        Philadelphia has a gun violence problem. Clean & Green Philly empowers
        Philadelphians to take action to solve it.
      </p>
      <br></br>

      <div id={'problem'} className="mb-20">
        <InfoGraphicSection
          header={{ text: 'The Gun Violence Problem' }}
          body={{
            text: (
              <>
                With homicides trending up since 2013, and a record high of 562
                gun deaths in 2021, community members need concrete solutions.
                Many solutions focus on long-term impact, including nearly 80%
                of the City of Philadelphia&rsquo;s anti-violence spending. But
                immediate, actionable approaches are also needed.
              </>
            ),
          }}
          image={{
            data: imageShootings,
          }}
        />
      </div>

      <div id={'research'} className="my-20">
        <InfoGraphicSection
          header={{ text: 'The Research' }}
          body={{
            text: (
              <>
                Research shows that greening and cleaning vacant properties is
                one of the most impactful, cost-effective interventions
                available to reduce gun violence in a neighborhood. For example,
                Dr. Eugenia South and her team have demonstrated that greening
                vacant lots in Philadelphia reduced gun violence by as much as
                29% in the surrounding area.
              </>
            ),
          }}
          image={{
            data: imageResearch,
            className: 'ring-1 ring-black/5',
          }}
        />
      </div>

      <div id={'challenge'} className="my-20">
        <InfoGraphicSection
          header={{ text: 'The Challenge' }}
          body={{
            text: (
              <>
                Transforming Philadelphia&rsquo;s vacant lots should be a key
                strategy to combating gun violence here. But in a city with
                nearly 40,000 vacant properties, the main obstacle is figuring
                out which properties to prioritize and how to get access to
                them.
              </>
            ),
          }}
          image={{
            data: imageLots,
          }}
        />
      </div>

      <div id={'Vision'} className="my-20">
        <InfoGraphicSection
          header={{ text: 'Our Vision' }}
          body={{
            text: (
              <>
                Our vision was to empower local residents, non-profit
                organizations, and government stakeholders to find and
                prioritize vacant properties for interventions, understand how
                to transform the properties they’ve identified, and connect
                users to resources that can support them.
              </>
            ),
          }}
          image={{
            data: imageSkills,
          }}
        />
      </div>

      <div id={'methodology'} className="my-20">
        <InfoGraphicSection
          header={{ text: 'Our Methodology' }}
          body={{
            text: (
              <>
                We created a dataset based on the original research conducted by
                Dr. Eugenia South and her colleagues, as well as many
                conversations with stakeholders, including community residents,
                CDCs, City government offices, academic researchers, and more.
                We analyzed and combined many data sets on crime, green space,
                and properties.
              </>
            ),
          }}
          image={{
            data: imageMerge,
          }}
          link={{
            icon: PiArrowRight,
            label: 'Learn More',
            href: '/methodology',
          }}
        />
      </div>

      <div id={'faq'} className="my-8">
        <h2 className="heading-2xl font-semibold mb-4">
          Frequently Asked Questions
        </h2>
        <p className="body-md mb-6 italic">
          This FAQ explains how Clean & Green Philly works. For information
          about the project&rsquo;s closure, support, and data policies, please
          see{' '}
          <a
            href="https://github.com/CodeForPhilly/clean-and-green-philly/blob/main/README.md"
            target="_blank"
            rel="noopener noreferrer"
            className="link"
          >
            our README in our GitHub repository
          </a>
          .
        </p>

        <div className="space-y-6">
          <div>
            <h3 className="heading-xl font-semibold mb-3">
              Who can use Clean & Green Philly and what can I do with it?
            </h3>
            <p className="body-md">
              Clean & Green Philly is for residents, community organizations,
              nonprofits, government agencies, and anyone interested in
              improving Philadelphia neighborhoods. You can use it to find
              current information on vacant properties, identify which
              properties need attention most urgently, learn about interventions
              like cleaning or greening, and connect to resources and community
              partners.
            </p>
          </div>

          <div>
            <h3 className="heading-xl font-semibold mb-3">
              What can&rsquo;t Clean & Green Philly do?
            </h3>
            <p className="body-md">
              Clean & Green Philly does not own or manage properties, grant
              legal access or ownership, provide direct funding, guarantee
              outcomes, or resolve land disputes. We are not affiliated with the
              City of Philadelphia. You must follow City and legal processes for
              property access. We connect you to resources and opportunities but
              don&rsquo;t replace the work of City agencies or nonprofits.
            </p>
          </div>

          <div>
            <h3 className="heading-xl font-semibold mb-3">
              What do the priority levels mean?
            </h3>
            <p className="body-md mb-3">
              Priority levels are determined by gun crime density, L&I code
              violations, L&I complaints density, tree canopy coverage, and
              whether the property is already maintained by PHS LandCare:
            </p>
            <ul className="list-disc list-inside space-y-2 body-md ml-4">
              <li>
                <strong>High Priority (red)</strong>: Properties in areas with
                gun crime rates more than one standard deviation above average
                and either have code violations, high complaint density, or are
                not in PHS LandCare. Also includes properties with medium gun
                crime rates that have violations/complaints but aren&rsquo;t in
                PHS LandCare and have very low tree canopy (less than 70%
                coverage).
              </li>
              <li>
                <strong>Medium Priority (yellow)</strong>: Properties in areas
                with gun crime rates between average and one standard deviation
                above average that have violations/complaints and are in PHS
                LandCare, or have violations/complaints but aren&rsquo;t in PHS
                LandCare and have adequate tree canopy. Also includes properties
                with high gun crime rates that are in PHS LandCare but
                don&rsquo;t have violations/complaints and have adequate tree
                canopy.
              </li>
              <li>
                <strong>Low Priority (green)</strong>: Properties in areas with
                gun crime rates at or below average, or properties with medium
                gun crime rates that have no violations/complaints.
              </li>
            </ul>
          </div>

          <div>
            <h3 className="heading-xl font-semibold mb-3">
              All the vacant properties in my area are &lsquo;Low
              Priority&rsquo; but there are real issues. Does this mean my
              neighborhood doesn&rsquo;t matter?
            </h3>
            <p className="body-md">
              No, your neighborhood absolutely matters. We use a very narrow
              definition of &lsquo;high priority&rsquo; - only about 10% of
              vacant properties get this label. This doesn&rsquo;t mean the
              other 90% don&rsquo;t have real challenges. Clean & Green Philly
              was created to help residents and local organizations focus
              limited time and resources on the places where intervention might
              have the biggest impact first. A &lsquo;Low Priority&rsquo; rating
              isn&rsquo;t a judgment about a neighborhood - it&rsquo;s about
              helping everyone be strategic with where to start.
            </p>
          </div>

          <div>
            <h3 className="heading-xl font-semibold mb-3">
              What types of vacancy does Clean and Green Philly NOT show?
            </h3>
            <p className="body-md">
              We focus on vacant land and properties suitable for cleaning,
              greening, or community use. We do not currently map land already
              used for community gardens, vacant commercial storefronts,
              industrial sites, occupied but underused buildings, short-term
              vacancies, vacant units inside occupied apartment buildings, or
              land not suitable for greening due to legal or environmental
              barriers.
            </p>
          </div>
        </div>
      </div>

      <div className="my-8">
        <h2 className="heading-2xl font-semibold mb-4">Acknowledgements</h2>
        <p className="body-md mb-4">
          Clean & Green Philly was built by a team of more than fifty Code for
          Philly volunteers. The project was founded and led by Nissim Lebovits.
          Amanda Soskin was Executive Director. Special thanks are due to our
          board members, Conor Carroll, Dante Leonard, and Claude Schraeder; to
          Jon Geeting and Will Tung at the Center for Philadelphia&rsquo;s Urban
          Future; to our tech leads, Will Budreau, Brandon Cohen, Collum
          Freedman, Tommy Moorman, Arielle Moylen, Marvie Mulder, Hannah Vy
          Nyugen, Gary Pang, Nathaniel Sidwell, Tracy Tran, and Nico Zigouras;
          and to all of the local residents, community leaders, City staff, and
          faculty at the University of Pennsylvania, Temple University, and
          Thomas Jefferson University who informed and supported our work.
        </p>
        <p className="body-md">
          Lastly, we are grateful to Dr. Eugenia South and her colleagues, whose
          work this project depends on.
        </p>
      </div>
      <div className="my-6">
        <h2 className="heading-2xl font-semibold mb-4">Feedback</h2>
        <p className="body-md mb-4">
          If you find issues in this website or would like to offer us feedback,
          please reach out to us at{' '}
          <a
            href="mailto:cleanandgreenphl@gmail.com"
            target="_blank"
            rel="noopener noreferrer"
            className="link"
          >
            cleanandgreenphl@gmail.com.
          </a>{' '}
        </p>
      </div>
      <div className="my-6">
        <h2 className="heading-2xl font-semibold mb-4">Removing Properties</h2>
        <p className="body-md mb-4">
          If you would like to request that we remove a property from the
          dashboard, please see our{' '}
          <a href="/request-removal" className="link">
            Request Removal
          </a>{' '}
          page.
        </p>
      </div>
    </>
  );
}
