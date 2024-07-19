'use client';

import { CookieProvider } from '@/context/CookieContext';

export const CookieProviderWrapper = ({
  children,
}: {
  children: React.ReactNode;
}) => {
  return <CookieProvider>{children}</CookieProvider>;
};
