import React, { Component } from 'react';
import PlacesAutocomplete from 'react-places-autocomplete';
import Divider from '@material-ui/core/Divider';
import TextField from '@material-ui/core/TextField';

const _style = {
    container: {
        minHeight: 200,
    },
    textField: {
      marginLeft: 120,
      marginRight: 120,
    },
    location: {
        marginLeft: 120,
        width: '70%',
    },
    divider: {
        height: 1,
    },
};

class LocationComponent extends Component {
    
    renderFunc = ({ getInputProps, getSuggestionItemProps, suggestions, loading }) => {
        console.log(this.props.errorLocationText)
        return(
        <div style={_style.container}>
          <TextField
            required
            style={_style.location}
            margin="normal"
            label="Location"
            error={this.props.error}
            helperText={this.props.errorLocationText}
            {...getInputProps({
                placeholder: 'Eg: Boston',
                className: 'location-search-input',
            })} 
          />
          <div className="autocomplete-dropdown-container">
            {loading && <div style = {_style.textField}>Loading...</div>}
            {suggestions.map(suggestion => {
                const className = suggestion.active
                    ? 'suggestion-item--active'
                    : 'suggestion-item';
                // inline style for demonstration purpose
                const style = suggestion.active
                    ? { backgroundColor: '#fafafa', cursor: 'pointer',  marginLeft: 120,  marginRight: 120 }
                    : { backgroundColor: '#ffffff', cursor: 'pointer',  marginLeft: 120,  marginRight: 120 };
                return (
                    <div
                        {...getSuggestionItemProps(suggestion, {
                            className,
                            style,
                        })}
                    >
                        <span style={_style.position}>{suggestion.description}</span>
                        <Divider style={_style.divider}/>
                    </div>
                );
            })}
          </div>
        </div>);
    };

    render() {
        return (
            <PlacesAutocomplete
                value={this.props.location}
                onChange={this.props.handleChangeAddress}
                onSelect={this.props.handleSelect}
                onError={this.props.helperText}
            >
                {this.renderFunc}
            </PlacesAutocomplete>
        )
    } 
}

export default LocationComponent;