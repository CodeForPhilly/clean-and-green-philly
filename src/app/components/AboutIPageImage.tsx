import Image from "next/image";
import { FC } from "react";


interface AboutPageImageProps{
    src: string;
    alt: string;
}

const AboutPageImage: FC<AboutPageImageProps> = ({
    src,
    alt,
  }) => {
    return (
      <div className="text-center w-1/4">
        <div className="w-full h-64 relative">
          <Image src={src} alt={alt} fill={true} />
        </div>
      </div>
    );
  };

export default AboutPageImage;