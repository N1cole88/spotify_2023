import React from 'react';

function CurrentDate() {
  // Create a new Date object to get the current date and time
  const currentDate = new Date();

  // Extract individual components of the date
  const year = currentDate.getFullYear();
  const month = currentDate.getMonth() + 1; // Note: Months are zero-based
  const day = currentDate.getDate();
  
  // You can also get hours, minutes, seconds, and milliseconds if needed
  const hours = currentDate.getHours();
  const minutes = currentDate.getMinutes();
  const seconds = currentDate.getSeconds();

  return (
    <div>
      <p>Current Date: {`${year}-${month}-${day}`}</p>
    </div>
  );
}

export default CurrentDate;
