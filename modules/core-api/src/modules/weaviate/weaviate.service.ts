import weaviate, { WeaviateClient } from "weaviate-client";

class WeaviateService {
	private client: WeaviateClient | null = null;

	constructor() {
		console.log(
			process.env.WEAVIATE_HOST,
			process.env.WEAVIATE_PORT,
			process.env.WEAVIATE_SECURE,
			process.env.WEAVIATE_GRPC_HOST,
			process.env.WEAVIATE_GRPC_PORT,
			process.env.WEAVIATE_GRPC_SECURE,
		);

		weaviate
			.connectToCustom({
				httpHost: process.env.WEAVIATE_HOST!,
				httpPort: parseInt(process.env.WEAVIATE_PORT!),
				httpSecure: process.env.WEAVIATE_SECURE === "true",
				grpcHost: process.env.WEAVIATE_GRPC_HOST!,
				grpcPort: parseInt(process.env.WEAVIATE_GRPC_PORT!),
				grpcSecure: process.env.WEAVIATE_GRPC_SECURE === "true",
			})
			.then((client) => {
				this.client = client;
			})
			.catch((error) => {
				console.error(error);
			});
	}

	async searchProducts(query: string) {
		if (!this.client) {
			throw new Error("Weaviate client not initialized");
		}

		const productCollection = this.client.collections.use("Product");

		const result = await productCollection.query.nearText(query, {
			limit: 1,
			certainty: 0.5,
		});

		return result.objects;
	}
}

export default new WeaviateService();
