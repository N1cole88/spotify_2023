import React from 'react';
import { useState } from 'react';

function DisplayAnalysis(props) {
    const { receivedData } = props;

    if (receivedData) {
        // Use the receivedData here
        console.log(receivedData);
    }
    return (
        <div>
            <h1>{receivedData ? 'Your result retrieved on' : ''} {props.date}</h1>
            <p>{props.result}</p>
        </div>
    );
}
export default DisplayAnalysis;