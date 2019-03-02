import React from 'react';
import PlacesAutocomplete from 'react-places-autocomplete';
import Divider from '@material-ui/core/Divider';
import TextField from '@material-ui/core/TextField';

const _style = {
    textField: {
      marginLeft: 120,
      marginRight: 120,
    },
    location: {
        marginLeft: 120,
        width: '70%',
    },
    divider: {
        height: 2,
    }
};

const renderFunc = ({ getInputProps, getSuggestionItemProps, suggestions, loading }) => (
    <div>
      <TextField
        required
        style={_style.location}
        margin="normal"
        label="Location"
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
                    <span>{suggestion.description}</span>
                    <Divider style={_style.divider}/>
                </div>
            );
        })}
      </div>
    </div>
);

const LocationComponent = (props) => {
    const { address, handleChangeAddress, handleSelect } = props    
    return (
        <PlacesAutocomplete
            value={address}
            onChange={handleChangeAddress}
            onSelect={handleSelect}
            onError={props.helperText}
        >
            {renderFunc}
        </PlacesAutocomplete>
    );
};
export default LocationComponent;