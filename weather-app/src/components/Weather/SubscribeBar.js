import React from 'react';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';

const _style = {
    outer: {
        width: '100%',
        display: 'flex',
        flexDirection: 'column',
    },
}

const SubscribeBar = () => (
    <div style={_style.outer}>
        <AppBar position="static" color="default">
        <Toolbar>
          <Typography variant="h6" color="inherit">
            Subscribe Here
          </Typography>
        </Toolbar>
      </AppBar>
    </div>
);
  
export default SubscribeBar;