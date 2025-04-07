import { useFilter } from '@/context/FilterContext';
import { Card, CardBody } from '@nextui-org/react';
import { Check } from '@phosphor-icons/react';
import { IconType } from 'react-icons';


interface PanelProps {
  property: string;
  header: string;
  description: string;
  icon: IconType | React.ComponentType<any>;
  aria_describedby_label: string;
}

const Panel({property, header, description, icon, aria_describedby_label}: PanelProps): JSX.Element => {
  const {dispatch, appFilter} = useFilter();
  const currentFilterKeys = appFilter[property]?.values || [];

  const isSelected = currentFilterKeys.includes(); //Fix getting the included property

  const handleTogglePanel = () => {
    const updatedFilterKeys = isSelected ? currentFilterKeys.filter(option => option !==  ): [...currentFilterKeys, ];
    dispatch({
      type: 'SET_DIMENSIONS',
      property,
      dimensions: updatedFilterKeys,
    });
  }

  return (
    <Card
      role="checkbox"
      aria-describedby={aria_describedby_label}
      aria-checked={isSelected}
      className={isSelected ? 'panelSelected ' : 'panelDefault'}
      isPressable
      onPress={() => handleTogglePanel()}
      shadow="none"
    >
      <CardBody className="flex flex-row justify-between p-[0px]">
        <div className="flex flex-row">
          <div className="mr-3">
            <icon aria-hidden={true} className="size-8" />
          </div>
          <div className="flex flex-row items-center sm:items-start sm:flex-col lg:flex-row lg:items-center">
            <div className="flex flex-col flex-0">
              <div className="heading-md">{header}</div>
              <div className="body-sm">{description}</div>
            </div>
          </div>
        </div>
        <div>
          {isSelected ? <Check className="self-end size-5" /> : undefined}
        </div>
      </CardBody>
    </Card>
  )
}