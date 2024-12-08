<script lang="ts">
	import { toast } from 'svelte-sonner';
	import { onMount, getContext } from 'svelte';

	import { refreshTrigger } from '$lib/stores';

	import { user } from '$lib/stores';

	import {
			updateAutopticEndpoint,
			deleteAutopticEndpoint,
			updateAutopticEnvironment,
			deleteAutopticEnvironment,
			updateServerURL,
			deleteServerURL,
			updateEndpointID,
			deleteEndpointID,
			healthcheckServerURL,
				} from '$lib/apis/autoptic';

	import { copyToClipboard } from '$lib/utils';

	const i18n = getContext('i18n');

	export let admin = false;


	let profileImageUrl = '';
	let name = '';

	let showSaaSConfiguration = false;
	let showNewKeys = false;
	let showServerConfiguration = false;


	let autoptic_endpoint = '';
	let token_id = '';
	let serverURL = '';
	let displayedServerURL = '';
	let endpointID = '';
	let accessToken = '';

	let envFile = null;
	let newEnvFile = false;

	let placeholderText = "Environment file here.";
	const defaultPlaceholderEnv = "Environment file here.";

	let isDisabled = true;

	function handleEnvFileChange(event) {
		
		const fileInput = event.target;
		
		if (fileInput.files.length > 0) {
			envFile = fileInput.files[0]
			const fileName = fileInput.files[0].name;
			placeholderText = fileName;

		} else {
			placeholderText = "Environment file here.";
			}	
		newEnvFile = true;

	}

	const readEnvFile = () => {
		return new Promise((resolve,reject) => {

			const reader = new FileReader();
			reader.onload = function(e) {

				const envFileContent = e.target.result;
				const envFileName = envFile.name;

				try {
					JSON.parse(envFileContent);
					resolve({ envFileContent , envFileName });
				} catch (e) {
					toast.error($i18n.t('Environment file invalid. Your config will not be saved.'));
					placeholderText = defaultPlaceholderEnv
					reject();
				}
			};

			reader.onerror = () => reject();
			reader.readAsText(envFile);

		});
	};

	const saveEnvContent = async() => {
		if (placeholderText != defaultPlaceholderEnv) {
			try {
				const { envFileContent , envFileName } = await readEnvFile();
				await updateAutopticEnvironment(localStorage.token,envFileContent,envFileName)
				localStorage.autoptic_environment = envFileContent
				localStorage.envFileName = envFileName;
			} catch (error){
				toast.error($i18n.t("Environment file invalid. Your config will not be saved."));
            	placeholderText = defaultPlaceholderEnv;
            	return false; 
			}
		} else {
			deleteAutopticEnvironment(localStorage.token)
			localStorage.removeItem('autoptic_environment');
			localStorage.removeItem('envFileName');
		}
		return true;
	};

	const saveAPIURL = async () => {
		if (autoptic_endpoint != ''){
            await updateAutopticEndpoint(localStorage.token,autoptic_endpoint)
		} else {
			await deleteAutopticEndpoint(localStorage.token)
		}
		localStorage.autoptic_endpoint=autoptic_endpoint;
		return true
        };

	function formatServerUrl(url: string) {
		const pattern = /^(https?:\/\/)?(.+?)\/?$/;

		const match = url.match(pattern);
		if (match) {
			const protocol = match[1] ? match[1] : "http://";
			const mainContent = match[2];
			
			return `${protocol}${mainContent}/`;
		}
		return '';
	}

	const saveServerURL = async () => {
		if (serverURL != ''){
			serverURL = formatServerUrl(serverURL)
			try {
				await healthcheckServerURL(localStorage.token,serverURL);
				await updateServerURL(localStorage.token,serverURL)
			} catch {
				toast.error($i18n.t(`Can't connect with the server through the URL ${serverURL}. The config will not be saved.`))
				serverURL = localStorage.serverURL
				return false;
			}
		} else {
			await deleteServerURL(localStorage.token)
		}
		localStorage.serverURL=serverURL;
		return true
        };

	const saveEndpointID = async () => {
		if (endpointID != ''){
			await updateEndpointID(localStorage.token,endpointID)
		} else {
			await deleteEndpointID(localStorage.token)
		}
		localStorage.endpointID=endpointID;
		refreshTrigger.set(true); 
		return true
        };

	async function handleSavingConfig() {
		let urlSaved = true;
		let envSaved = true;

		if (serverURL !== localStorage.serverURL) {
			urlSaved = await saveServerURL();
		}

		if (newEnvFile) {
			envSaved = await saveEnvContent();
			newEnvFile = false;
		}

		if (urlSaved && envSaved) {
			await Promise.all([saveAPIURL(), saveEndpointID()]);
			toast.success($i18n.t('Your configuration has been saved!'));
		}

		isDisabled = !isDisabled;

	}


	onMount(async () => {
		name = $user.name;
		profileImageUrl = $user.profile_image_url;

		const storedEndpoint = localStorage.getItem('autoptic_endpoint');
			if (storedEndpoint) {
				autoptic_endpoint = storedEndpoint;
			}

		const storedEnvName = localStorage.getItem('envFileName');
			if (storedEnvName) {
				placeholderText = storedEnvName;
				}

		const storedServerURL= localStorage.getItem('serverURL');
			if (storedServerURL) {
				serverURL = storedServerURL;
			}

		const storedEndpointID= localStorage.getItem('endpointID');
			if (storedEndpointID) {
				endpointID = storedEndpointID;
			}
	});

    $: isDisabled = !(
        (autoptic_endpoint !== localStorage.autoptic_endpoint) ||
        newEnvFile ||
        (serverURL !== localStorage.serverURL) ||
        (endpointID !== localStorage.endpointID)
    );
	
    $: displayURL = serverURL === '' ? '' : (serverURL + '/');

