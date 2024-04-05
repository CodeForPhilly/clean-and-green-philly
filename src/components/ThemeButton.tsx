import React, { forwardRef } from "react";
import { Button as NextUIButton, Link } from "@nextui-org/react";

type NextUIButtonProps = React.ComponentProps<typeof NextUIButton>;

type ButtonProps = Omit<NextUIButtonProps, "color"> & {
  label?: string | React.ReactNode;
  color?: "primary" | "secondary" | "tertiary";
  isSelected?: boolean;
};

type Ref = HTMLButtonElement;

// override NEXT-UI default styles
const basedStyles = `flex items-center p-2 gap-1 h-[40px] align-middle`;
const removedTransitionStyles = `transition-none hover:transition-none data-[pressed=true]:transition-none data-[pressed=true]:transition-none data-[pressed=true]:scale-100 data-[pressed=true]:skew-x-0 data-[pressed=true]skew-y-0 data-[pressed=true]:rotate-0 data-[pressed=true]:translate-x-0 data-[pressed=true]:translate-y-0`;

const btnColorStyles = {
  primary: `bg-green-600 hover:bg-green-700 active:bg-green-800 text-white`,
  primaryDisabled: `bg-green-600/50 text-white`,
  secondary: `bg-gray-100 hover:bg-gray-200 active:bg-gray-300 text-gray-900 hover:text-gray-900`,
  secondaryDisabled: `bg-gray-100/50 text-gray-900/50`,
  secondarySelected: `bg-green-200 hover:bg-green-300 active:bg-green-400 text-green-700 hover:text-green-700`,
  secondarySelectedDisabled: `bg-green-200/50 text-green-700/50`,
  tertiary: `bg-gray-0 hover:bg-gray-100 active:bg-gray-200 text-gray-900 hover:text-gray-900`,
  tertiaryDisabled: `bg-gray-0 text-gray-900/50`,
  tertiarySelected: `bg-green-100 hover:bg-green-200 active:bg-green-300 text-green-700 hover:text-green-700`,
  tertiarySelectedDisabled: `bg-green-100/50 text-green-700/50`,
};

const getButtonColorStyles = (
  color: string,
  isSelected: boolean,
  isDisabled: boolean
) => {
  let styles;
  if (color === "secondary") {
    if (isSelected) {
      styles = isDisabled
        ? btnColorStyles.secondarySelectedDisabled
        : btnColorStyles.secondarySelected;
    } else {
      styles = isDisabled
        ? btnColorStyles.secondaryDisabled
        : btnColorStyles.secondary;
    }
  } else if (color === "tertiary") {
    if (isSelected) {
      styles = isDisabled
        ? btnColorStyles.tertiarySelectedDisabled
        : btnColorStyles.tertiarySelected;
    } else {
      styles = isDisabled
        ? btnColorStyles.tertiaryDisabled
        : btnColorStyles.tertiary;
    }
  } else {
    // Primary
    styles = isDisabled
      ? btnColorStyles.primaryDisabled
      : btnColorStyles.primary;
  }

  return styles;
};

const ThemeButton = forwardRef<Ref, ButtonProps>(
  (
    {
      label,
      onPress,
      onClick,
      startContent,
      endContent,
      className = "",
      isSelected = false,
      disabled = false,
      isDisabled = false,
      color = "primary",
      isIconOnly = false,
      ...restProps
    },
    ref
  ) => {
    if (!!onClick) {
      throw new Error("onClick is deprecated. Please use onPress instead.");
    }
    const iconOnly = isIconOnly || !label;
    isDisabled = isDisabled || disabled;

    const colorStyles = getButtonColorStyles(color, isSelected, isDisabled);
    const padding = iconOnly ? "p-0" : "py-2.5 px-3";
    const disabledStyles = isDisabled
      ? `cursor-not-allowed ${removedTransitionStyles}`
      : "";
    const iconStyles = "w-5 h-5 text-xl";

    return (
      <NextUIButton
        disableRipple={isDisabled}
        onPress={isDisabled ? undefined : onPress}
        isIconOnly={iconOnly}
        size="md"
        className={`${basedStyles}  ${colorStyles} ${padding} ${disabledStyles} ${className}`}
        ref={ref}
        aria-disabled={isDisabled}
        aria-current={isSelected ? "true" : undefined}
        startContent={
          startContent ? (
            <span className={iconStyles}>{startContent}</span>
          ) : undefined
        }
        endContent={
          endContent ? (
            <span className={iconStyles}>{endContent}</span>
          ) : undefined
        }
        {...restProps}
      >
        {label && <span className="text-base leading-5">{label}</span>}
      </NextUIButton>
    );
  }
);

type ThemeButtonLinkProps = ButtonProps & {
  href: string;
};

const ThemeButtonLink = forwardRef<Ref, ThemeButtonLinkProps>(
  ({ href, ...restProps }, ref) => {
    return (
      <ThemeButton as={Link} role="link" href={href} {...restProps} ref={ref} />
    );
  }
);

export { ThemeButton, ThemeButtonLink };
