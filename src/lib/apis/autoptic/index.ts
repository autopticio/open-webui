import { AUTOPTIC_BASE_URL } from '$lib/constants';

export const generateJustQueryResponse = async (Query) => {
	let _response = null;

	_response = await sendToAPI(Query);
	
	return _response;
};

const sendToAPI = async (mensaje) => {
	let error = null;
	let result= null

	const endpoint = localStorage.getItem('autoptic_endpoint');

	let json_env = localStorage.getItem('autoptic_environment');
	json_env= JSON.parse(json_env)
	json_env = JSON.stringify(json_env);

	const database64Encoded = btoa(json_env);

	const mensajebase64Encoded = btoa(mensaje)

	const res = await fetch(`${AUTOPTIC_BASE_URL}/runPQL`, {
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


export const insertIframe = async (chatId,messageId, html_to_render) => {
	let responseDiv = document.getElementById("message-" + messageId);

	if (responseDiv) {

		let iframeID = "iframe-" + chatId + messageId;
		let existingIframe = document.getElementById(iframeID);
		if (existingIframe) {
			existingIframe.parentNode?.removeChild(existingIframe);
		}

		var iframe = document.createElement('iframe');
		iframe.id = iframeID;
		iframe.width = "100%";
		iframe.style.border = "none";

		let closeButtonHtml = `
			<button id="closeButton-${iframeID}" style="position: absolute; top: -40px; right: 10px; background: #FF3A3A; border: 0.5px solid #323232; cursor: pointer; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center">
				<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
					<path d="M6 18L18 6M6 6l12 12" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
				</svg>
			</button>
		`;

		if (!html_to_render.includes(`id="closeButton-${iframeID}"`)) {
			html_to_render = `
				<div style="position: relative; top: 40px">
					${html_to_render}
					${closeButtonHtml}
				</div>
			`;
		}

		responseDiv.parentNode.insertBefore(iframe, responseDiv.nextSibling);

		iframe.contentWindow.document.open();
		iframe.contentWindow.document.write(html_to_render);
		iframe.contentWindow.document.close();

		iframe.onload = () => {

			// Let's ensure that the iframe height adjusts to fit the content
			const adjustIframeHeight = () => {
				const iframeDocument = iframe.contentWindow.document;
				const contentHeight = iframeDocument.body.scrollHeight; // Calculate the content height
				iframe.style.height = contentHeight + "px"; // Adjust the iframe height
			};

			adjustIframeHeight();

			iframe.contentWindow.document.getElementById(`closeButton-${iframeID}`).addEventListener('click', function() {
				deleteIframeContent(iframeID, chatId , messageId);
				});
		};

		if (!localStorage.getItem(`iframeContent-${chatId}-${messageId}`)) {
			storeIframeContent(chatId , messageId, html_to_render);
		}
	
	}
}

export function deleteIframeContent(iframeID, chatId , messageId){
	let iframe = document.getElementById(iframeID)

	if (iframe) {
		iframe.parentNode.removeChild(iframe);
		localStorage.removeItem(`iframeContent-${chatId}-${messageId}`);
	}
}

// Function to store iframe content in localStorage
function storeIframeContent(chatId ,messageId, content) {
	localStorage.setItem(`iframeContent-${chatId}-${messageId}`, content);
}

// Function to load iframe content from localStorage
export function loadIframeContent(chatId ,messageId) {
	return localStorage.getItem(`iframeContent-${chatId}-${messageId}`);
}


export const updateAutopticEndpoint = async (token: string, autoptic_endpoint: string) => {
	let error = null;
	const res = await fetch(`${AUTOPTIC_BASE_URL}/keys/new_autoptic_endpoint`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		},
		body: JSON.stringify({ autoptic_endpoint })
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json(); 
		})
		.catch((err) => {
			console.log(err);
			error = err.detail;
			console.log(error)
			return null;
		});
	if (error) {
		throw error;
	}
	return res.autoptic_endpoint;
};

export const getAutopticEndpoint = async (token: string) => {
	let error = null;

	const res = await fetch(`${AUTOPTIC_BASE_URL}/keys/get_autoptic_endpoint`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			error = err.detail;
			return null;
		});
	if (error) {
		throw error;
	}

	return res.autoptic_endpoint;

};

