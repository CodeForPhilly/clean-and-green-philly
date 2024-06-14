import type { Metadata } from "next";
import { metadata as globalMetadata } from "../app/layout";

//imageUrl and imageAlt included to allow different images to be used for different pages in the future if desired

export function generateMetadata({
  title,
  description,
  url,
  imageUrl,
  imageAlt,
}: {
  title: string;
  description?: string;
  url: string;
  imageUrl?: string;
  imageAlt?: string;
}): Metadata {
  return {
    ...globalMetadata,
    title,
    description,
    openGraph: {
      ...globalMetadata.openGraph,
      url,
      title: `${title} - Clean & Green Philly`,
      description,
      images: [
        {
          url: imageUrl || "/thumbnail.png",
          width: 1200,
          height: 630,
          alt: imageAlt || "Clean & Green Philly",
        },
      ],
    },
  };
}
