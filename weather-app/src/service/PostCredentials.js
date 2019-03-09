import axios from 'axios';

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
        if (!data || response.status === 400 || response.status === 204){
            return { isError: true } 
        } else if (data.success) {
            return { isSuccess: true } 
        } else if (data.isEmailInvalid) {
            return { errorEmailText: "Email address is invalid. Please enter a valid email address" }
        } else if (data.isEmailPresent)  {
            return { errorEmailText: "Email address already present. Please give a different email Id" }
        } else if (data.isLocationInvalid)  {
            return { errorLocationText: "Location is invalid. Please give a different location" }
        } else {
            return { isError: true }
        }
    } catch (e) {
        return { isError: true }
    }
}

export default onPostCredential;