export const deleteAutopticEndpoint = async (token: string) => {
	let error = null;

	const res = await fetch(`${AUTOPTIC_BASE_URL}/keys/delete_autoptic_endpoint`, {
		method: 'DELETE',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			error = err.detail;
			return null;
		});
	if (error) {
		throw error;
	}
	return res;
};

export const updateAutopticEnvironment = async (token: string, autoptic_environment: string, envFileName: string) => {
	let error = null;
	const res = await fetch(`${AUTOPTIC_BASE_URL}/keys/new_autoptic_environment`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		},
		body: JSON.stringify({ autoptic_environment , envFileName })
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json(); 
		})
		.catch((err) => {
			console.log(err);
			error = err.detail;
			console.log(error)
			return null;
		});
	if (error) {
		throw error;
	}
	return res.autoptic_environment;
};

export const getAutopticEnvironment = async (token: string) => {
	let error = null;

	const res = await fetch(`${AUTOPTIC_BASE_URL}/keys/get_autoptic_environment`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			error = err.detail;
			return null;
		});
	if (error) {
		throw error;
	}

	return res.autoptic_environment;

};

export const deleteAutopticEnvironment = async (token: string) => {
	let error = null;

	const res = await fetch(`${AUTOPTIC_BASE_URL}/keys/delete_autoptic_environment`, {
		method: 'DELETE',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			error = err.detail;
			return null;
		});
	if (error) {
		throw error;
	}
	return res;
};

export const getEnvFileName = async (token: string) => {
	let error = null;

	const res = await fetch(`${AUTOPTIC_BASE_URL}/keys/get_envFileName`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			error = err.detail;
			return null;
		});
	if (error) {
		throw error;
	}

	return res.envFileName;

};

// Get List PQL: GET /story/ep/{endpoint_id}/pql
export const getListPQL = async (endpoint_id: string) => {
	let error = null;

	const res = await fetch(`${AUTOPTIC_BASE_URL}/pqls/get_list_pql?endpoint_id=${endpoint_id}`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			// Authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			error = err.detail;
			return null;
		});
	if (error) {
		throw error;
	}

	return res;

};

// Get a snapshot: GET /story/ep/{endpoint_id}/pql/{pql_id}/snap/{format}/{timestamp}/{snapshot_id}
export const getUniqueSnapshot = async (token: string, endpoint_id: string, pql_id: string, format: string, timestamp: string, snapshot_id: string) => {
	let error = null;

	const res = await fetch(`${AUTOPTIC_BASE_URL}/story/ep/${endpoint_id}/pql/${pql_id}/snap/${format}/${timestamp}/${snapshot_id}`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			error = err.detail;
			return null;
		});
	if (error) {
		throw error;
	}

	return res.envFileName;

};

// List snapshots: GET /story/ep/{endpoint_id}/pql/{pql_id}/snap/{format}/{timestamp}
export const getListSnapshots = async (endpoint_id: string, pql_id: string, format: string, timestamp: string) => {
	let error = null;

	const res = await fetch(`${AUTOPTIC_BASE_URL}/snapshots/get_list_snapshot?endpoint_id=${endpoint_id}&pql_id=${pql_id}&format=${format}&timestamp=${timestamp}`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			// Authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			error = err.detail;
			return null;
		});
	if (error) {
		throw error;
	}

	return res;
};

export const readSnapshot = async (endpoint_id: string, pql_id: string, format: string, timestamp: string, snapshot_id: string) => {
	let error = null;

	const res = await fetch(`${AUTOPTIC_BASE_URL}/snapshots/read_snapshot?endpoint_id=${endpoint_id}&pql_id=${pql_id}&format=${format}&timestamp=${timestamp}&snapshot_id=${snapshot_id}`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			// Authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.text();
			return res.text();
		})
		.catch((err) => {
			console.log(err);
			error = err.detail;
			return null;
		});
	if (error) {
		throw error;
	}

	return res;
};

export const deleteSnapshot = async (endpoint_id: string, pql_id: string, format: string, timestamp: string, snapshot_id: string) => {
	let error = null;

	const res = await fetch(`${AUTOPTIC_BASE_URL}/snapshots/delete_snapshot?endpoint_id=${endpoint_id}&pql_id=${pql_id}&format=${format}&timestamp=${timestamp}&snapshot_id=${snapshot_id}`, {
		method: 'DELETE',
		headers: {
			'Content-Type': 'application/json',
			// Authorization: `Bearer ${token}`
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			error = err.detail;
			return null;
		});
	if (error) {
		throw error;
	}

	return res;
};