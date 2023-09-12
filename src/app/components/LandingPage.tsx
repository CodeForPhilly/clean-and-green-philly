import { Button, Link } from "@nextui-org/react";
import LandingPageImage from "./LandingPageImage";

const images = [
  {
    src: "/image1.jpg",
    alt: "Vacant lot in Philadelphia",
    captionTitle: "Search",
    captionBody:
      "Look up specific properties to find out information about them.",
  },
  {
    src: "/image2.jpg",
    alt: "Vacant lot in Philadelphia",
    captionTitle: "Filter",
    captionBody:
      "Filter by neighborhood to find which properties could be cleaned to make a big impact.",
  },
  {
    src: "/image3.jpg",
    alt: "Vacant lot in Philadelphia",
    captionTitle: "Download",
    captionBody: "Download this data to analyze with Excel or other tools.",
  },
];

const LandingPage = () => (
  <div className="container mx-auto pt-20">
    <div className="text-left text-2xl my-10">
      Research has shown that cleaning and greening vacant properties can reduce
      gun violence. This website can help you identify properties where to make
      the most impact.
    </div>
    <div className="flex justify-between space-x-2.5">
      {images.map(({ src, alt, captionTitle, captionBody }) => (
        <LandingPageImage
          key={src}
          src={src}
          alt={alt}
          captionTitle={captionTitle}
          captionBody={captionBody}
        />
      ))}
    </div>
    <div className="flex justify-center mt-20">
      <Link href="/map">
        <Button size="lg" color="primary">
          View Map
        </Button>
      </Link>
    </div>
  </div>
);

export default LandingPage;
