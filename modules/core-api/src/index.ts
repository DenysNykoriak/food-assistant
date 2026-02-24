import { Hono } from "hono";
import assistantController from "./modules/assistant/assistant.controller";
import * as dotenv from "dotenv";

dotenv.config();

const app = new Hono();

app.route("/assistant", assistantController);

export default app;
