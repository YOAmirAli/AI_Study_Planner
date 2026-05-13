import React from 'react';

const GroupCard = ({ group }) => {
  return (
    <div className="p-4 border rounded shadow">
      {group?.name || 'Group'}
    </div>
  );
};

export default GroupCard;
