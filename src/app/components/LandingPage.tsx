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
    alt: "Greened lot in Philadelphia",
  },
];

const LandingPage = () => (
  <div className="container mx-auto px-4">
    <div className="flex flex-col md:flex-row justify-between items-start md:items-center my-10">
      <div className="text-left pr-10">
        <h1 className="text-green-600 text-xl md:text-2xl lg:text-5xl font-thin leading-tight md:leading-[3rem]">
          <span className="block">
            Cleaning and greening vacant properties can{" "}
            <span className="font-extrabold">reduce gun violence</span> in
            neighborhoods by as much as 29%.
          </span>
        </h1>
      </div>
      <div className="flex flex-col justify-between items-end">
        <div className="text-gray-700 mb-4">
          {/* Responsive paragraphs */}
          <p className="hidden md:block">
            This tool can empower you to find the highest-impact properties in
            Philadelphia and take action.
          </p>
        </div>
        <div className="inline-flex space-x-2">
          <Link href="/map">
            <Button size="lg" className="bg-green-600 text-white">
              <ArrowRightIcon className="w-5 h-5 mr-2" />
              Find properties
            </Button>
          </Link>
          <Link href="/about">
            <Button
              size="lg"
              className="bg-transparent border border-green-600 text-green-600"
            >
              <ArrowRightIcon className="w-5 h-5 mr-2" />
              Learn more
            </Button>
          </Link>
        </div>
      </div>
    </div>
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {images.map(({ src, alt }) => (
        <Image
          key={src}
          src={src}
          alt={alt}
          width="100%"
          height="auto"
          radius="none"
        />
      ))}
    </div>
  </div>
);

export default LandingPage;
