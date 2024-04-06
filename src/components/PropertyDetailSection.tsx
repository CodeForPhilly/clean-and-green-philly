"use client";

import {
  FC,
  useState,
  useMemo,
  useRef,
  useEffect,
  SetStateAction,
  Dispatch,
} from "react";
import { PiArrowRight } from "react-icons/pi";
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
  PaginationProps,
  usePaginationItem,
  usePagination,
  Spinner,
} from "@nextui-org/react";
import PropertyCard from "./PropertyCard";
import SinglePropertyDetail from "./SinglePropertyDetail";
import { BarClickOptions } from "@/app/find-properties/page";
import { MapGeoJSONFeature } from "maplibre-gl";

// const { activePage, range, setPage, onNext, onPrevious } = usePagination({
//   total: 6,
//   showControls: true,
//   siblings: 10,
//   boundaries: 10,
// });

// return (
//   <div className="flex flex-col gap-2">
//     <p>Active page: {activePage}</p>
//     <ul className="flex gap-2 items-center">
//       {range.map((page) => {
//         if (page === PaginationItemType.NEXT) {
//           return (
//             <li key={page} aria-label="next page" className="w-4 h-4">
//               <button
//                 className="w-full h-full bg-default-200 rounded-full"
//                 onClick={onNext}
//               >
//                 <PiArrowRight className="rotate-180" />
//               </button>
//             </li>
//           );
//         }

//         if (page === PaginationItemType.PREV) {
//           return (
//             <li key={page} aria-label="previous page" className="w-4 h-4">
//               <button
//                 className="w-full h-full bg-default-200 rounded-full"
//                 onClick={onPrevious}
//               >
//                 <PiArrowRight />
//               </button>
//             </li>
//           );
//         }

//         if (page === PaginationItemType.DOTS) {
//           return (
//             <li key={page} className="w-4 h-4">
//               ...
//             </li>
//           );
//         }

//         return (
//           <li key={page} aria-label={`page ${page}`} className="w-4 h-4">
//             <button
//               className={cn(
//                 "w-full h-full bg-default-300 rounded-full",
//                 activePage === page && "bg-secondary"
//               )}
//               onClick={() => setPage(page)}
//             />
//           </li>
//         );
//       })}
//     </ul>
//   </div>
// );

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

  // const getItemAriaLabel = (

  //   page?: string | number | undefined,
  //   isActive?: boolean
  // ): string => {
  //   const paginationElements = document.querySelectorAll('nav[aria-label="pagination"] ul li[role="button"]');

  //   if (typeof page === "number") {
  //     const baseLabel = isActive ? `${page}` : `Go to page ${page}`;
  //     return baseLabel.replace("active", ""); // Remove the word 'active' from the label
  //   } else if (page === "prev") {
  //     return "Go to previous page";
  //   } else if (page === "next") {
  //     return "Go to next page";
  //   } else if (page === "prev_5") {
  //     return "Jump Backward 5 Pages";
  //   } else if (page === "next_5") {
  //     return "Jump Forward 5 Pages";
  //   } else if (page === "dots") {
  //     return "Jump 5 Pages";
  //   }
  //   return "";
  // };

  const paginationElements = document.querySelectorAll<HTMLElement>(
    'nav[aria-label="pagination"] ul li[role="button"]'
  );

  console.log(paginationElements);

  const getItemAriaLabel = (
    page?: string | number | undefined,
    isActive?: boolean
  ): string => {
    if (typeof page === "number") {
      const baseLabel = isActive ? `${page}` : `Go to page ${page}`;
      return baseLabel.replace("active", ""); // Remove the word 'active' from the label
      console.log(baseLabel);
    } else if (page === "prev") {
      return "Go to previous page";
    } else if (page === "next") {
      return "Go to next page";
    } else if (page === "prev_5") {
      return "Jump Backward 5 Pages";
    } else if (page === "next_5") {
      return "Jump Forward 5 Pages";
    } else if (page === "dots") {
      return "Jump 5 Pages";
    }
    return "";
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
      <div className="flex flex-wrap flex-grow h-full min-h-[calc(100svh-101px)] max-h-[calc(100svh-101px)]">
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
                getItemAriaLabel={getItemAriaLabel}
                aria-label="pagination"
                isCompact
                showControls
                showShadow
                color="secondary"
                page={page}
                data-dots-jump={false} // Setting data-dots-jump to false to remove ellipses
                total={pages}
                onChange={(newPage) => setPage(newPage)}
                className="example"
              ></Pagination>
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
