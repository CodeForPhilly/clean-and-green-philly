import { FC } from "react";
import DimensionFilter from "./Filters/DimensionFilter";
import { PiX } from "react-icons/pi";
import { BarClickOptions } from "@/app/find-properties/[[...opa_id]]/page";
import { ThemeButton } from "./ThemeButton";

const neighborhoods = ['Academy Gardens', 'Airport', 'Allegheny West', 'Andorra', 'Aston-Woodbridge', 'Bartram Village', 'Bella Vista', 'Belmont', 'Brewerytown', 'Bridesburg', 'Burholme', 'Bustleton', 'Byberry', 'Callowhill', 'Carroll Park', 'Cedar Park', 'Cedarbrook', 'Center City East', 'Chestnut Hill', 'Chinatown', 'Clearview', 'Cobbs Creek', 'Crescentville', 'Crestmont Farms', 'Dearnley Park', 'Dickinson Narrows', 'Dunlap', 'East Falls', 'East Germantown', 'East Kensington', 'East Mount Airy', 'East Oak Lane', 'East Park', 'East Parkside', 'East Passyunk', 'East Poplar', 'Eastwick', 'Elmwood', 'Fairhill', 'Fairmount', 'Feltonville', 'Fern Rock', 'Fishtown - Lower Kensington', 'Fitler Square', 'Fox Chase', 'Francisville', 'Frankford', 'Franklin Mills', 'Franklinville', 'Garden Court', 'Germantown - Morton', 'Germantown - Penn Knox', 'Germantown - Westside', 'Germany Hill', 'Girard Estates', 'Glenwood', 'Graduate Hospital', 'Grays Ferry', 'Greenwich', 'Haddington', 'Harrowgate', 'Hartranft', 'Haverford North', 'Hawthorne', 'Holmesburg', 'Hunting Park', 'Industrial', 'Juniata Park', 'Kingsessing', 'Lawndale', 'Lexington Park', 'Logan', 'Logan Square', 'Lower Moyamensing', 'Ludlow', 'Manayunk', 'Mantua', 'Mayfair', 'McGuire', 'Mechanicsville', 'Melrose Park Gardens', 'Mill Creek', 'Millbrook', 'Modena', 'Morrell Park', 'Navy Yard', 'Newbold', 'Nicetown', 'Normandy Village', 'North Central', 'Northeast Phila Airport', 'Northern Liberties', 'Northwood', 'Ogontz', 'Old City', 'Old Kensington', 'Olney', 'Overbrook', 'Oxford Circle', 'Packer Park', 'Parkwood Manor', 'Paschall', 'Passyunk Square', 'Pennsport', 'Pennypack', 'Pennypack Park', 'Pennypack Woods', 'Penrose', 'Point Breeze', 'Port Richmond', 'Powelton', 'Queen Village', 'Rhawnhurst', 'Richmond', 'Rittenhouse', 'Riverfront', 'Roxborough', 'Roxborough Park', 'Sharswood', 'Society Hill', 'Somerton', 'Southwest Germantown', 'Southwest Schuylkill', 'Spring Garden', 'Spruce Hill', 'Stadium District', 'Stanton', 'Strawberry Mansion', 'Summerdale', 'Tacony', 'Tioga', 'Torresdale', 'University City', 'Upper Kensington', 'Upper Roxborough', 'Walnut Hill', 'Washington Square West', 'West Central Germantown', 'West Kensington', 'West Mount Airy', 'West Oak Lane', 'West Park', 'West Parkside', 'West Passyunk', 'West Poplar', 'West Powelton', 'West Torresdale', 'Whitman', 'Winchester Park', 'Wissahickon', 'Wissahickon Hills', 'Wissahickon Park', 'Wissinoming', 'Wister', 'Woodland Terrace', 'Wynnefield', 'Wynnefield Heights', 'Yorktown']

const filters = [
  {
    property: "priority_level",
    display: "Priority Level",
    options: ["Low", "Medium", "High"],
    tooltip: "For information on how this is calculated, see the About page",
  },
  {
    property: "parcel_type",
    display: "Parcel Type",
    options: ["Land", "Building"],
    tooltip: "Parcel type from City of Philadelphia data",
  },
  {
    property: "access_process",
    display: "Access Process",
    options: ["Buy Property", "Land Bank", "Private Land Use Agreement"],
    tooltip: "For information on what these mean, see the Get Access page",
  },
  {
    property: "neighborhood",
    display: "Neighborhoods",
    options: neighborhoods,
    tooltip: "",
  },
  // {

  // },
  {
    property: "tactical_urbanism",
    display: "Tactical Urbanism",
    options: ["Yes", "No"],
    tooltip: "For an explanation of this, see the Get Access page",
  },
  {
    property: "conservatorship",
    display: "Conservatorship Eligible",
    options: ["Yes", "No"],
    tooltip: "For an explanation of this, see the Get Access page",
  },
  {
    property: "side_yard_eligible",
    display: "Side Yard Eligible",
    options: ["Yes", "No"],
    tooltip: "For an explanation of this, see the Get Access page",
  },
  {
    property: "llc_owner",
    display: "LLC Owner",
    options: ["Yes", "No"],
    tooltip: "For an explanation of this, see the Get Access page",
  },
];

type FilterViewProps = {
  updateCurrentView: (view: BarClickOptions) => void;
};

const FilterView: FC<FilterViewProps> = ({ updateCurrentView }) => {
  return (
    <div className="relative p-6">
      <ThemeButton
        color="secondary"
        className="right-4 lg:right-[24px] absolute top-8 min-w-[3rem]"
        aria-label="Close filter panel"
        startContent={<PiX />}
        onPress={() => updateCurrentView("filter")}
      />
      {filters.map(({ property, display, options, tooltip }) => (
        <DimensionFilter
          key={property}
          property={property}
          options={options}
          display={display}
          tooltip={tooltip}
        />
      ))}
    </div>
  );
};

export default FilterView;
