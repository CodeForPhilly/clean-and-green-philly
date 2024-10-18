import { ThemeButtonLink } from '@/components/ThemeButton';
import { ArrowUpRight } from '@phosphor-icons/react';
import Image from 'next/image';
import imageTransformProperty from '@/images/transform-a-property.png';

export default function SupportPage() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-10 items-center">
      <div>
        <h1 className="heading-3xl font-bold mb-6">
          Support Clean & Green Philly
        </h1>
        <p>
          Help us catalyze transformative investment in Philadelphia&#39;s
          vacant properties. Your donation supports us in promoting data-driven
          efforts to improve quality of life across Philadelphia through
          strategic, place-based interventions.
        </p>
        <p className="mt-4">Thank you for supporting Clean & Green Philly!</p>
        <ThemeButtonLink
          className="text-white inline-flex mt-4"
          href="https://fnd.us/clean-and-green-philly/pay"
          target="_blank"
          rel="noopener noreferrer"
          color="primary"
          label="Donate Now"
          endContent={<ArrowUpRight aria-hidden="true" />}
          aria-label="Open donation page in a new tab"
        />
      </div>
      <div className="flex justify-center items-center">
        <div className="relative w-7/12 pb-[105%]">
          <Image
            src={imageTransformProperty}
            alt="Transform a property in Philadelphia"
            className="object-cover object-center rounded-lg"
            fill
            sizes="(max-width: 768px) 58vw, 29vw"
          />
        </div>
      </div>
    </div>
  );
}
