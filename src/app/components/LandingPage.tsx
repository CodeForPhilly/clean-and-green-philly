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
  <div className=" mx-auto px-4">
    <div className="flex flex-col md:flex-row justify-between items-start md:items-center my-10">
      <div className="text-left pr-10">
        <h1 className="text-green-600 text-xl md:text-2xl lg:text-5xl font-thin  md:leading-[3rem]">
          <span className="block leading-tight">
            Cleaning and greening vacant <br/> properties can{" "}
            <span className="font-extrabold">reduce gun violence</span> in <br/> neighborhoods <span className="font-extrabold">by as much as 29%.</span>
          </span>
        </h1>
      </div>
      <div className="flex flex-col justify-between items-end px-8">
        <div className="text-gray-700 mb-4">
          {/* Responsive paragraphs */}
          <p className="hidden md:block text-2xl">
            This tool can empower anyone to <br /> find properties that would make a <br /> significant impact in Philadelphia <br /> and take action.
          </p>
        </div>
        <div className="px-16 space-x-2">
          <Link href="/map">
            <Button size="md" className="bg-green-600 text-white">
              <ArrowRightIcon className="w-5 h-5" />
              Find properties
            </Button>
          </Link>
          <Link href="/about">
            <Button size="md"className="bg-transparent border border-green-600 text-green-600"
            >
              <ArrowRightIcon className="w-5 h-5" />
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
