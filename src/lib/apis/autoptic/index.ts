import { AUTOPTIC_BASE_URL } from '$lib/constants';

export const generateJustQueryResponse = async (Query) => {

	const _response = await sendToAPI(Query);
	
	return _response;
};

const sendToAPI = async (message: string) => {

	const endpoint = localStorage.getItem('autoptic_endpoint');

	let json_env = localStorage.getItem('autoptic_environment');
	json_env= JSON.parse(json_env)
	json_env = JSON.stringify(json_env);

	const database64Encoded = btoa(json_env);

	const mensajebase64Encoded = btoa(message)

	try {
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
		})

		const response = await res.json();

		if (!res.ok) {
			throw new Error(response.message || 'Failed to send PQL to API');
		}

		return response;

	} catch (error) {
		console.error('Error sending PQL to API:', error.message);
		return {};
	}
};

export const insertIframe = async (chatId, messageId, html_to_render) => {
    return new Promise((resolve, reject) => {
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
			iframe.style.marginTop = "10px"

            let closeButtonHtml = `
                <button id="closeButton-${iframeID}" style="position: absolute; top: -40px; right: 10px; background: #FF3A3A; border: 0.5px solid #323232; cursor: pointer; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M6 18L18 6M6 6l12 12" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </button>
            `;

            if (!html_to_render.includes(`id="closeButton-${iframeID}"`)) {
                html_to_render = `
                    <div style="position: relative; margin-top: 10px; top: 40px">
                        ${html_to_render}
                        ${closeButtonHtml}
                    </div>
                `;
            }

            responseDiv.parentNode.insertBefore(iframe, responseDiv.nextSibling);

            iframe.contentWindow.document.open();
            iframe.contentWindow.document.write(html_to_render);
            iframe.contentWindow.document.close();
            iframe.style.borderRadius = '20px';     
            iframe.style.overflow = 'hidden';

            iframe.onload = () => {
                const adjustIframeHeight = () => {
                    const iframeDocument = iframe.contentWindow.document;
                    const contentHeight = iframeDocument.body.scrollHeight;
                    iframe.style.height = contentHeight + "px";
                    iframeDocument.body.style.backgroundColor = 'white';
                };

                adjustIframeHeight();

                iframe.contentWindow.document.getElementById(`closeButton-${iframeID}`).addEventListener('click', function() {
                    deleteIframeContent(iframeID, chatId, messageId);
                });

                resolve();
            };

            iframe.onerror = (error) => {
                reject(error);
            };

            if (!localStorage.getItem(`iframeContent-${chatId}-${messageId}`)) {
                storeIframeContent(chatId, messageId, html_to_render);
            }
        } else {
            reject(new Error("Response div not found"));
        }
    });
};

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
	try {
		const res = await fetch(`${AUTOPTIC_BASE_URL}/keys/new_autoptic_endpoint`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${token}`
			},
			body: JSON.stringify({ autoptic_endpoint })
		})
	
		const response = await res.json()
	
		if (!res.ok) {
			throw new Error(response.message || 'Failed to update API URL');
		}
	
		return response.autoptic_endpoint;

	} catch (error) {
		console.error('Error updating API URL:', error.message);
		throw error; 
	}

};

export const getAutopticEndpoint = async (token: string) => {
	try {
		const res = await fetch(`${AUTOPTIC_BASE_URL}/keys/get_autoptic_endpoint`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${token}`
			}
		})

		const response = await res.json()
	
		if (!res.ok) {
			throw new Error(response.message || 'Failed to get API URL');
		}
	
		return response.autoptic_endpoint;

	} catch (error) {
		console.error('Error getting API URL:', error.message);
		throw error;
	}
	
};

export const deleteAutopticEndpoint = async (token: string) => {
	try {
		const res = await fetch(`${AUTOPTIC_BASE_URL}/keys/delete_autoptic_endpoint`, {
			method: 'DELETE',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${token}`
			}
		});

		const response = await res.json();

		if (!res.ok) {
			throw new Error(response.message || 'Failed to delete API URL');
		}

		return response;

	} catch (error) {
		console.error('Error deleting API URL:', error.message);
		throw error;
	}

};

export const updateAutopticEnvironment = async (token: string, autoptic_environment: string, envFileName: string) => {
	try {
		const res = await fetch(`${AUTOPTIC_BASE_URL}/keys/new_autoptic_environment`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${token}`
			},
			body: JSON.stringify({ autoptic_environment , envFileName })
		});

		const response = await res.json();

		if (!res.ok) {
			throw new Error(response.message || 'Failed to update Autoptic environment');
		}

		return response.autoptic_environment;

	} catch (error) {
		console.error('Error updating environment file:', error.message);
		throw error;		
	}

};

