'use client';

import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalFooter,
  useDisclosure,
} from '@nextui-org/react';
import { ThemeButton } from './ThemeButton';
import { PiX } from 'react-icons/pi';
import { useEffect, useState } from 'react';

export default function DataDisclaimerModal() {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [isClientSide, setIsClientSide] = useState(false);

  // Use useEffect to check if modal has been shown and open it if not
  useEffect(() => {
    setIsClientSide(true); // Ensure client-side rendering

    const hasSeenModal = localStorage.getItem('hasSeenModal'); // Check localStorage

    if (!hasSeenModal) {
      onOpen(); // Open modal if not seen before
    }
  }, [onOpen]);

  const closeHandler = () => {
    localStorage.setItem('hasSeenModal', 'true'); // Set flag so modal doesn't show again
    onClose(); // Close modal
  };

  if (!isClientSide) return null;

  return (
    <>
      <Modal
        isOpen={isOpen}
        onOpenChange={onClose}
        size={'3xl'}
        hideCloseButton={true}
        className="items-center"
      >
        <ModalContent>
          <ModalHeader className="flex flex-col gap-1 text-green-600 text-4xl text-center">
            <h2>Disclaimer</h2>
            <ThemeButton
              color="tertiary"
              className="right-4 lg:right-[24px] absolute top-4 min-w-[3rem]"
              aria-label="Close"
              startContent={<PiX />}
              onPress={closeHandler} // Close modal and set flag
            />
          </ModalHeader>

          <ModalBody className="p-10">
            <p>
              🚨 <strong>Note:</strong> Clean & Green Philly ceased active
              development and maintainence in July of 2025. For more
              information, please see{' '}
              <a
                href="https://github.com/CodeForPhilly/clean-and-green-philly/blob/main/docs/PROJECT_BACKGROUND/C%26GP%20Shutdown%20Letter%2C%20June%205%2C%202025.pdf"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:text-blue-800 underline"
              >
                our letter to stakeholders
              </a>
              . The site, codebase, and data will{' '}
              <a
                href="https://github.com/CodeForPhilly/clean-and-green-philly"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:text-blue-800 underline"
              >
                remain available and open source
              </a>{' '}
              for the foreseeable future.
            </p>
            <p className="mt-4">
              The data shown in the map are current as of July 2025, other than
              the vacant properties data, which are from June of 2024, which is{' '}
              <a
                href="http://www.inquirer.com/opinion/commentary/mayor-parker-housing-plan-missing-data-20250625.html"
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:text-blue-800 underline"
              >
                when the City of Philadelphia last collected accurate vacancy
                data
              </a>
              .
            </p>
          </ModalBody>
          <ModalFooter>
            <ThemeButton
              color="primary"
              className=""
              aria-label="Close"
              label="I understand"
              onPress={closeHandler} // Close modal and set flag
            />
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
}
