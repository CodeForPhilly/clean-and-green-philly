import Image from 'next/image';
import { Chip } from '@nextui-org/react';
import { toTitleCase } from '../utilities/toTitleCase';

interface PropertyCardProps {
  feature: any;
  setSelectedProperty: (feature: any) => void;
}

function getPriorityClass(priorityLevel: string) {
  switch (priorityLevel) {
    case 'High':
      return 'bg-red-200 text-red-800'; // Style for High Priority
    case 'Medium':
      return 'bg-yellow-200 text-yellow-800'; // Style for Medium Priority
    case 'Low':
      return 'bg-green-200 text-green-800'; // Style for Low Priority
    default:
      return 'bg-gray-500 border-gray-700'; // Default style
  }
}

const PropertyCard = ({ feature, setSelectedProperty }: PropertyCardProps) => {
  const {
    standardized_street_address,
    gun_crimes_density_label,
    priority_level,
    opa_id,
  } = feature.properties;

  const image = `https://storage.googleapis.com/cleanandgreenphl/${opa_id}.jpg`;
  const formattedAddress = toTitleCase(standardized_street_address);
  const priorityClass = getPriorityClass(priority_level);

  const handleClick = () => setSelectedProperty(feature);
  const handleKeyDown = (e: React.KeyboardEvent): void => {
    if (e.key === 'Enter' || e.key === 'Space') {
      handleClick();
    }
  };

  return (
    <div className="sm:max-w-sm w-full lg:w-1/2 max-lg:px-4 max-lg:flex max-lg:justify-center max-lg:mx-auto">
      <div
        className="cursor-pointer max-w-sm w-full h-full"
        onClick={handleClick}
      >
        <div className="bg-white h-full flex flex-col rounded-lg overflow-hidden p-3 hover:bg-gray-100 focus-within:bg-gray-100">
          <div
            className="relative w-full rounded-md overflow-hidden"
            style={{ height: '160px', width: 'auto' }}
          >
            <Image
              src={image}
              alt=""
              layout="fill"
              objectFit="cover"
              unoptimized
            />
          </div>
          <div className="my-3">
            <button
              className="font-bold heading-lg focus:bg-gray-100"
              onKeyDown={handleKeyDown}
            >
              {formattedAddress ?? 'Address not available'}
            </button>
            <div className="text-gray-700 body-sm">
              {gun_crimes_density_label} Gun Crime Rate
            </div>
          </div>
          <Chip
            classNames={{
              base: `${priorityClass} border-small border-white/50`,
              content: 'body-sm',
            }}
          >
            {priority_level + ' Priority'}
          </Chip>
        </div>
      </div>
    </div>
  );
};

export default PropertyCard;
