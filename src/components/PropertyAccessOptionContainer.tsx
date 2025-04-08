import { access_options, PropertyAccess } from '@/config/propertyAccessOptions';
import PropertyAccessOptionCard from './PropertyAccessOptionCard';

const determineCardEnums = (property: any) => {
  let best: PropertyAccess | undefined;
  let neighbor: PropertyAccess | undefined;
  const available = new Set<PropertyAccess>();
  const unavailable = new Set<PropertyAccess>();

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

  if (property.side_yard_eligible === 'Yes') {
    neighbor = 'SIDE_YARD';
  } else {
    unavailable.add('SIDE_YARD');
  }

  if (property.tactical_urbanism === 'Yes') {
    available.add('TACTICAL_URBANISM');
  } else {
    unavailable.add('TACTICAL_URBANISM');
  }

  if (property.conservatorship === 'Yes') {
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
        <PropertyAccessOptionCard type={'best'} option={access_options[best]} />
      )}
      {available.length > 0 &&
        available.map((opt: PropertyAccess) => (
          <PropertyAccessOptionCard
            key={opt}
            type={'available'}
            option={access_options[opt]}
          />
        ))}
      {neighbor && (
        <PropertyAccessOptionCard
          type={'neighbors'}
          option={access_options[neighbor]}
        />
      )}
      {unavailable.length > 0 &&
        unavailable.map((opt: PropertyAccess) => (
          <PropertyAccessOptionCard
            key={opt}
            type={'unavailable'}
            option={access_options[opt]}
          />
        ))}
    </div>
  );
};

export default PropertyAccessOptionContainer;
