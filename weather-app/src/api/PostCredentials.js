import axios from 'axios';

const onPostCredential = async (credential) => {
    try {
        let response = await axios.post('http://localhost:3000/api/postCredential', {
            credential
        });
        response = {success: true}
        return response
    } catch (e) {
        console.log("This is Failure ", false)
        let response = {success: true}
        return response;
    }
}

export default onPostCredential;