export const getAutopticEnvironment = async (token: string) => {
	try {
		const res = await fetch(`${AUTOPTIC_BASE_URL}/keys/get_autoptic_environment`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${token}`
			}
		})

		const response = await res.json();

		if (!res.ok) {
			throw new Error(response.message || 'Failed to get environment file');
		}

		return response.autoptic_environment;

	} catch (error) {
		console.error('Error getting environment file:', error.message);
		throw error;
	}

};

export const deleteAutopticEnvironment = async (token: string) => {

	try {
		const res = await fetch(`${AUTOPTIC_BASE_URL}/keys/delete_autoptic_environment`, {
			method: 'DELETE',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${token}`
			}
		})

		const response = await res.json();

		if (!res.ok) {
			throw new Error(response.message || 'Failed to delete environment file');
		}

		return response;

	} catch (error) {
		console.error('Error deleting environment file:', error.message);
		throw error;
	}

};

export const getEnvFileName = async (token: string) => {

	try {
		const res = await fetch(`${AUTOPTIC_BASE_URL}/keys/get_envFileName`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${token}`
			}
		});

		const response = await res.json();

		if (!res.ok) {
			throw new Error(response.message || 'Failed to get environment name');
		}

		return response.envFileName;

	} catch (error) {
		console.error('Error getting environment name:', error.message);
		throw error;
	}

};

export const healthcheckServerURL = async (token: string, serverURL: string) => {

	try {
		const res = await fetch(`${AUTOPTIC_BASE_URL}/serverconfig/healthcheck`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${token}`
			},
			body: JSON.stringify({ serverURL })
		})

		const response = await res.json();

		if (!res.ok) {
			throw new Error(response.message || 'Failed to check server URL health');
		}

		return response

	} catch (error) {
		console.error('Error checking server URL health:', error.message);
		throw error;
	}

};

export const updateServerURL = async (token: string, serverURL: string) => {

	try {
		const res = await fetch(`${AUTOPTIC_BASE_URL}/serverconfig/new_serverURL`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${token}`
			},
			body: JSON.stringify({ serverURL })
		})

		const response = await res.json();

		if (!res.ok) {
			throw new Error(response.message || 'Failed to update server URL');
		}

		return response.serverURL

	} catch (error) {
		console.error('Error updating server URL:', error.message);
		throw error;
	}

};

export const getServerURL = async (token: string) => {

	try {
		const res = await fetch(`${AUTOPTIC_BASE_URL}/serverconfig/get_serverURL`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${token}`
			}
		});

		const response = await res.json();

		if (!res.ok) {
			throw new Error(response.message || 'Failed to get server URL');
		}

		return response.serverURL

	} catch (error) {
		console.error('Error getting server URL:', error.message);
		throw error;
	}

};

export const deleteServerURL = async (token: string) => {

	try {
		const res = await fetch(`${AUTOPTIC_BASE_URL}/serverconfig/delete_serverURL`, {
			method: 'DELETE',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${token}`
			}
		});

		const response = await res.json();

		if (!res.ok) {
			throw new Error(response.message || 'Failed to delete server URL');
		}

		return response

	} catch (error) {
		console.error('Error deleting server URL:', error.message);
		throw error;
	}

};

export const updateEndpointID = async (token: string, endpointID: string) => {

	try {
		const res = await fetch(`${AUTOPTIC_BASE_URL}/serverconfig/new_endpointID`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${token}`
			},
			body: JSON.stringify({ endpointID })
		});

		const response = await res.json();

		if (!res.ok) {
			throw new Error(response.message || 'Failed to update Endpoint ID');
		}

		return response.endpointID;

	} catch (error) {
		console.error('Error updating Endpoint ID:', error.message);
		throw error;
	}

};

