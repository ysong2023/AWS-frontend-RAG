"use client";

import { Configuration, DefaultApi } from "@/api-client";

export function getApiUrl() {
  // return process.env.NEXT_PUBLIC_API_BASE_URL || "http://0.0.0.0:8000";
  return process.env.NEXT_PUBLIC_API_BASE_URL || "https://nlnpntcdzj4vuychrfxrjojqsm0ewwkg.lambda-url.us-east-1.on.aws";
}

export default function createApiClient() {
  const apiConfig = new Configuration({
    basePath: getApiUrl(),
  });
  const api = new DefaultApi(apiConfig);
  return api;
}
