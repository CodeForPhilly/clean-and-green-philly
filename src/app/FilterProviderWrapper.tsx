"use client";

import { FilterProvider } from "@/context/FilterContext";

export const FilterProviderWrapper = ({
    children,
}: {
    children: React.ReactNode;
}) => {
    return <FilterProvider>{children}</FilterProvider>
}