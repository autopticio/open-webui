import { WEBUI_BASE_URL } from '$lib/constants';

export const generateJustQueryResponse = async (Query) => {
	let _response = null;

	_response = await sendToAPI(Query);

	//console.log('_response',_response)
	
	return _response;
};

const sendToAPI = async (mensaje) => {
	let error = null;
	let result= null

	const endpoint = localStorage.getItem('autoptic_endpoint');

	let json_env = localStorage.getItem('envFileVariables');
	json_env= JSON.parse(json_env)
	json_env = JSON.stringify(json_env);

	const database64Encoded = btoa(json_env);

	const mensajebase64Encoded = btoa(mensaje)

	const res = await fetch(`${WEBUI_BASE_URL}/api/runPQL`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({
			query:{
				vars: database64Encoded, 
				pql: mensajebase64Encoded
			},
			endpoint: endpoint
		})
	}).catch((err) => {
		error = err;
		return null;
	});

	if (error) {
		throw error;
	}
	result = await res.json()
	return result;
};
