'use client';

import { NextUIProvider } from '@nextui-org/react';
import { FC } from 'react';
import DonatePage from './DonatePage';

const Donate: FC = () => {
  return (
    <NextUIProvider>
      <DonatePage />
    </NextUIProvider>
  );
};

export default Donate;
