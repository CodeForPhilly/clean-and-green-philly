import { FC, ReactNode } from "react";
import { ThemeButtonLink } from "./ThemeButton";
import { ArrowUpRight } from "@phosphor-icons/react";

interface Link {
  url: string;
  text: string;
}

type ContentCardProps = {
  image: ReactNode;
  title: string;
  body: string;
  label?: string;
  description?: string;
  labelUpkeep?: string;
  upkeepLevel?: string;
  hasLink: boolean;
  linkurl?: string; // Make linkurl and linktext optional since they are conditionally rendered
  linktext?: string;
  links?: Link[]; // Array of links
};

const ContentCard: FC<ContentCardProps> = ({
  image,
  title,
  body,
  label,
  description,
  linkurl,
  linktext,
  labelUpkeep,
  upkeepLevel,
  hasLink,
  links,
}) => {
  return (
    <div className="bg-green-100 rounded-md">
      <div>{image}</div>
      <div className="flex items-center p-6">
        <div>
          <h4 className="font-bold mb-2 heading-lg">{title}</h4>
          <p>{body}</p>
          <div className="grid gap-4 grid-cols-2 pt-5">
            <div>
              <span className="font-bold">{label}</span> {description}
            </div>
            <div>
              <span className="font-bold">{labelUpkeep}</span> {upkeepLevel}
            </div>
          </div>
          <div className="flex justify-start flex-col !items-start !text-left pt-5 !px-0 pt-5 !mx-0 !my-0">
            {hasLink &&
              links &&
              links.length > 0 &&
              links
                .slice(0, 3)
                .map((link, index) => (
                  <ThemeButtonLink
                    key={index}
                    className="text-blue-700 !bg-green-100 !px-0 !py-0 mb-2 h-5 !text-left !items-start"
                    color="tertiary"
                    aria-label="Link opens in new tab"
                    href={link.url}
                    target="_blank"
                    rel="noreferrer"
                    endContent={
                      <ArrowUpRight className="h-5 w-5" aria-hidden="true" />
                    }
                    label={link.text}
                  />
                ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ContentCard;
