import type { IconType } from 'react-icons';

interface NumberedIconCardProps {
  icon: IconType;
  num: number;
  body: string;
}

/**
 * Renders an numbered icon card component.
 *
 * Initially developed as a infographic component for use in the InfoGraphicSection component.
 */
export const NumberedIconCard = ({
  icon,
  num,
  body,
}: NumberedIconCardProps) => {
  const Icon = icon;
  return (
    <li
      role="listitem"
      className="bg-[#E5F8FF] rounded-lg text-[#077099] p-5 space-y-4"
    >
      <Icon aria-hidden={true} className="size-[60px]" />
      <div className="space-y-2">
        <div className="heading-xl">{num}.</div>
        <div className="heading-md lg:heading-lg">{body}</div>
      </div>
    </li>
  );
};
