import React from 'react';
// Custom imports
import SubscribeBar from './SubscribeBar';
import FormContent from './FormContent';

const _style = {
    outer: {
        width: 800,
        height: 450,
        display: 'flex',
        borderStyle: 'groove',
        flexDirection: 'column',
    },
}

const WeatherContainer = () => (
    <div style={_style.outer}>
        <SubscribeBar />
        <FormContent />
    </div>
);

export default WeatherContainer;