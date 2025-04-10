import { PropertyAccessOption } from '@/config/propertyAccessOptions';
import { useFilter } from '@/context/FilterContext';
import { Card, CardBody } from '@nextui-org/react';
import { Check } from '@phosphor-icons/react';
import { IconType } from 'react-icons';

export type PanelProps = Required<
  Omit<PropertyAccessOption, 'primary_description' | 'slug'>
>;

const Panel = ({
  property,
  dimension,
  header,
  secondary_description,
  icon,
}: PanelProps): JSX.Element => {
  const { dispatch, appFilter } = useFilter();
  const currentFilterKeys = appFilter[property]?.values || [];

  const isSelected = currentFilterKeys.includes(dimension); //Fix getting the included property
  const ariaLabel = header.replace(/\s/g, '');
  const Icon = icon;

  const handleTogglePanel = () => {
    const updatedFilterKeys = isSelected
      ? currentFilterKeys.filter((option) => option !== dimension)
      : [...currentFilterKeys, dimension];
    dispatch({
      type: 'SET_DIMENSIONS',
      property,
      dimensions: updatedFilterKeys,
    });
  };

  return (
    <Card
      role="checkbox"
      aria-describedby={ariaLabel}
      aria-checked={isSelected}
      className={isSelected ? 'panelSelected ' : 'panelDefault'}
      isPressable
      onPress={() => handleTogglePanel()}
      shadow="none"
    >
      <CardBody className="flex flex-row justify-between p-[0px]">
        <div className="flex flex-row">
          <div className="mr-3">
            <Icon aria-hidden={true} className="size-8" />
          </div>
          <div className="flex flex-row items-center sm:items-start sm:flex-col lg:flex-row lg:items-center">
            <div className="flex flex-col flex-0">
              <div className="heading-md">{header}</div>
              <div className="body-sm">{secondary_description}</div>
            </div>
          </div>
        </div>
        <div>
          {isSelected ? <Check className="self-end size-5" /> : undefined}
        </div>
      </CardBody>
    </Card>
  );
};

export default Panel;
