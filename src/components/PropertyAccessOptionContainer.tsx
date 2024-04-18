import { access_options, PropertyAccess } from "@/config/propertyAccessOptions";
import PropertyAccessOptionCard from "./PropertyAccessOptionCard";

const determineCardEnums = (property: any) => {
  let best;
  let neighbor;
  let available = [];
  let unavailable = [];

  property.access_process === "Private Land Use Agreement"
    ? (best = PropertyAccess.PRIVATE_LAND_USE)
    : unavailable.push(PropertyAccess.PRIVATE_LAND_USE);

  property.access_process === "Land Bank"
    ? (best = PropertyAccess.LAND_BANK)
    : unavailable.push(PropertyAccess.LAND_BANK);

  property.access_process === "Buy Property"
    ? (best = PropertyAccess.BUY_FROM_OWNER)
    : property.market_value <= 1000
    ? available.push(PropertyAccess.BUY_FROM_OWNER)
    : unavailable.push(PropertyAccess.BUY_FROM_OWNER);

  property.side_yard_eligible === "Yes"
    ? (neighbor = PropertyAccess.SIDE_YARD)
    : unavailable.push(PropertyAccess.SIDE_YARD);

  property.tactical_urbanism === "Yes"
    ? available.push(PropertyAccess.QUICK_CLEANING)
    : unavailable.push(PropertyAccess.QUICK_CLEANING);

  property.conservatorship === "Yes"
    ? available.push(PropertyAccess.CONSERVATORSHIP)
    : unavailable.push(PropertyAccess.CONSERVATORSHIP);

  return {
    best,
    available,
    neighbor,
    unavailable,
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
