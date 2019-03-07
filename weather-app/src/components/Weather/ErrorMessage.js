import React from 'react';

const _style = {
    container: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        marginTop: 10,
    },
    icon: {
        color: 'red',
        marginRight: 10,
    },
};
const ErrorMessage = () => (
  <div style={_style.container}>
    <i className="material-icons" style={_style.icon}>error</i> 
    <div>Registration Unsuccessfull. Please try again later</div>
  </div>
);

export default ErrorMessage;