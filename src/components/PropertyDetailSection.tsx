"use client";

import { FC, useState, useMemo, useRef, SetStateAction, Dispatch } from "react";
import {
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
  getKeyValue,
  Pagination,
  PaginationItem,
  PaginationItemType,
  Spinner,
} from "@nextui-org/react";
import PropertyCard from "./PropertyCard";
import SinglePropertyDetail from "./SinglePropertyDetail";
import { BarClickOptions } from "@/app/map/page";
import { MapGeoJSONFeature } from "maplibre-gl";

const tableCols = [
  {
    key: "ADDRESS",
    label: "Address",
  },
  {
    key: "guncrime_density",
    label: "Crime Rate",
  },
  {
    key: "tree_canopy_gap",
    label: "Canopy Gap",
  },
];

interface PropertyDetailSectionProps {
  featuresInView: MapGeoJSONFeature[];
  display: "detail" | "list";
  loading: boolean;
  selectedProperty: MapGeoJSONFeature | null;
  setSelectedProperty: (property: MapGeoJSONFeature | null) => void;
  setIsStreetViewModalOpen: Dispatch<SetStateAction<boolean>>;
  smallScreenMode: string;
  updateCurrentView: (view: BarClickOptions) => void;
}

const PropertyDetailSection: FC<PropertyDetailSectionProps> = ({
  featuresInView,
  display,
  loading,
  selectedProperty,
  setSelectedProperty,
  setIsStreetViewModalOpen,
  updateCurrentView,
  smallScreenMode,
}) => {
  const [page, setPage] = useState(1);

  const rowsPerPage = 6;
  const pages = Math.ceil(featuresInView.length / rowsPerPage);
  const widthRef = useRef(false);

  // const isBefore = index < range.indexOf(activePage);

  // Function to customize ARIA labels for pagination items
  const getItemAriaLabel = (page?: string | number | undefined): string => {
    if (typeof page === "number") {
      return `go to page  ${page}`;
    } else if (page === "prev") {
      return "go to previous page";
    } else if (page === "next") {
      return "go to next page";
    } else if (page === "prev_5") {
      return "Jump Backward 5 Pages"; // Customize label for jump backward
    } else if (page === "next_5") {
      return "Jump Forward 5 Pages"; // Customize label for jump forward
    } else if (page === "dots") {
      return "jump 5 pages"; // struggling on a way to identify whether the button is jumping forward or background to apply appropriate label
    }
    return ""; // Default label
  };

  const items = useMemo(() => {
    const start = (page - 1) * rowsPerPage;
    const end = start + rowsPerPage;

    /*Updates the pagination width
      Toggling from map (0 results) to results in mobile causes the component
      to miscalculate the 1st active span since parent width === 0.
    */
    if (typeof window !== "undefined") {
      widthRef.current =
        (smallScreenMode === "properties" && window.innerWidth < 640) ||
        window.innerWidth >= 640;
    }

    if (start > featuresInView.length) {
      setPage(1);
    }

    return featuresInView.slice(start, end);
  }, [page, featuresInView, smallScreenMode]);

  return loading ? (
    <div className="flex-grow h-full">
      {/* Center vertically in screen */}
      <div className="flex w-full justify-center p-4 mt-24">
        <p className="body-md">Loading properties</p>
      </div>
      <div className="flex w-full justify-center">
        <Spinner />
      </div>
    </div>
  ) : selectedProperty ? (
    <SinglePropertyDetail
      property={selectedProperty}
      setSelectedProperty={setSelectedProperty}
      setIsStreetViewModalOpen={setIsStreetViewModalOpen}
      updateCurrentView={updateCurrentView}
    />
  ) : (
    <>
      <div className="flex flex-wrap flex-grow h-full">
        {display === "list" ? (
          <Table
            aria-label="Property Details"
            radius="none"
            removeWrapper
            classNames={{
              th: "bg-white",
            }}
          >
            <TableHeader>
              {tableCols.map((column) => (
                <TableColumn key={column.key}>{column.label}</TableColumn>
              ))}
            </TableHeader>
            <TableBody items={items}>
              {({ properties }) => (
                <TableRow
                  key={properties?.OPA_ID}
                  onClick={() => {
                    setSelectedProperty(
                      items.find(
                        (item) =>
                          properties?.OPA_ID === item?.properties?.OPA_ID
                      ) || null
                    );
                  }}
                >
                  {(columnKey) => (
                    <TableCell>{getKeyValue(properties, columnKey)}</TableCell>
                  )}
                </TableRow>
              )}
            </TableBody>
          </Table>
        ) : (
          items.map((feature, index) => (
            <PropertyCard
              feature={feature}
              key={index}
              setSelectedProperty={setSelectedProperty}
            />
          ))
        )}
        {featuresInView?.length > 0 && widthRef.current && (
          <div>
            <div className="flex w-full justify-center mt-4">
              <Pagination
                role={undefined}
                key={PaginationItemType.DOTS}
                getItemAriaLabel={getItemAriaLabel}
                aria-label="pagination"
                isCompact
                showControls
                showShadow
                color="secondary"
                page={page}
                total={pages}
                onChange={(newPage) => setPage(newPage)}
                dotsJump={5}
                classNames={{
                  ellipsis: "testing-class-names-dots",
                }}
                // renderItem={({ value, index }) => {
                //   console.log(value, index);
                // }}
              />
            </div>
            <div className="flex w-full justify-center py-4 px-6">
              <p className="body-sm text-gray-500">
                Note: only the first 100 properties can be viewed in list.
                Filter or zoom in to a smaller area to see more detail.{" "}
              </p>
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default PropertyDetailSection;
