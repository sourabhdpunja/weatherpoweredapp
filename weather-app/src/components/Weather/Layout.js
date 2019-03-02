import React from 'react';
import WeatherContainer from './WeatherContainer';

const _style = {
    outer: {
        width: '100%',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
    },
}

const Layout = () => (
    <div style={_style.outer}>
        <WeatherContainer/>
    </div>
);

export default Layout