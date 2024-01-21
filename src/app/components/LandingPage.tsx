import { Button, Link } from "@nextui-org/react";
import LandingPageImage from "./LandingPageImage";
import { ArrowRightIcon } from "@heroicons/react/20/solid";

const images = [
  {
    src: "/dirtyLot.jpg",
    alt: "Dirty lot in Philadelphia",
    size:"",
  },
  {
    src: "/cleaningLot.jpg",
    alt: "Clean lot in Philadelphia",
    size:"",
  },
  {
    src: "/greenedLot.jpg",
    alt: "Green lot in Philadelphia",
    size:"",
  },
];

const LandingPage = () => (
  <div className="flex flex-col mx-auto pl-32">
    <div className="">
      <div className="text-green-600 md:text-5xl my-10 p-2">
      <p className="leading-normal">Cleaning and greening vacant properties can <br /> <span className="font-bold leading-normal">reduce gun violence</span> in neighborhoods as <br />  much as <span className="font-bold leading-normal">29%.</span></p>
    </div>
    <div className="relative">
      <div className="md:absolute bottom-10 right-6">
        <p className="">This tool can empower anyone to find properties that <br /> would make a significant impact in Philadelphia and <br /> take action.</p>
        <Link href="/map">
          <Button size="lg" className="bg-green-60">
          <ArrowRightIcon className="w-5 h-5 ml-2" />
          Find properties
          </Button>
        </Link>
        <Link href="/about">
          <Button size="lg" color="default">
            <ArrowRightIcon className="w-5 h-5 ml-2" />
            Learn More 
          </Button>
        </Link>
      </div>
    </div>
    </div>
    <div className="scale-x-125 flex space-x-1">
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
