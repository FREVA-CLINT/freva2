import { createSlice } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit";
import { RootState } from "../store";
import TokenService from "./TokenService";
import { TToken } from "./Token";
type UserState = {
  username: string | null;
};
export const userSlice = createSlice({
  name: "user",
  initialState: {
    username: TokenService.getUsername(),
  } as UserState,
  reducers: {
    login(state, action: PayloadAction<{ token: TToken; username: string }>) {
      TokenService.setUser(action.payload.token, action.payload.username);
      state.username = TokenService.getUsername();
    },
    logout(state) {
      TokenService.removeUser();
      state.username = null;
    },
    setUsername(state) {
      state.username = TokenService.getUsername();
    },
  },
});

export const { login, logout, setUsername } = userSlice.actions;
export const selectUsername = (state: RootState) => state.user.username;
export default userSlice.reducer;
