interface FilterDescriptionProps {
  title: string;
  description?: string;
  link?: string;
}

export default function FilterDescription({
  title,
  description,
  link,
}: FilterDescriptionProps): JSX.Element {
  return (
    <div className="flex flex-col mb-2">
      <h2 className="heading-lg">{title}</h2>
      {description && (
        <p className="body-sm text-gray-500 w-[90%] my-1">
          {description}
          {link && (
            <a
              href={link}
              className="link"
              aria-label={`Learn more about ${title.toLowerCase()} from our Methodology Page`}
            >
              Learn more{' '}
            </a>
          )}
        </p>
      )}
    </div>
  );
}
