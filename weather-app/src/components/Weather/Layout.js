import React from 'react';
// Custom import
import TitleBar from './TitleBar'
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
    <div>
        <TitleBar />
        <div style={_style.outer}>
            <WeatherContainer/>
        </div>
    </div>
);

export default Layout