import type { Metadata } from "next";
import { metadata as globalMetadata } from "../app/layout";

export function generateMetadata({
  title,
  description,
  url,
  imageUrl,
}: {
  title: string;
  description: string;
  url: string;
  imageUrl?: string;
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
          alt: title,
        },
      ],
    },
  };
}
