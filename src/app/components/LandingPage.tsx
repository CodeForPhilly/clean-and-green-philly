import { Button, Link, Image } from "@nextui-org/react";
import { ArrowRightIcon } from "@heroicons/react/20/solid";

const images = [
  {
    src: "/dirtyLot.jpg",
    alt: "Dirty lot in Philadelphia",
  },
  {
    src: "/cleaningLot.jpg",
    alt: "Cleaning lot in Philadelphia",
  },
  {
    src: "/greenedLot.jpg",
    alt: "Green lot in Philadelphia",
  },
];

const LandingPage = () => (
  <div className="container mx-auto px-4 py-8">
    <div className="flex flex-col md:flex-row justify-between items-start md:items-center">
      <div className="text-left space-y-4">
      <h1 className="font-light text-green-600 text-5xl">
      Cleaning and greening vacant properties can 
      <br></br>
      <span className="font-semibold"> reduce gun violence </span> 
      in neighborhoods 
      <br></br>
      <span className="font-semibold"> as much as 29%</span>.
      </h1>

        <p className="text-gray-700">This tool can empower you to find the highest impact properties in Philadelphia and take action.</p>
        <div className="flex space-x-4">
          <Link href="/map">
            <Button size="lg" className="bg-green-600 text-white">
              <ArrowRightIcon className="w-5 h-5 mr-2" />
              Find properties
            </Button>
          </Link>
          <Link href="/about">
            <Button size="lg" className="bg-transparent border border-green-600 text-green-600">
              <ArrowRightIcon className="w-5 h-5 mr-2" />
              Learn more
            </Button>
          </Link>
        </div>
      </div>
      <div className="flex flex-row space-x-4 mt-4 md:mt-0">
        {/* Add any additional navigation or informational elements here */}
      </div>
    </div>
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8">
      {images.map(({ src, alt }) => (
        <Image
          key={src}
          src={src}
          alt={alt}
          width="100%"
          height="auto"
        />
      ))}
    </div>
  </div>
);

export default LandingPage;