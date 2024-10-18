'use client';

import { NextUIProvider } from '@nextui-org/react';
import { FC } from 'react';
import GentrificationPage from './GentrificationPage';

const Gentrification: FC = () => {
  return (
    <NextUIProvider>
      <GentrificationPage />
    </NextUIProvider>
  );
};

export default Gentrification;
