import { PUBLIC_FEEDBACK_BASE_URL } from '$env/static/public';

let feedbackEndpoint: string = '/';
if (PUBLIC_FEEDBACK_BASE_URL) {
	feedbackEndpoint = `${PUBLIC_FEEDBACK_BASE_URL}/feedback`;
}

export const postFeedback = async (comment: string, rating: number) => {
	const response = await fetch(feedbackEndpoint, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			comment,
			rating
		})
	});

	if (!response.ok) {
		throw new Error('Failed to post feedback');
	}

	const data = await response.json();
	return data;
};
