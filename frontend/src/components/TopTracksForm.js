import React, { useState } from 'react';
import classes from "./TopTracksForm.module.css";
import { Button } from '@mui/material';
import DisplayAnalysis from './DisplayTopTracksAnalysis';


function TopTracksForm() {

    const [argument, setArgument] = useState({
        limit:0,
        timeRange: ""
    });

    const [response, setResponse] = useState({
        date: '',
        analysis: ''
    });

    
    const submitHandler = (e) => {
        e.preventDefault();

        // Send the data to flask back end
        fetch('/data', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(argument),
          })
          .then(response => response.json())
          .then(data => {
            // Handle the response from the backend if needed
            setResponse({
                date: data.date,
                analysis: data.message
            })
            console.log(response.date);
          })
          .catch(error => {
            console.error('Error:', error);
          });
    };

    // Define the range of valid integers
    const minInteger = 1;
    const maxInteger = 50;
    const integerOptions = Array.from({ length: maxInteger - minInteger + 1 }, (_, index) => minInteger + index);

    return (
        <div>
            <h1 className={classes.h1}>Analyze Your Recent Top Tracks</h1>
            <form className={classes.form} onSubmit={submitHandler}>
                <label>
                    Select the number of tracks you want to include in the analysis:
                    <select value={argument.limit} onChange={(e) => setArgument({ ...argument, limit: e.target.value })}>
                        <option value="">Select an integer</option>
                        {integerOptions.map((integer) => (
                        <option key={integer} value={integer}>
                            {integer}
                        </option>
                        ))}
                    </select>
                </label>
                <br />
                <label>
                    Select the time range:
                    <select value={argument.timeRange} onChange={(e) => setArgument({ ...argument, timeRange: e.target.value })}>
                        <option value="">Select an option</option>
                        <option value="short_term">short term (last 4 weeks)</option>
                        <option value="medium_term">medium term (last 6 months)</option>
                        <option value="long_term">long term</option>
                    </select>
                </label>
                <br />
                <Button variant="contained" type="submit">Submit</Button>
                
                
            </form>
            <div className={classes.result}>
                <DisplayAnalysis date={response.date} result={response.analysis} />
            </div>
        </div>
    );
}

export default TopTracksForm;