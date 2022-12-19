import { TToken } from "./Token";

class TokenService {
  getLocalRefreshToken() {
    const user = this.getUser();
    if (user) {
      return user.refresh;
    }
    return null;
  }

  getLocalAccessToken() {
    const user = this.getUser();
    if (user) {
      return user.access;
    }
    return null;
  }

  updateLocalAccessToken(token: string) {
    const user = this.getUser();
    if (user) {
      user.access = token;
      localStorage.setItem("user", JSON.stringify(token));
    }
  }

  getUser() {
    const userToken = localStorage.getItem("user");
    if (userToken) {
      return JSON.parse(userToken) as TToken;
    }
    return null;
  }

  getUsername() {
    return localStorage.getItem("username");
  }

  setUser(token: TToken, username: string) {
    localStorage.setItem("user", JSON.stringify(token));
    localStorage.setItem("username", username);
  }

  removeUser() {
    localStorage.removeItem("user");
    localStorage.removeItem("username");
  }
}

export default new TokenService();
