import React, { Component } from 'react';
import EmailValidator from 'email-validator';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import {
    geocodeByAddress,
    getLatLng,
  } from 'react-places-autocomplete';

import LocationComponent from './LocationComponent';
import onPostCredential from '../../api/PostCredentials'
import LoadingSpinner from './LoadingSpinner';
import SuccessMessage from './SuccessMessage';

const _style = {
    container: {
      display: 'flex',
      flexDirection: 'column',
      width: '100%',
      height: '100%',
      marginTop: 20,
    },
    textField: {
      marginLeft: 120,
      marginRight: 120,
      minHeight: 60,
    },
    buttonContainer: {
        display: 'flex',
    },
    button: {
        marginLeft: 120,
        marginRight: 20,
        width: '71%',
    },
};

class FormLayout extends Component {
    constructor(props) {
        super(props);
        this.state = {
            email: this.props.defaultEmail,
            address: '',
            latitude: '',
            longitude: '',
            errorEmailText: '',
            errorLocationText: '',
            isLoading: false, 
            isSuccess: false,
        };
    }

    handleChange = email => event => {
        this.setState({ email: event.target.value });
    };

    handleChangeAddress = address => {
        this.setState({ address });
    };
     
    handleSelect = address => {
        this.setState({ address });
        geocodeByAddress(address)
          .then(results => getLatLng(results[0]))
          .then(latLng => {
              this.setState({ latitude: latLng.lat});
              this.setState({ longitude: latLng.lng});
              this.setState({ errorLocationText: ''});
            })
          .catch(error => {
              this.setState({ errorLocationText: "Invalid location. Please try again"})
              this.setState({ latitude: ''});
              this.setState({ longitude: ''});
              this.setState({ address: ''});
          });
    };

    submitCredentials = (email, address, latitude, longitude) => {
        if (!EmailValidator.validate(email)){
            this.setState({errorEmailText: "Invalid Email. Please use a valid email address"})
        } else if(!latitude || !longitude || !address) {
            this.setState({ errorEmailText: ''});
            this.setState({errorLocationText: "Please enter valid location."})
        } else {
            this.setState({ errorEmailText: ''});
            this.setState({ errorLocationText: ''});
            console.log("Successfully sent.")
            console.log(email, address, latitude, longitude)
            this.setState({isLoading: true}, () => {
                const response = onPostCredential({email, address, latitude, longitude})
                response.then((response) => {
                    if (response.success){
                        this.setState({ 
                            isLoading: true,
                            isSuccess: false,
                        });
                    } else if (response.isEmailPresent) {
                        this.setState({ 
                            isLoading: false,
                            isSuccess: false,
                            errorEmailText: "Email address already present. Please give a different email Id",
                        });
                    } else {
                        this.setState({ 
                            isLoading: false,
                            isSuccess: false,
                            errorEmailText: "Please try a different emailId",
                            errorLocationText: "Please try a different location.",
                        });
                    }
                })
            });
        }
    };

    render() {
        return (
            <form style={_style.container} autoComplete="on">
                <TextField
                    required
                    id="standard-name"
                    label="Email Address"
                    placeholder="eg: sourabhdpunja@gmail.com"
                    value={this.state.email}
                    style={_style.textField}
                    onChange={this.handleChange('email')}
                    error ={this.state.errorEmailText.length === 0 ? false : true }
                    helperText={this.state.errorEmailText}
                    margin="normal"
                />
                <LocationComponent
                    address = {this.state.address}
                    handleChangeAddress = {this.handleChangeAddress}
                    error ={this.state.errorLocationText.length === 0 ? false : true }
                    handleSelect = {this.handleSelect}
                    errorLocationText={this.state.errorLocationText}
                />
                <div  style={_style.buttonContainer} >
                    <Button 
                        color="primary" 
                        variant="contained" 
                        style={_style.button}
                        disabled={this.state.isLoading}
                        onClick = {() => 
                            this.submitCredentials(
                                this.state.email, this.state.address, this.state.latitude, this.state.longitude
                            )}>
                        Subscribe
                    </Button>
                    {this.state.isLoading ? <LoadingSpinner /> : null}
                </div>
                {this.state.isSuccess ? <SuccessMessage /> : null}
            </form>
        )
    }
};

FormLayout.defaultProps = {
    defaultEmail: '',
};

export default FormLayout;