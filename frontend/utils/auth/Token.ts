export type TToken = {
  refresh: string;
  access: string;
};

export type TDecodedToken = {
  name: string;
  // It has more information that the name,
  // but the name is the only thing we need right now
};
