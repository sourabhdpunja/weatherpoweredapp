import React from 'react';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';

const _style = {
  outer: {
    width: '100%',
    display: 'flex',
    flexDirection: 'column',
    marginBottom: '30px'
  },
  bar: {
    backgroundColor: '#3f51b5'
  }
}

const SubscribeBar = () => (
  <div style={_style.outer}>
    <AppBar style={_style.backgroundColor} position="static">
      <Toolbar>
        <Typography variant="h6" color="inherit">
          Weather Powered Email
          </Typography>
      </Toolbar>
    </AppBar>
  </div>
);

export default SubscribeBar;