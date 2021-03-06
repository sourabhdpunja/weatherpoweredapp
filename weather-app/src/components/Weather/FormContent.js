import React, { Component } from 'react';
import PropTypes from 'prop-types';
import EmailValidator from 'email-validator';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import {
    geocodeByAddress,
    getLatLng,
} from 'react-places-autocomplete';

// Custom imports
import LocationComponent from './LocationComponent';
import onPostCredential from '../../service/PostCredentials'
import LoadingSpinner from './LoadingSpinner';
import SuccessMessage from './SuccessMessage';
import ErrorMessage from './ErrorMessage';
import { INVALID_EMAIL_ADDRESS_MSG, INVALID_LOCATION_MSG } from '../../utils/Constants'

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
            email: this.props.email,
            location: this.props.location,
            latitude: '',
            longitude: '',
            errorEmailText: '',
            errorLocationText: '',
            // boolean used to render loading spinner
            isLoading: false,
            // boolean used to render success message
            isSuccess: false,
            // boolean used to render error message
            isError: false,
        };
    }

    handleChange = email => event => {
        this.setState({ email: event.target.value });
    };

    handleChangeAddress = location => {
        this.setState({ location });
    };

    handleSelect = location => {
        this.setState({ location });
        geocodeByAddress(location)
            .then(results => getLatLng(results[0]))
            .then(latLng => {
                this.setState({
                    latitude: parseFloat(latLng.lat.toFixed(4)),
                    longitude: parseFloat(latLng.lng.toFixed(4)),
                    errorLocationText: '',
                });
            })
            .catch(error => {
                this.setState({
                    errorLocationText: INVALID_LOCATION_MSG,
                    latitude: '',
                    longitude: '',
                    location: '',
                });
            });
    };

    submitCredentials = (email, location, latitude, longitude) => {
        email = email.trim()
        if (!EmailValidator.validate(email)) {
            this.setState({ errorEmailText: INVALID_EMAIL_ADDRESS_MSG })
        } else if (!latitude || !longitude || !location) {
            this.setState({
                errorEmailText: "",
                errorLocationText: INVALID_LOCATION_MSG
            });
        } else {
            this.setState({
                errorEmailText: "",
                errorLocationText: "",
            });
            this.setState({ isLoading: true }, () => {
                const response = onPostCredential({ email, location, latitude, longitude })
                response.then((data) => {
                    this.setState({
                        isLoading: false,
                        isSuccess: data.isSuccess,
                        isError: data.isError,
                        errorEmailText: data.errorEmailText || "",
                        errorLocationText: data.errorLocationText || "",
                    });
                });
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
                    placeholder="eg: sourabh@gmail.com"
                    value={this.state.email}
                    style={_style.textField}
                    onChange={this.handleChange('email')}
                    error={this.state.errorEmailText.length > 0}
                    helperText={this.state.errorEmailText}
                    margin="normal"
                />
                <LocationComponent
                    location={this.state.location}
                    handleChangeAddress={this.handleChangeAddress}
                    error={this.state.errorLocationText.length > 0}
                    handleSelect={this.handleSelect}
                    errorLocationText={this.state.errorLocationText}
                />
                <div style={_style.buttonContainer} >
                    <Button
                        color="primary"
                        variant="contained"
                        style={_style.button}
                        disabled={this.state.isLoading}
                        onClick={() =>
                            this.submitCredentials(
                                this.state.email, this.state.location, this.state.latitude, this.state.longitude
                            )}>
                        Subscribe
                    </Button>
                    {this.state.isLoading ? <LoadingSpinner /> : null}
                </div>
                {this.state.isSuccess ? <SuccessMessage /> : null}
                {this.state.isError ? <ErrorMessage /> : null}
            </form>
        )
    }
};

FormLayout.propTypes = {
    email: PropTypes.string,
    location: PropTypes.string,
};

FormLayout.defaultProps = {
    email: '',
    location: '',
};

export default FormLayout;