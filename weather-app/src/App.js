import React from 'react';
import Layout from './components/Weather/Layout';

const _style = {
  outer: {
      width: '100%',
      height: '100%',
  },
}

const App = () => (
  <div style={_style.outer}>
      <Layout/>
  </div>
);


export default App;
