import weaviateService from "../weaviate/weaviate.service";
import { createOpenAICompatible } from "@ai-sdk/openai-compatible";

class AssistantService {
	private model: ReturnType<ReturnType<typeof createOpenAICompatible>>;

	constructor() {
		const docker = createOpenAICompatible({
			name: "docker",
			baseURL: process.env.AI_PROVIDER_BASE_URL!,
		});

		this.model = docker("ai/qwen3:latest");
	}

	async getRelativeProducts(query: string) {
		const products = await weaviateService.searchProducts(query);
		return products.map((product) => product.properties["content"]);
	}

	async completeProductQuestion(prompt: string, products: string[]) {
		const response = await this.model.doGenerate({
			prompt: [
				{
					role: "system",
					content: `You are a helpful assistant that can answer questions about food.
            
            Here are related products to the question:
            ${products.join("\n")}
            `,
				},
				{
					role: "user",
					content: [{ type: "text", text: prompt }],
				},
			],
		});

		return response.content;
	}
}

export default new AssistantService();
