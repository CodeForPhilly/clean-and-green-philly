import { access_options, PropertyAccess } from "@/config/propertyAccessOptions";
import PropertyAccessOptionCard from "./PropertyAccessOptionCard";

const determineCardEnums = (property: any) => {
  let available = [];
  let unavailable = [];

  const bestCard = () => {
    switch (property.access_process) {
      case "Private Land Use Agreement":
        return PropertyAccess.PRIVATE_LAND_USE;
      case "Land Bank":
        return PropertyAccess.LAND_BANK;
      case "Buy Property":
        return PropertyAccess.BUY_FROM_OWNER;
      default:
        return PropertyAccess.DO_NOTHING;
    }
  };

  property.tactical_urbanism === "Yes"
    ? available.push(PropertyAccess.QUICK_CLEANING)
    : unavailable.push(PropertyAccess.QUICK_CLEANING);

  property.market_value <= 1000
    ? available.push(PropertyAccess.BUY_FROM_OWNER)
    : unavailable.push(PropertyAccess.BUY_FROM_OWNER);

  property.conservatorship === "Yes"
    ? available.push(PropertyAccess.CONSERVATORSHIP)
    : unavailable.push(PropertyAccess.CONSERVATORSHIP);

  property.access_process !== "Land Bank" &&
    available.push(PropertyAccess.LAND_BANK);

  return {
    best: bestCard(),
    available,
    neighbor: PropertyAccess.SIDE_YARD,
    unavailable,
  };
};

const PropertyAccessOptionContainer = ({ property }: any) => {
  const { best, available, neighbor, unavailable } =
    determineCardEnums(property);

  return (
    <div className="flex flex-col space-y-2">
      <PropertyAccessOptionCard type={"best"} option={access_options[best]} />
      {available.map((opt: PropertyAccess) => (
        <PropertyAccessOptionCard
          type={"available"}
          option={access_options[opt]}
        />
      ))}
      <PropertyAccessOptionCard
        type={"neighbors"}
        option={access_options[neighbor]}
      />
      {unavailable.map((opt: PropertyAccess) => (
        <PropertyAccessOptionCard
          type={"unavailable"}
          option={access_options[opt]}
        />
      ))}
    </div>
  );
};

export default PropertyAccessOptionContainer;
