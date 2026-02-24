import { Context, Hono } from "hono";
import assistantService from "./assistant.service";

class AssistantController {
	private assistantHono = new Hono();

	constructor() {
		this.assistantHono.post("/complete", this.complete);
	}

	getHono() {
		return this.assistantHono;
	}

	async complete(c: Context) {
		const { query } = await c.req.json();

		if (!query) {
			return c.json({ error: "query is required" }, 400);
		}

		const products = await assistantService.getRelativeProducts(query);

		const response = await assistantService.completeProductQuestion(
			query,
			products as string[],
		);

		return c.json({ response });
	}
}

export default new AssistantController().getHono();
