import { access_options, PropertyAccess } from "@/config/propertyAccessOptions";
import PropertyAccessOptionCard from "./PropertyAccessOptionCard";

const determineCardEnums = (property: any) => {
  let best;
  let neighbor;
  let available = new Set();
  let unavailable = new Set();

  if (property.access_process === "Private Land Use Agreement") {
    best = PropertyAccess.PRIVATE_LAND_USE;
    available.add(PropertyAccess.BUY_FROM_OWNER);
  }

  if (property.access_process === "Buy Property") {
    best = PropertyAccess.BUY_FROM_OWNER;
    available.add(PropertyAccess.PRIVATE_LAND_USE);
  }

  if (
    !available.has(PropertyAccess.BUY_FROM_OWNER) &&
    best !== PropertyAccess.BUY_FROM_OWNER &&
    property.market_value <= 1000
  ) {
    available.add(PropertyAccess.BUY_FROM_OWNER);
  } else {
    unavailable.add(PropertyAccess.BUY_FROM_OWNER);
  }

  if (
    !available.has(PropertyAccess.PRIVATE_LAND_USE) &&
    best !== PropertyAccess.PRIVATE_LAND_USE
  ) {
    unavailable.add(PropertyAccess.PRIVATE_LAND_USE);
  }

  property.access_process === "Land Bank"
    ? (best = PropertyAccess.LAND_BANK)
    : unavailable.add(PropertyAccess.LAND_BANK);

  property.side_yard_eligible === "Yes"
    ? (neighbor = PropertyAccess.SIDE_YARD)
    : unavailable.add(PropertyAccess.SIDE_YARD);

  property.tactical_urbanism === "Yes"
    ? available.add(PropertyAccess.TACTICAL_URBANISM)
    : unavailable.add(PropertyAccess.TACTICAL_URBANISM);

  property.conservatorship === "Yes"
    ? available.add(PropertyAccess.CONSERVATORSHIP)
    : unavailable.add(PropertyAccess.CONSERVATORSHIP);

  debugger;

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
        <PropertyAccessOptionCard type={"best"} option={access_options[best]} />
      )}
      {available.length > 0 &&
        available.map((opt: PropertyAccess) => (
          <PropertyAccessOptionCard
            key={opt}
            type={"available"}
            option={access_options[opt]}
          />
        ))}
      {neighbor && (
        <PropertyAccessOptionCard
          type={"neighbors"}
          option={access_options[neighbor]}
        />
      )}
      {unavailable.length > 0 &&
        unavailable.map((opt: PropertyAccess) => (
          <PropertyAccessOptionCard
            key={opt}
            type={"unavailable"}
            option={access_options[opt]}
          />
        ))}
    </div>
  );
};

export default PropertyAccessOptionContainer;
