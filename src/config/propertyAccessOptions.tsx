import {
  PiBank,
  PiGavel,
  PiHandshake,
  PiMoney,
  PiPottedPlant,
  PiXCircle,
} from "react-icons/pi";
import { Rake } from "@/components/icons/Rake";
import { IconType } from "react-icons";

export enum PropertyAccess {
  PRIVATE_LAND_USE = "PRIVATE_LAND_USE",
  TACTICAL_URBANISM = "TACTICAL_URBANISM",
  BUY_FROM_OWNER = "BUY_FROM_OWNER",
  SIDE_YARD = "SIDE_YARD",
  LAND_BANK = "LAND_BANK",
  CONSERVATORSHIP = "CONSERVATORSHIP",
  DO_NOTHING = "DO_NOTHING",
}

export interface PropertyAccessOption {
  icon: IconType | React.ComponentType<any>;
  header: string;
  description: string;
  alt_description?: string;
  dimension: string;
  property: string;
  slug?: string;
}

export const access_options: Record<PropertyAccess | string, PropertyAccessOption> = {
  [PropertyAccess.PRIVATE_LAND_USE]: {
    icon: PiHandshake,
    header: "Get permission from Owner",
    description:
      'Properties, given the price an owner, getting a "private land use agreement" seems best.',
    alt_description:
      'Properties where you could get a "private land use agreement"',
    dimension: 'Private Land Use Agreement',
    property: 'access_process',
    slug: "/get-access#private-land-use",
  },
  [PropertyAccess.TACTICAL_URBANISM]: {
    icon: Rake,
    header: "Tactical Urbanism",
    description:
      "Properties likely safe enough to clean without express permission from the owner.",
    alt_description:
      'Properties likely safe to quickly clean without express permission',
    dimension: 'Yes',
    property: 'tactical_urbanism'
  },
  [PropertyAccess.BUY_FROM_OWNER]: {
    icon: PiMoney,
    header: "Buy Affordably from Owner",
    description:
      "Properties cheap enough to buy, with an estimated market value under $1,000.",
    alt_description:
      'Properties with a market value under $1,000',
    dimension: 'Buy Property',
    property: 'access_process',
    slug: "/get-access#buy-from-owner",
  },
  [PropertyAccess.SIDE_YARD]: {
    icon: PiPottedPlant,
    header: "Purchase as a Side Yard",
    description:
      'If you live next to this property, you may purchase this through the "Side Yard Programs"',
    alt_description:
      'Properties eligible for the "Side Yard Program"',
    dimension: 'Yes',
    property: 'side_yard_eligible',
    slug: "/get-access#side-yard",
  },
  [PropertyAccess.LAND_BANK]: {
    icon: PiBank,
    header: "Gain through Land Bank",
    description:
      "Properties owned by the Land Bank and available to buy with discounted prices.",
    alt_description:
      'Properties available for discount prices from the Land Bank',
    dimension: 'Land Bank',
    property: 'access_process',
    slug: "/get-access#land-bank",
  },
  [PropertyAccess.CONSERVATORSHIP]: {
    icon: PiGavel,
    header: "Get Through Conservatorship",
    description:
      'Properties, abandoned and unsafe, which can be gained through a legal "conservatorship"',
    alt_description:
      'Abandoned and unsafe properties you can gain through a legal process',
    dimension: 'Yes',
    property: 'conservatorship',
    slug: "/get-access#conservatorship",
  },
  [PropertyAccess.DO_NOTHING]: {
    icon: PiXCircle,
    header: "Do Nothing",
    description:
      "We believe access this property legally is too complicated to justify the effort.",
    dimension: "",
    property: "",
    slug: "/get-access#do-nothing",
  },
};