</script>

<div class="flex flex-col h-full justify-between text-sm">
	<div class=" space-y-3 pr-1.5 overflow-y-scroll max-h-[25rem]">

		<div class="space-y-1">
			<div class="flex space-x-5 mb-4">
				<div class="flex flex-col">
					<div class="self-center mt-2">
						<img
							src={"/autoptic_whitebg.png"}
							alt="autoptic_logo"
							class=" rounded-full dark:bg-white size-16 object-cover"
						/>
					</div>
				</div>
		
				<div class="flex-1 flex flex-col self-center gap-0.5">
					<div class=" mb-0.5  font-medium">{$i18n.t('Autoptic')}</div>
						<div class=" text-xs font-medium ">
							<a
								href="https://www.autoptic.io/"
								class="text-blue-500 hover:underline"
								target="_blank"
								rel="autoptic web"
							>
								Visit the Autoptic's website
							</a>
						</div>
					</div>
				</div>
		</div>

		{#if $user.role === 'admin'}

			<div class="flex justify-between items-center text-sm">
				<div class="  font-medium">{$i18n.t('API Token')}</div>
				<button
					class=" text-xs font-medium text-gray-500"
					type="button"
					on:click={() => {
						showNewKeys = !showNewKeys;
					}}>{showNewKeys ? $i18n.t('Hide') : $i18n.t('Show')}</button
				>
			</div>

			{#if showNewKeys}
				<div class="flex flex-col gap-4">
					<div class="justify-between w-full">
						<div class="flex justify-between w-full">
							<div class="self-center text-xs font-medium">{$i18n.t('API Token')}</div>
						</div>

						<div class="flex mt-2">
							<div class="flex w-full">
								<input
									class="w-full rounded py-1.5 pl-4 text-sm bg-white dark:text-gray-300 dark:bg-gray-850 outline-none"
									placeholder='Enter your API Token'
									bind:value={token_id}
								/>

							</div>

							<button
								class="ml-1.5 px-1.5 py-1 dark:hover:bg-gray-850 transition rounded-lg"
								on:click={() => {
									if (token_id != '') {
										token_id=''
									toast.success($i18n.t('Token deleted. Please save your config!'));
									}
								}}
								>
								<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3" viewBox="0 0 16 16">
									<path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5M11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47M8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5"/>
								</svg>
							</button>
						</div>
					</div>
				</div>
			{/if}

			<hr class=" dark:border-gray-850 my-4" />
		{/if}
		
		<div class="flex justify-between items-center text-sm">
			<div class="  font-medium">{$i18n.t('SaaS Configuration')}</div>
			<button
				class=" text-xs font-medium text-gray-500"
				type="button"
				on:click={() => {
					showSaaSConfiguration = !showSaaSConfiguration;
				}}>{showSaaSConfiguration ? $i18n.t('Hide') : $i18n.t('Show')}</button
			>
		</div>

		{#if showSaaSConfiguration}
			<div class="flex flex-col gap-4">
				<div class="justify-between w-full">
					<div class="flex justify-between w-full">
						<div class="self-center text-xs font-medium">{$i18n.t('API URL')}</div>
					</div>

					<div class="flex mt-2">
						<div class="flex w-full">
							<input
								class="w-full rounded py-1.5 pl-4 text-sm bg-white dark:text-gray-300 dark:bg-gray-850 outline-none"
								placeholder='Enter your API URL'
								bind:value={autoptic_endpoint}
							/>

						</div>

						<button
							class="ml-1.5 px-1.5 py-1 dark:hover:bg-gray-850 transition rounded-lg"
							on:click={() => {
								if (autoptic_endpoint != '') {
								autoptic_endpoint=''
								toast.success($i18n.t('API URL deleted. Please save your config!'));
								}
							}}
							>
							<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3" viewBox="0 0 16 16">
								<path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5M11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47M8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5"/>
							</svg>
						</button>
					</div>
				</div>
				<div class="flex flex-col gap-4">
					<div class="justify-between w-full">
						<div class="flex justify-between w-full">
							<div class="self-center text-xs font-medium">{$i18n.t('Environment JSON file')}</div>
						</div>
	
						<div class="flex mt-2">
							<div class="flex w-full">
								<input
								type="file"
								accept=".JSON"
								class="hidden"
								id="file-upload"
								name="myfile"
								on:change={handleEnvFileChange}
							/>
								<label
									for="file-upload"
									class="w-full rounded py-1.5 pl-4 text-sm bg-white dark:text-gray-300 dark:bg-gray-850 cursor-pointer"
								>
									<span>{placeholderText}</span>
								</label>
							</div>
	
							<button
								class="ml-1.5 px-1.5 py-1 dark:hover:bg-gray-850 transition rounded-lg"
								on:click={() => {
								if (placeholderText != defaultPlaceholderEnv) {
									placeholderText='Environment file here.'
									newEnvFile= true
									toast.success($i18n.t('Environment file deleted. Please save your configuration!'));	
									}
								}}>
								<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3" viewBox="0 0 16 16">
									<path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5M11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47M8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5"/>
								</svg>
							</button>
						</div>
					</div>
					
				</div>
			</div>
		{/if}

		<hr class=" dark:border-gray-850 my-4" />
	
		<div class="flex justify-between items-center text-sm">
			<div class="  font-medium">{$i18n.t('Server Configuration')}</div>
			<button
				class=" text-xs font-medium text-gray-500"
				type="button"
				on:click={() => {
					showServerConfiguration = !showServerConfiguration;
				}}>{showServerConfiguration ? $i18n.t('Hide') : $i18n.t('Show')}</button
			>
		</div>

		{#if showServerConfiguration}
			<div class="flex flex-col gap-4">
				<div class="justify-between w-full">
					<div class="flex justify-between w-full">
						<div class="self-center text-xs font-medium">{$i18n.t('Server URL')}</div>
					</div>

					<div class="flex mt-2">
						<div class="flex w-full">
							<input
								class="w-full rounded py-1.5 pl-4 text-sm bg-white dark:text-gray-300 dark:bg-gray-850 outline-none"
								placeholder='Enter the Server URL'
								bind:value = {serverURL}
							/>

						</div>

						<button
							class="ml-1.5 px-1.5 py-1 dark:hover:bg-gray-850 transition rounded-lg"
							on:click={() => {
								if (serverURL != '') {
									serverURL=''
									toast.success($i18n.t('Server URL deleted. Please save your configuration!'));
									}
								}}
							>
							<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3" viewBox="0 0 16 16">
								<path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5M11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47M8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5"/>
							</svg>
						</button>
					</div>
				</div>

			</div>

			<div class="flex flex-col gap-4">
				<div class="justify-between w-full">
					<div class="flex justify-between w-full">
						<div class="self-center text-xs font-medium">{$i18n.t('Endpoint ID')}</div>
					</div>

					<div class="flex mt-2">
						<div class="flex w-full">
							<input
								class="w-full rounded py-1.5 pl-4 text-sm bg-white dark:text-gray-300 dark:bg-gray-850 outline-none"
								placeholder='Enter your Endpoint ID.'
								bind:value={endpointID}
							/>

						</div>

						<button
							class="ml-1.5 px-1.5 py-1 dark:hover:bg-gray-850 transition rounded-lg"
							on:click={() => {
								if (endpointID != '') {
									endpointID=''
									toast.success($i18n.t('Endpoint ID deleted. Please save your configuration!'));
									}
								}}
							>
							<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3" viewBox="0 0 16 16">
								<path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5M11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47M8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5"/>
							</svg>
						</button>
					</div>
				</div>
			</div>


			<div class="flex flex-col gap-4">
				<div class="justify-between w-full">
					<div class="flex justify-between w-full">
						<div class="self-center text-xs font-medium">{$i18n.t('Access Token')}</div>
					</div>

					<div class="flex mt-2">
						<div class="flex w-full">
							<input
								class="w-full rounded py-1.5 pl-4 text-sm bg-white dark:text-gray-300 dark:bg-gray-850 outline-none"
								placeholder='Enter your Access Token... Soon!'
								bind:value={accessToken}
								disabled={true}
							/>

						</div>

						<button
							class="ml-1.5 px-1.5 py-1 dark:hover:bg-gray-850 transition rounded-lg"
							on:click={() => {
								if (accessToken != '') {
									accessToken=''
									toast.success($i18n.t('Access Token deleted. Please save your configuration!'));
									}
								}}
							>
							<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash3" viewBox="0 0 16 16">
								<path d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5M11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47M8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5"/>
							</svg>
						</button>
					</div>
				</div>
			</div>

		{/if}

	</div>

	<div class="flex justify-end pt-3 text-sm font-medium">
		<button
			class=" {isDisabled ? 'bg-emerald-950' : 'bg-emerald-700 hover:bg-emerald-800'} px-4 py-2  text-gray-100 transition rounded-lg"
			disabled={isDisabled}
			on:click={handleSavingConfig}
		>
			{$i18n.t('Save')}
		</button>
	</div>

</div>
