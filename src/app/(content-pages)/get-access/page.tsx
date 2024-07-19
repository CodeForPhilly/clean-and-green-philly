'use client';

import { NextUIProvider } from '@nextui-org/react';
import { FC } from 'react';
import GetAccessPage from './GetAccessPage';

const GetAccess: FC = () => {
  return (
    <NextUIProvider>
      <GetAccessPage />
    </NextUIProvider>
  );
};

export default GetAccess;