export const getEndpointID = async (token: string) => {

	try {
		const res = await fetch(`${AUTOPTIC_BASE_URL}/serverconfig/get_endpointID`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${token}`
			}
		});

		const response = await res.json();

		if (!res.ok) {
			throw new Error(response.message || 'Failed to get Endpoint ID');
		}

		return response.endpointID;

	} catch (error) {
		console.error('Error getting Endpoint ID:', error.message);
		throw error;
	}

};

export const deleteEndpointID = async (token: string) => {

	try {
		const res = await fetch(`${AUTOPTIC_BASE_URL}/serverconfig/delete_endpointID`, {
			method: 'DELETE',
			headers: {
				'Content-Type': 'application/json',
				Authorization: `Bearer ${token}`
			}
		});

		const response = await res.json();

		if (!res.ok) {
			throw new Error(response.message || 'Failed to delete Endpoint ID');
		}

		return response;

	} catch (error) {
		console.error('Error deleting Endpoint ID:', error.message);
		throw error;
	}
};

//////////////////////////////////////////////////////////////////////////////////////////////////////////
// GO SERVER FUNCTIONS
//////////////////////////////////////////////////////////////////////////////////////////////////////////

// Get List PQL: GET /story/ep/{endpoint_id}/pql

export const getListPQL = async () => {

	const serverURL = localStorage.getItem('serverURL');
	const endpoint_id = localStorage.getItem('endpointID');

	try {
		const res = await fetch(`${AUTOPTIC_BASE_URL}/pqls/get_list_pql?endpoint_id=${endpoint_id}&serverURL=${encodeURIComponent(serverURL)}`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
			}
		});

		const response = await res.json();

		if (!res.ok) { 
			throw new Error(response.message || 'Failed to fetch PQL list');
		}

		return response

	} catch (error) {
		console.error('Error fetching PQL list:', error.message);
		return [];
	}

};

export const getDefaultListSnapshots = async (window: string) => {

	const serverURL = localStorage.getItem('serverURL');
	const endpoint_id = localStorage.getItem('endpointID');

	try {
		const res = await fetch(`${AUTOPTIC_BASE_URL}/snapshots/get_default_list_snapshot?endpoint_id=${endpoint_id}&window=${window}&serverURL=${encodeURIComponent(serverURL)}`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				// Authorization: `Bearer ${token}`
			}
		});

		const response = await res.json();

		if (!res.ok) { 
			throw new Error(response.message || 'Failed to fetch snapshots');
		}

		return response

	} catch (error) {
		console.error('Error fetching snapshots:', error.message);
		return [];
	}

};

// List snapshots: GET /story/ep/{endpoint_id}/pql/{pql_id}/snap/{format}/{timestamp}

// This function is not use now. It will be used in the future

export const getListSnapshots = async (pql_id: string, format: string, timestamp: string) => {

	const serverURL = localStorage.getItem('serverURL');
	const endpoint_id = localStorage.getItem('endpointID');

	try {
		const res = await fetch(`${AUTOPTIC_BASE_URL}/snapshots/get_list_snapshot?endpoint_id=${endpoint_id}&pql_id=${pql_id}&format=${format}&timestamp=${timestamp}&serverURL=${encodeURIComponent(serverURL)}`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				// Authorization: `Bearer ${token}`
			}
		});

		const response = await res.json();

		if (!res.ok) { 
			throw new Error(response.message || 'Failed to fetch PQL list');
		}

		return response

	} catch (error) {
		console.error('Error fetching snapshots:', error.message);
		return [];
	}

};

// This function is not use now. It will be used in the future

export const getWindowListSnapshots = async (pql_id: string, format: string, timestamp: string) => {

	const serverURL = localStorage.getItem('serverURL');
	const endpoint_id = localStorage.getItem('endpointID');

	try {
		const res = await fetch(`${AUTOPTIC_BASE_URL}/snapshots/get_list_snapshot?endpoint_id=${endpoint_id}&pql_id=${pql_id}&format=${format}&timestamp=${timestamp}&serverURL=${encodeURIComponent(serverURL)}`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				// Authorization: `Bearer ${token}`
			}
		});

		const response = await res.json();

		if (!res.ok) { 
			throw new Error(response.message || 'Failed to fetch PQL list');
		}

		return response

	} catch (error) {
		console.error('Error fetching snapshots:', error.message);
		return [];
	}

};



export const readSnapshot = async (pql_id: string, format: string, timestamp: string, snapshot_id: string) => {

	const serverURL = localStorage.getItem('serverURL');
	const endpoint_id = localStorage.getItem('endpointID');

	try {
		const res = await fetch(`${AUTOPTIC_BASE_URL}/snapshots/read_snapshot?endpoint_id=${endpoint_id}&pql_id=${pql_id}&format=${format}&timestamp=${timestamp}&snapshot_id=${snapshot_id}&serverURL=${encodeURIComponent(serverURL)}`, {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json',
				// Authorization: `Bearer ${token}`
			}
		});

		const response = await res.text();

		if (!res.ok) { 
			throw new Error(response.message || 'Failed to read the snapshot');
		}

		return response;

	} catch (error) {
		console.error('Error reading the snapshot:', error.message);
		throw error;
	}

};

export const deleteSnapshot = async (pql_id: string, format: string, timestamp: string, snapshot_id: string) => {

	const serverURL = localStorage.getItem('serverURL');
	const endpoint_id = localStorage.getItem('endpointID');

	try {
		const res = await fetch(`${AUTOPTIC_BASE_URL}/snapshots/delete_snapshot?endpoint_id=${endpoint_id}&pql_id=${pql_id}&format=${format}&timestamp=${timestamp}&snapshot_id=${snapshot_id}&serverURL=${encodeURIComponent(serverURL)}`, {
			method: 'DELETE',
			headers: {
				'Content-Type': 'application/json',
				// Authorization: `Bearer ${token}`
			}
		});

		const response = await res.json();

		if (!res.ok) { 
			throw new Error(response.message || 'Failed to delete the snapshot');
		}

		return response;

	} catch (error) {
		console.error('Error deleting the snapshot:', error.message);
		throw error;
	}

};
