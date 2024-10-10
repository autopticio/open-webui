<script lang="ts">
	import { toast } from 'svelte-sonner';
	import { onMount, getContext } from 'svelte';

	import { user } from '$lib/stores';
	import { updateUserProfile,
			 createAPIKey,
			 getAPIKey,
				} from '$lib/apis/auths';

	import {
			updateAutopticEndpoint,
			 deleteAutopticEndpoint,
			 updateAutopticEnvironment,
			 deleteAutopticEnvironment,
				} from '$lib/apis/autoptic';

	import { generateInitialsImage, canvasPixelTest } from '$lib/utils';
	import { copyToClipboard } from '$lib/utils';

	const i18n = getContext('i18n');

	export let saveHandler: Function;
	export let admin = false;


	let profileImageUrl = '';
	let name = '';

	let showAPIKeys = false;
	
	let showAutopticKeys = false;
	let showNewKeys = false;


	let autoptic_endpoint = '';
	let token_id = '';

	let APIKey = '';

	let envFile = null;
	let newEnvFile= false;

	let placeholderText = "Environment file here.";

	function handleEnvFileChange(event) {
		
		const fileInput = event.target;
		
		if (fileInput.files.length > 0) {
			envFile = fileInput.files[0]
			const fileName = fileInput.files[0].name;
			placeholderText = fileName; 
		} else {
			placeholderText = 'Envinroment file here';
			}	
		newEnvFile=true;
	}

	const saveEnvContent = async() => {
		// JERE: I will improve this if.
		if (placeholderText != "Environment file here.") {
			const reader = new FileReader();

			const readEnvFile = () => {
				return new Promise((resolve,reject) => {
					reader.onload = function(e) {
						const envFileContent = e.target.result;
						const envFileName = envFile.name;
						try {
							JSON.parse(envFileContent)
							resolve({ envFileContent , envFileName })
						} catch (e) {
							toast.error($i18n.t('Environment file invalid. Your config will not be saved.'));
							placeholderText = "Environment file here."
							reject();
						}
					};

					reader.onerror = () => reject();
					reader.readAsText(envFile);

				});
			};

			const { envFileContent , envFileName } = await readEnvFile();
			updateAutopticEnvironment(localStorage.token,envFileContent,envFileName)
			localStorage.autoptic_environment = envFileContent
			localStorage.envFileName = envFileName;
			toast.success($i18n.t('Environment configuration saved!'));

		} else {
			deleteAutopticEnvironment(localStorage.token)
			localStorage.removeItem('autoptic_environment');
			localStorage.removeItem('envFileName');
			toast.success($i18n.t('Environment configuration deleted!'));
		}
	};

	const saveEndpoint = async () => {
		if (autoptic_endpoint != ''){
            await updateAutopticEndpoint(localStorage.token,autoptic_endpoint)
		} else {
			await deleteAutopticEndpoint(localStorage.token)
		}
		localStorage.autoptic_endpoint=autoptic_endpoint;
		toast.success($i18n.t('Autoptic endpoint saved!'));
        };

	const submitHandler = async () => {
		if (name !== $user.name) {
			if (profileImageUrl === generateInitialsImage($user.name) || profileImageUrl === '') {
				profileImageUrl = generateInitialsImage(name);
			}
		}

		const updatedUser = await updateUserProfile(localStorage.token, name, profileImageUrl).catch(
			(error) => {
				toast.error(error);
			}
		);

		if (updatedUser) {
			await user.set(updatedUser);
			return true;
		}
		return false;
	};

	onMount(async () => {
		name = $user.name;
		profileImageUrl = $user.profile_image_url;

		APIKey = await getAPIKey(localStorage.token).catch((error) => {
			console.log(error);
			return '';
		});

		const storedEndpoint = localStorage.getItem('autoptic_endpoint');
			if (storedEndpoint) {
				autoptic_endpoint = storedEndpoint;
			}

		const storedEnvName = localStorage.getItem('envFileName');
			if (storedEnvName) {
				placeholderText = storedEnvName;
				}

	});
</script>

<div class="flex flex-col h-full justify-between text-sm">
	<div class=" space-y-3 pr-1.5 overflow-y-scroll max-h-[25rem]">

		<div class="space-y-1">
			<div class="flex space-x-5 mb-4">
				<div class="flex flex-col">
					<div class="self-center mt-2">
						<img
							src={"/autoptic.png"}
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
									toast.success($i18n.t('Token saved. Please save your config!'));
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
			<div class="  font-medium">{$i18n.t('API keys')}</div>
			<button
				class=" text-xs font-medium text-gray-500"
				type="button"
				on:click={() => {
					showAutopticKeys = !showAutopticKeys;
				}}>{showAutopticKeys ? $i18n.t('Hide') : $i18n.t('Show')}</button
			>
		</div>

		{#if showAutopticKeys}
			<div class="flex flex-col gap-4">
				<div class="justify-between w-full">
					<div class="flex justify-between w-full">
						<div class="self-center text-xs font-medium">{$i18n.t('API endpoint')}</div>
					</div>

					<div class="flex mt-2">
						<div class="flex w-full">
							<input
								class="w-full rounded py-1.5 pl-4 text-sm bg-white dark:text-gray-300 dark:bg-gray-850 outline-none"
								placeholder='Enter your Endpoint'
								bind:value={autoptic_endpoint}
							/>

						</div>

						<button
							class="ml-1.5 px-1.5 py-1 dark:hover:bg-gray-850 transition rounded-lg"
							on:click={() => {
								if (autoptic_endpoint != '') {
								autoptic_endpoint=''
								toast.success($i18n.t('API endpoint deleted. Please save your config!'));
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
								on:change="{handleEnvFileChange}"
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
								if (placeholderText != "Environment file here.") {
									placeholderText='Environment file here.'
									newEnvFile= true
									toast.success($i18n.t('Environment file deleted. Please save your config!'));	
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

	</div>

	<div class="flex justify-end pt-3 text-sm font-medium">
		<button
			class="  px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-gray-100 transition rounded-lg"
			on:click={async () => {
				if (autoptic_endpoint != localStorage.autoptic_endpoint) {
					saveEndpoint();
				}
				if (newEnvFile){
					saveEnvContent();
				}
				const res = await submitHandler();
				if (res) {
					saveHandler();
				}
			}}
		>
			{$i18n.t('Save')}
		</button>
	</div>

</div>
