import { toast } from "@zerodevx/svelte-toast";

export function showMessage(type = "SUCCESS", message) {
	switch (type.toUpperCase()) {
		case "SUCCESS":
			toast.push(message, {
				theme: {
					"--toastBackground": "#48BB78",
					"--toastProgressBackground": "#2F855A",
				},
			});
			break;
		case "WARNING":
			toast.push(message, {
				theme: {
					"--toastBackground": "#ECC94B",
					"--toastProgressBackground": "#B7791F",
				},
			});
			break;
		case "ERROR":
			toast.push(message, {
				theme: {
					"--toastBackground": "#F56565",
					"--toastProgressBackground": "#C53030",
				},
			});
			break;
	}
}
