import { PropertyAccessOption } from "@/config/propertyAccessOptions";
import { Chip } from "@nextui-org/react";
import Link from "next/link";
import React from "react";
import { PiCaretRight, PiCheck, PiHouse, PiStar, PiX } from "react-icons/pi";
import clsx from "clsx";

interface Props {
  type: "best" | "available" | "neighbors" | "unavailable";
  option: PropertyAccessOption;
}

function getChip(type: Props["type"]) {
  switch (type) {
    case "best":
      return (
        <Chip
          startContent={<PiStar size={18} />}
          classNames={{
            base: `bg-[#BAE4F5] text-[#003144] flex flex-row space-x-1 py-[3px] px-[6px]`,
            content: "body-sm",
          }}
        >
          Best Option
        </Chip>
      );
    case "available":
      return (
        <Chip
          startContent={<PiCheck size={18} />}
          classNames={{
            base: `bg-[#C2F5BA] text-[#094400] flex flex-row space-x-1 py-[3px] px-[6px]`,
            content: "body-sm",
          }}
        >
          Available
        </Chip>
      );
    case "neighbors":
      return (
        <Chip
          startContent={<PiHouse size={18} />}
          classNames={{
            base: `bg-[#FFF0BB] text-[#443500] flex flex-row space-x-1 py-[3px] px-[6px]`,
            content: "body-sm",
          }}
        >
          For Neighbors
        </Chip>
      );
    case "unavailable":
      return (
        <Chip
          startContent={<PiX size={18} />}
          classNames={{
            base: `bg-[#F7C4BC] text-[#440900] flex flex-row space-x-1 py-[3px] px-[6px]`,
            content: "body-sm",
          }}
        >
          Unavailable
        </Chip>
      );
  }
}

function getBackgroundStyle(type: Props["type"]) {
  switch (type) {
    case "best":
      return "bg-[#E5F8FF]";
    case "available":
      return "bg-[#E9FFE5]";
    case "neighbors":
      return "bg-[#FFF5D0]";
    case "unavailable":
      return "bg-[#FFE9E5]";
  }
}

const PropertyAccessOptionCard = ({ type, option }: Props) => {
  const Icon = option.icon;
  const Chip = getChip(type);
  const bgColor = getBackgroundStyle(type);

  const Card = () => (
    <div
      className={`flex flex-row items-center rounded-md p-3 space-x-3 ${bgColor}`}
    >
      <div className="flex-1">
        <Icon aria-hidden={true} className="size-8" />
      </div>
      <div className="flex flex-row items-center sm:items-start sm:flex-col lg:flex-row lg:items-center">
        <div className="flex flex-col flex-0">
          <div className="heading-md">{option.header}</div>
          <div className="body-sm">{option.description}</div>
        </div>
        <div className="ml-2 sm:ml-0 sm:mt-2 lg:ml-2">{Chip}</div>
      </div>
      <div className="flex-1">
        <PiCaretRight
          aria-hidden={true}
          className={clsx("size-6", {
            ["invisible"]: !option.slug,
          })}
        />
      </div>
    </div>
  );

  return option.slug ? (
    <Link href={option.slug}>
      <Card />
    </Link>
  ) : (
    <Card />
  );
};

export default PropertyAccessOptionCard;
