import Image from "next/image";
import { FC } from "react";

interface LandingPageImageProps {
  src: string;
  alt: string;
  captionTitle: string;
  captionBody: string;
}

const LandingPageImage: FC<LandingPageImageProps> = ({
  src,
  alt,
  captionTitle,
  captionBody,
}) => {
  return (
    <div className="text-center w-1/4">
      <div className="w-full h-64 relative">
        <Image src={src} alt={alt} fill={true} />
      </div>
      <h4 className="text-xl mt-2 font-bold pt-5">{captionTitle}</h4>
      <p className="text-lg text-gray-600 pt-5">{captionBody}</p>
    </div>
  );
};

export default LandingPageImage;
