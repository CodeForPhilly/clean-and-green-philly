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
  slug?: string;
}

export const access_options: Record<PropertyAccess, PropertyAccessOption> = {
  [PropertyAccess.PRIVATE_LAND_USE]: {
    icon: PiHandshake,
    header: "Get permission from Owner",
    description:
      'Properties, given the price an owner, getting a "private land use agreement" seems best.',
    slug: "/get-access#private-land-use",
  },
  [PropertyAccess.TACTICAL_URBANISM]: {
    icon: Rake,
    header: "Tactical Urbanism",
    description:
      "Properties likely safe enough to clean without express permission from the owner.",
  },
  [PropertyAccess.BUY_FROM_OWNER]: {
    icon: PiMoney,
    header: "Buy Affordably from Owner",
    description:
      "Properties cheap enough to buy, with an estimated market value under $1,000.",
    slug: "/get-access#buy-from-owner",
  },
  [PropertyAccess.SIDE_YARD]: {
    icon: PiPottedPlant,
    header: "Purchase as a Side Yard",
    description:
      'If you live next to this property, you may purchase this through the "Side Yard Programs"',
    slug: "/get-access#side-yard",
  },
  [PropertyAccess.LAND_BANK]: {
    icon: PiBank,
    header: "Gain through Land Bank",
    description:
      "Properties owned by the Land Bank and available to buy with discounted prices.",
    slug: "/get-access#land-bank",
  },
  [PropertyAccess.CONSERVATORSHIP]: {
    icon: PiGavel,
    header: "Get Through Conservatorship",
    description:
      'Properties, abandoned and unsafe, which can be gained through a legal "conservatorship"',
    slug: "/get-access#conservatorship",
  },
  [PropertyAccess.DO_NOTHING]: {
    icon: PiXCircle,
    header: "Do Nothing",
    description:
      "We believe access this property legally is too complicated to justify the effort.",
    slug: "/get-access#do-nothing",
  },
};
