'use client';

import { FC, useState, useMemo, useRef, SetStateAction, Dispatch } from 'react';
import { ThemeButton } from './ThemeButton';
import { PiCaretRight, PiCaretLeft } from 'react-icons/pi';
import {
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
  getKeyValue,
  Pagination,
  PaginationItemType,
  PaginationItemRenderProps,
  Spinner,
} from '@nextui-org/react';
import PropertyCard from './PropertyCard';
import SinglePropertyDetail from './SinglePropertyDetail';
import { BarClickOptions } from '@/app/find-properties/[[...opa_id]]/page';
import { MapGeoJSONFeature } from 'maplibre-gl';
import { X } from '@phosphor-icons/react';
import { useFilter } from '@/context/FilterContext';

const tableCols = [
  {
    key: 'ADDRESS',
    label: 'Address',
  },
  {
    key: 'gun_crimes_density_label',
    label: 'Crime Rate',
  },
  {
    key: 'tree_canopy_gap',
    label: 'Canopy Gap',
  },
];

interface PropertyDetailSectionProps {
  featuresInView: MapGeoJSONFeature[];
  display: 'detail' | 'list';
  loading: boolean;
  selectedProperty: MapGeoJSONFeature | null;
  setSelectedProperty: (property: MapGeoJSONFeature | null) => void;
  setIsStreetViewModalOpen: Dispatch<SetStateAction<boolean>>;
  shouldFilterSavedProperties: boolean;
  setShouldFilterSavedProperties: (shouldFilter: boolean) => void;
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
  shouldFilterSavedProperties,
  setShouldFilterSavedProperties,
  updateCurrentView,
  smallScreenMode,
}) => {
  const [page, setPage] = useState(1);
  const { dispatch } = useFilter();
  const rowsPerPage = 6;
  const pages = Math.ceil(featuresInView.length / rowsPerPage);
  const widthRef = useRef(false);

  const renderItem = (props: PaginationItemRenderProps): React.ReactNode => {
    const {
      ref,
      key,
      value,
      isActive,
      onNext,
      onPrevious,
      setPage,
      className,
    } = props;

    if (value === PaginationItemType.NEXT) {
      return (
        <ThemeButton
          key={key}
          className="content-center bg-gray-100 text-gray-900 min-w-8 w-9 h-9 shadow-none"
          color="secondary"
          aria-label="Go to next page"
          onPress={onNext}
          startContent={<PiCaretRight className="w-5 h-5" />}
        />
      );
    }

    if (value === PaginationItemType.PREV) {
      return (
        <ThemeButton
          isDisabled={page === 1}
          aria-disabled={page === 1}
          key={key}
          className={`${className} ${
            page === 1
              ? 'bg-gray-100/50 text-gray-900/50 hover:bg-gray-100/50 text-gray-900/50'
              : 'content-center bg-gray-100 text-gray-900 min-w-8 w-9 h-9 shadow-none'
          }`}
          color="secondary"
          aria-label={page === 1 ? `No Previous Page` : `Go to Previous Page`}
          onPress={onPrevious}
          isIconOnly={true}
          startContent={<PiCaretLeft />}
        />
      );
    }

    if (value === PaginationItemType.DOTS) {
      return (
        <span key={key} className="bg-white content-center">
          ...
        </span>
      );
    }

    // cursor is the default item
    return (
      <ThemeButton
        key={key}
        ref={ref}
        color="tertiary"
        className={`${className} ${
          isActive
            ? 'text-green-700 !font-normal	bg-green-200 font-bold rounded-md shadow-none content-center'
            : 'bg-white text-gray-900 rounded-md shadow-none rounded-md content-center'
        }`}
        aria-label={isActive ? `Page ${value}` : `Go to page ${value}`}
        aria-current={isActive ? 'page' : false}
        onPress={() => setPage(value)}
        label={value}
      >
        {value}
      </ThemeButton>
    );
  };

  const items = useMemo(() => {
    const start = (page - 1) * rowsPerPage;
    const end = start + rowsPerPage;

    /*Updates the pagination width
      Toggling from map (0 results) to results in mobile causes the component
      to miscalculate the 1st active span since parent width === 0.
    */
    if (typeof window !== 'undefined') {
      widthRef.current =
        (smallScreenMode === 'properties' && window.innerWidth < 640) ||
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
      shouldFilterSavedProperties={shouldFilterSavedProperties}
      setShouldFilterSavedProperties={setShouldFilterSavedProperties}
      updateCurrentView={updateCurrentView}
    />
  ) : featuresInView.length ? (
    <>
      <div className="flex flex-wrap flex-grow h-full min-h-[calc(100svh-101px)] max-h-[calc(100svh-101px)] mt-2">
        {display === 'list' ? (
          <Table
            aria-label="Property Details"
            radius="none"
            removeWrapper
            classNames={{
              th: 'bg-white',
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
                  key={properties?.opa_id}
                  onClick={() => {
                    setSelectedProperty(
                      items.find(
                        (item) =>
                          properties?.opa_id === item?.properties?.opa_id
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
          <>
            <div aria-live="polite" className="sr-only">
              {' '}
              {`You are on page ${page}`}{' '}
            </div>
            {items.map((feature, index) => (
              <PropertyCard
                feature={feature}
                key={index}
                setSelectedProperty={setSelectedProperty}
              />
            ))}
          </>
        )}
        {featuresInView?.length > 0 && widthRef.current && (
          <div>
            <div className="flex w-full justify-center mt-4">
              <Pagination
                role={undefined}
                aria-label="pagination"
                showControls
                page={page}
                total={pages}
                onChange={(newPage) => setPage(newPage)}
                className="shadow-none"
                renderItem={renderItem}
                disableCursorAnimation={true}
              ></Pagination>
            </div>
            <p className="text-center mt-4">
              {`${(page - 1) * 6 + 1} to ${page === pages ? featuresInView.length : page * 6} of ${featuresInView.length}`}
            </p>
            <div className="flex w-full justify-center py-4 px-6">
              <p className="body-sm text-gray-500">
                Note: only the first 100 properties can be viewed in list.
                Filter or zoom in to a smaller area to see more detail.{' '}
              </p>
            </div>
          </div>
        )}
      </div>
    </>
  ) : (
    <>
      <div className="flex w-full my-auto items-center justify-center">
        <div aria-live="polite" className="flex flex-col justify-center">
          <p className="text-center text-xl font-bold">No Results</p>
          <p className="text-center mt-1">
            There are no results that match your filter.
          </p>
          <div className="mx-auto mt-2">
            <ThemeButton
              color="secondary"
              aria-label="Clear Filters"
              label="Clear Filters"
              startContent={<X />}
              onPress={() =>
                dispatch({
                  type: 'CLEAR_DIMENSIONS',
                  property: '',
                  dimensions: [],
                })
              }
            />
          </div>
        </div>
      </div>
    </>
  );
};

export default PropertyDetailSection;
