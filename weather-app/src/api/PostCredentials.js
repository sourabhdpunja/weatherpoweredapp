import axios from 'axios';

const onPostCredential = async (credential) => {
    try {
        var config = {
            headers: {
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Methods": "GET,HEAD,OPTIONS,POST,PUT",
                "Access-Control-Allow-Headers": "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers",
            },
            credentials: 'include',
        };
        let response = await axios.post('api/weather/postcredentials/', {
            credential
        }, config);
        return response
    } catch (e) {
        let response = {success: true}
        return response;
    }
}

export default onPostCredential;