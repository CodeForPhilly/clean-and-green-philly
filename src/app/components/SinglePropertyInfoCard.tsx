import React, { FC, ReactNode } from 'react';

type SinglePropertyInfoCardProps = {
  title: string;
  body: string;
  icon: ReactNode;
};

const SinglePropertyInfoCard: FC<SinglePropertyInfoCardProps> = ({ title, body, icon }) => {
  return (
    <div className="flex-grow p-3 border border-gray-300 rounded-md">
      <div className="flex gap-4 items-center">
        <div>{icon}</div>
        <div>
          <h4 className="font-bold mb-2 text-xl">{title}</h4>
          <p>{body}</p>
        </div>
      </div>
    </div>
  );
};

export default SinglePropertyInfoCard;
