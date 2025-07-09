import { accessOptions, PropertyAccess } from '@/config/propertyAccessOptions';
import PropertyAccessOptionCard from './PropertyAccessOptionCard';

const determineCardEnums = (property: any) => {
  let best: PropertyAccess | undefined;
  let neighbor: PropertyAccess | undefined;
  const available = new Set<PropertyAccess>();
  const unavailable = new Set<PropertyAccess>();

  // Debug logging for Boolean fields
  console.log('Property Boolean fields:', {
    side_yard_eligible: {
      value: property.side_yard_eligible,
      type: typeof property.side_yard_eligible,
      isTrue: property.side_yard_eligible === true,
      isYes: property.side_yard_eligible === 'Yes',
      isTrueString: property.side_yard_eligible === 'True',
      willMatch:
        property.side_yard_eligible === true ||
        property.side_yard_eligible === 'Yes' ||
        property.side_yard_eligible === 'True',
    },
    tactical_urbanism: {
      value: property.tactical_urbanism,
      type: typeof property.tactical_urbanism,
      isTrue: property.tactical_urbanism === true,
      isYes: property.tactical_urbanism === 'Yes',
      isTrueString: property.tactical_urbanism === 'True',
      willMatch:
        property.tactical_urbanism === true ||
        property.tactical_urbanism === 'Yes' ||
        property.tactical_urbanism === 'True',
    },
    conservatorship: {
      value: property.conservatorship,
      type: typeof property.conservatorship,
      isTrue: property.conservatorship === true,
      isYes: property.conservatorship === 'Yes',
      isTrueString: property.conservatorship === 'True',
      willMatch:
        property.conservatorship === true ||
        property.conservatorship === 'Yes' ||
        property.conservatorship === 'True',
    },
  });

  if (property.access_process === 'Private Land Use Agreement') {
    best = 'PRIVATE_LAND_USE';
  }

  if (property.access_process === 'Buy Property') {
    best = 'BUY_FROM_OWNER';
    available.add('PRIVATE_LAND_USE');
  } else if (property.market_value <= 1000) {
    available.add('BUY_FROM_OWNER');
  } else {
    unavailable.add('BUY_FROM_OWNER');
  }

  if (!available.has('PRIVATE_LAND_USE') && best !== 'PRIVATE_LAND_USE') {
    unavailable.add('PRIVATE_LAND_USE');
  }

  if (property.access_process === 'Go through Land Bank') {
    best = 'LAND_BANK';
  } else {
    unavailable.add('LAND_BANK');
  }

  if (
    property.side_yard_eligible === true ||
    property.side_yard_eligible === 'Yes' ||
    property.side_yard_eligible === 'True'
  ) {
    neighbor = 'SIDE_YARD';
  } else {
    unavailable.add('SIDE_YARD');
  }

  if (
    property.tactical_urbanism === true ||
    property.tactical_urbanism === 'Yes' ||
    property.tactical_urbanism === 'True'
  ) {
    available.add('TACTICAL_URBANISM');
  } else {
    unavailable.add('TACTICAL_URBANISM');
  }

  if (
    property.conservatorship === true ||
    property.conservatorship === 'Yes' ||
    property.conservatorship === 'True'
  ) {
    available.add('CONSERVATORSHIP');
  } else {
    unavailable.add('CONSERVATORSHIP');
  }

  return {
    best,
    available: Array.from(available),
    neighbor,
    unavailable: Array.from(unavailable),
  };
};

const PropertyAccessOptionContainer = ({ property }: any) => {
  const { best, available, neighbor, unavailable } =
    determineCardEnums(property);

  return (
    <div className="flex flex-col space-y-2">
      {best && (
        <PropertyAccessOptionCard type={'best'} option={accessOptions[best]} />
      )}
      {available.length > 0 &&
        available.map((opt: PropertyAccess) => (
          <PropertyAccessOptionCard
            key={opt}
            type={'available'}
            option={accessOptions[opt]}
          />
        ))}
      {neighbor && (
        <PropertyAccessOptionCard
          type={'neighbors'}
          option={accessOptions[neighbor]}
        />
      )}
      {unavailable.length > 0 &&
        unavailable.map((opt: PropertyAccess) => (
          <PropertyAccessOptionCard
            key={opt}
            type={'unavailable'}
            option={accessOptions[opt]}
          />
        ))}
    </div>
  );
};

export default PropertyAccessOptionContainer;
