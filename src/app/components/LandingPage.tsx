import { Button, Link } from "@nextui-org/react";
import LandingPageImage from "./LandingPageImage";
import { ArrowRightIcon } from "@heroicons/react/20/solid";

const images = [
  {
    src: "/dirtyLot.jpg",
    alt: "Dirty lot in Philadelphia",
  },
  {
    src: "/cleaningLot.jpg",
    alt: "Clean lot in Philadelphia",
  },
  {
    src: "/greenedLot.jpg",
    alt: "Green lot in Philadelphia",
  },
];

const LandingPage = () => (
  <div className="flex flex-col mx-auto pt-20 pl-32">
    <div className="md:text-5xl my-10 p-2">
      <p className="font-bold">Cleaning and greening vacant <br /> properties can reduce gun violence in <br /> neighborhoods as much as 29%.</p>
    </div>
    <div className="relative">
      <div className="md:absolute bottom-10 right-8">
        <p className="">This tool can empower anyone to find properties that <br /> would make a significant impact in Philadelphia and <br /> take action.</p>
        <Link href="/map">
          <Button size="lg" className="bg-green-60">
           Find properties
          <ArrowRightIcon className="w-5 h-5 ml-2" />
          </Button>
        </Link>
        <Link href="/about">
          <Button size="lg" color="default">
             Learn More 
            <ArrowRightIcon className="w-5 h-5 ml-2" />
          </Button>
        </Link>
      </div>
    </div>
    <div className="scale-150 relative flex justify-between space-x-2 p-10 h-32 ">
      {images.map(({ src, alt,}) => (
        <LandingPageImage
          key={src}
          src={src}
          alt={alt}
        />
      ))}
    </div>
  </div>
);

export default LandingPage;
