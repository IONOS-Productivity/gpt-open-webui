export const readFile = async (file: File): Promise<string> => {
	return new Promise((resolve) => {
		const reader = new FileReader();

		reader.onload = (event) => {
			resolve(event.target.result);
		};

		reader.readAsText(file);
	});
};
