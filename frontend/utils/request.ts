import axios, { AxiosError } from "axios";
import { TToken } from "./auth/Token";
import TokenService from "./auth/TokenService";

const instance = axios.create({
  headers: {
    "Content-Type": "application/json",
  },
});

instance.interceptors.request.use(
  (config) => {
    if (!config.headers) {
      config.headers = {};
    }
    const token = TokenService.getLocalAccessToken();

    if (token) {
      config.headers.Authorization = "Bearer " + token;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

instance.interceptors.response.use(
  (res) => {
    return res;
  },
  async (err: AxiosError) => {
    const originalConfig = err.config as AxiosError & {
      _retry?: boolean;
      url: string;
    };
    if (
      originalConfig &&
      originalConfig.url !== "/api/token/" &&
      err.response
    ) {
      // Access Token was expired
      if (err.response.status === 401 && !originalConfig._retry) {
        originalConfig._retry = true;

        try {
          const rs = await instance.post("/api/token/refresh/", {
            refresh: TokenService.getLocalRefreshToken(),
          });

          const { access } = rs.data as TToken;
          TokenService.updateLocalAccessToken(access);

          return instance(originalConfig);
        } catch (_error) {
          return Promise.reject(_error);
        }
      }
    }

    return Promise.reject(err);
  }
);

export default instance;
