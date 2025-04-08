import {
  PiBank,
  PiGavel,
  PiHandshake,
  PiMoney,
  PiPottedPlant,
  PiXCircle,
} from 'react-icons/pi';
import { Rake } from '@/components/icons/Rake';
import { IconType } from 'react-icons';

type PropertyAccessArray = [
  'PRIVATE_LAND_USE',
  'TACTICAL_URBANISM',
  'BUY_FROM_OWNER',
  'SIDE_YARD',
  'LAND_BANK',
  'CONSERVATORSHIP',
  'DO_NOTHING',
];

export const ALL_PROPERTY_ACCESS = [
  'PRIVATE_LAND_USE',
  'TACTICAL_URBANISM',
  'BUY_FROM_OWNER',
  'SIDE_YARD',
  'LAND_BANK',
  'CONSERVATORSHIP',
];

export type PropertyAccess = PropertyAccessArray[number];

export interface PropertyAccessOption {
  icon: IconType | React.ComponentType<any>;
  header: string;
  primary_description: string;
  secondary_description: string;
  property?: string;
  dimension?: string;
  slug?: string;
}

export const access_options: Record<PropertyAccess, PropertyAccessOption> = {
  PRIVATE_LAND_USE: {
    icon: PiHandshake,
    header: 'Get permission from Owner',
    primary_description:
      'Properties, given the price an owner, getting a "private land use agreement" seems best.',
    secondary_description:
      'Properties where you could get a "private land use agreement"',
    dimension: 'Private Land Use Agreement',
    property: 'access_process',
    slug: '/get-access#private-land-use',
  },
  TACTICAL_URBANISM: {
    icon: Rake,
    header: 'Tactical Urbanism',
    primary_description:
      'Properties likely safe enough to clean without express permission from the owner.',
    secondary_description:
      'Properties likely safe to quickly clean without express permission',
    dimension: 'Yes',
    property: 'tactical_urbanism',
  },
  BUY_FROM_OWNER: {
    icon: PiMoney,
    header: 'Buy Affordably from Owner',
    primary_description:
      'Properties cheap enough to buy, with an estimated market value under $1,000.',
    secondary_description: 'Properties with a market value under $1,000',
    dimension: 'Buy Property',
    property: 'access_process',
    slug: '/get-access#buy-from-owner',
  },
  SIDE_YARD: {
    icon: PiPottedPlant,
    header: 'Purchase as a Side Yard',
    primary_description:
      'If you live next to this property, you may purchase this through the "Side Yard Programs"',
    secondary_description: 'Properties eligible for the "Side Yard Program"',
    dimension: 'Yes',
    property: 'side_yard_eligible',
    slug: '/get-access#side-yard',
  },
  LAND_BANK: {
    icon: PiBank,
    header: 'Gain through Land Bank',
    primary_description:
      'Properties owned by the Land Bank and available to buy with discounted prices.',
    secondary_description:
      'Properties available for discount prices from the Land Bank',
    dimension: 'Go through Land Bank',
    property: 'access_process',
    slug: '/get-access#land-bank',
  },
  CONSERVATORSHIP: {
    icon: PiGavel,
    header: 'Get Through Conservatorship',
    primary_description:
      'Properties, abandoned and unsafe, which can be gained through a legal "conservatorship"',
    secondary_description:
      'Abandoned and unsafe properties you can gain through a legal process',
    dimension: 'Yes',
    property: 'conservatorship',
    slug: '/get-access#conservatorship',
  },
  DO_NOTHING: {
    icon: PiXCircle,
    header: 'Do Nothing',
    primary_description:
      'We believe access this property legally is too complicated to justify the effort.',
    secondary_description: '',
    slug: '/get-access#do-nothing',
  },
};
