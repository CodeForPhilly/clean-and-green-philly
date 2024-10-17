'use client';

import { NextUIProvider } from '@nextui-org/react';
import { FC } from 'react';
import RequestRemovalPage from './RequestRemovalPage';

const RequestRemoval: FC = () => {
  return (
    <NextUIProvider>
      <RequestRemovalPage />
    </NextUIProvider>
  );
};

export default RequestRemoval;
