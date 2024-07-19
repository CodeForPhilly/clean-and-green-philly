'use client';

import { NextUIProvider } from '@nextui-org/react';
import { FC } from 'react';
import VPATPage from './VPATPage';

const VPAT: FC = () => {
  return (
    <NextUIProvider>
      <VPATPage />
    </NextUIProvider>
  );
};

export default VPAT;
