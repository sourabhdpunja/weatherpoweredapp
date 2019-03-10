import axios from 'axios';

// Custom imports
import { INVALID_EMAIL_ADDRESS_MSG, EMAIL_ADDRESS_PRESENT_MSG, INVALID_LOCATION_MSG } from '../utils/Constants'

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.withCredentials = true;
const onPostCredential = async (credential) => {
    try {
        var config = {
            headers: {
                'Access-Control-Allow-Origin': '*',
            },
        };
        let response = await axios.post('api/subscriber/', {
            ...credential
        }, config);
        let data = response.data;
        if (!data || response.status === 400 || response.status === 204) {
            return { isError: true }
        } else if (data.success) {
            return { isSuccess: true }
        } else if (data.isEmailInvalid) {
            return { errorEmailText: INVALID_EMAIL_ADDRESS_MSG }
        } else if (data.isEmailPresent) {
            return { errorEmailText: EMAIL_ADDRESS_PRESENT_MSG }
        } else if (data.isLocationInvalid) {
            return { errorLocationText: INVALID_LOCATION_MSG }
        } else {
            return { isError: true }
        }
    } catch (e) {
        return { isError: true }
    }
}

export default onPostCredential;