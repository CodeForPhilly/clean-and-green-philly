import Image from "next/image";
import { FC } from "react";

interface LandingPageImageProps {
  src: string;
  alt: string;
}

const LandingPageImage: FC<LandingPageImageProps> = ({ src, alt }) => {
  return (
    <div className="w-screen h-screen relative">
      <Image src={src} alt={alt} fill={true} />
    </div>
  );
};

export default LandingPageImage;
