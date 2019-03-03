import React from 'react';
import TitleBar from './TitleBar';
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
        <TitleBar />
        <FormContent />
    </div>
);

export default WeatherContainer;