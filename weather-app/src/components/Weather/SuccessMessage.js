import React from 'react';

const _style = {
  container: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 10,
  },
  icon: {
    color: 'green',
    marginRight: 10,
  },
};
const SuccessMessage = () => (
  <div style={_style.container}>
    <i className="material-icons" style={_style.icon}>check_circle</i>
    <div>Email Id and Location Successfully Registered</div>
  </div>
);

export default SuccessMessage;