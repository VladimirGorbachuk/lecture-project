export type UserName = string;
export type Email = string;
export type Password = string;
export type Contact = string;
export type ContactsList = Contact[];
export type UniqueId = string;


export type UserAuth = {
    login: UserName;
    password: Password;
    password2: Password;
    email: Email;
}


export type User = {
    isAuthenticated: boolean;
    id: UniqueId | undefined;
    login: UserName | undefined;
    email: Email | undefined;
    cv: UniqueId | undefined;
    contacts: ContactsList | undefined;
}

export const UserNonAuthenticated: User = {
   isAuthenticated: false,
   id: undefined,
   login: undefined,
   email: undefined,
   cv: undefined,
   contacts: undefined,
}