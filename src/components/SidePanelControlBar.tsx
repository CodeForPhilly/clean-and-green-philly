'use client';

import React, { FC, useMemo, useRef, useEffect } from 'react';
import { BarClickOptions } from '@/app/find-properties/[[...opa_id]]/page';
import { BookmarkSimple, DownloadSimple, Funnel } from '@phosphor-icons/react';
import { ThemeButton } from './ThemeButton';
import { useFilter } from '@/context/FilterContext';
import { getPropertyIdsFromLocalStorage } from '@/utilities/localStorage';
import FilterView from './FilterView'; // Import the FilterView component

type SidePanelControlBarProps = {
  currentView: string;
  featureCount: number;
  loading: boolean;
  savedPropertyCount: number;
  shouldFilterSavedProperties: boolean;
  smallScreenMode: string;
  setShouldFilterSavedProperties: (shouldFilter: boolean) => void;
  updateCurrentView: (view: BarClickOptions) => void;
};

const SearchBarComponent: FC<SidePanelControlBarProps> = ({
  currentView,
  featureCount,
  loading,
  savedPropertyCount,
  shouldFilterSavedProperties,
  smallScreenMode,
  setShouldFilterSavedProperties,
  updateCurrentView,
}) => {
  const filterRef = useRef<HTMLButtonElement | null>(null);
  const savedRef = useRef<HTMLButtonElement | null>(null);
  const filterfocusRef = useRef<HTMLButtonElement | null>(null);

  const { dispatch, appFilter } = useFilter();
  const filterViewRef = useRef<any>(null); // Reference for the FilterView component

  const filterCount: number = useMemo(() => {
    let count = 0;
    for (const property of Object.keys(appFilter)) {
      if (appFilter[property]?.values && property === 'access_process') {
        count += appFilter[property]?.values.length;
      } else {
        count++;
      }
    }
    if (shouldFilterSavedProperties) {
      count--;
    }
    return count;
  }, [appFilter]);

  const onClickSavedButton = () => {
    const propertyIds = getPropertyIdsFromLocalStorage();

    if (shouldFilterSavedProperties) {
      setShouldFilterSavedProperties(false);
      dispatch({
        type: 'SET_DIMENSIONS',
        property: 'opa_id',
        dimensions: [],
      });
    } else {
      setShouldFilterSavedProperties(true);
      dispatch({
        type: 'SET_DIMENSIONS',
        property: 'opa_id',
        dimensions: [...propertyIds],
      });
    }
  };

  // Focus the "X" button inside FilterView after filter is expanded
  useEffect(() => {
    if (currentView === 'filter') {
      // Focus the "X" button inside FilterView using its ID
      const closeButton = document.getElementById('close-filter-button');
      if (closeButton) {
        closeButton.focus();
      }
    }
  });

  return loading ? (
    <div>{/* Keep empty while loading */}</div>
  ) : (
    <>
      <div className="flex justify-between -mx-6 px-12 top-0 py-4 z-10 bg-white">
        {/* Left-aligned content: Total Properties in View */}
        <div className="sm:px-4 lg:px-0 py-2">
          <h1 className="body-md">
            <span className="font-bold">
              {shouldFilterSavedProperties
                ? savedPropertyCount
                : featureCount.toLocaleString()}{' '}
            </span>
            <span className="sm:hidden lg:inline"> Total </span> Properties
          </h1>
        </div>
        {/* Right-aligned content: Buttons */}
        <div
          className="flex items-center space-x-2"
          role="region"
          aria-label="controls"
        >
          {savedPropertyCount > 0 ? (
            <ThemeButton
              color="tertiary"
              aria-label="Saved Properties"
              label={
                <div className="lg:space-x-1 body-md">
                  <span className="max-lg:hidden">Saved</span>
                </div>
              }
              onPress={onClickSavedButton}
              isSelected={shouldFilterSavedProperties}
              startContent={<BookmarkSimple />}
              className={`max-lg:min-w-[4rem] ${
                smallScreenMode === 'map' ? 'max-sm:hidden' : ''
              }`}
              ref={savedRef}
            />
          ) : (
            <></>
          )}
          <ThemeButton
            color="tertiary"
            aria-label={
              filterCount === 0
                ? 'Filter'
                : `Filter ${filterCount} filters active`
            }
            aria-expanded={currentView === 'filter'}
            label={
              <div className="lg:space-x-1 body-md">
                <span className="max-lg:hidden">Filter</span>
                {filterCount !== 0 && (
                  <span aria-hidden="true">({filterCount})</span>
                )}
              </div>
            }
            onPress={() => {
              updateCurrentView('filter');
              filterfocusRef.current?.focus(); // Focus the filter button after pressing
            }}
            isSelected={currentView === 'filter' || filterCount !== 0}
            startContent={<Funnel />}
            className="max-lg:min-w-[4rem]"
            data-hover={false}
            ref={filterRef}
          />
          <ThemeButton
            color="tertiary"
            aria-expanded={currentView === 'download'}
            aria-label="Download"
            onPress={() => updateCurrentView('download')}
            startContent={<DownloadSimple />}
            label={<span className="body-md max-lg:hidden">Download</span>}
            className={`max-md:min-w-[4rem] ${
              smallScreenMode === 'map' ? 'max-sm:hidden' : ''
            } px-0`}
          />
        </div>
      </div>
    </>
  );
};

export default SearchBarComponent;
