import Session from "supertokens-web-js/recipe/session";
import EmailPassword from "supertokens-web-js/recipe/emailpassword";

export async function signIn(email: string, password: string) {
  const response = await EmailPassword.signIn({ formFields: [
    { id: "email", value: email },
    { id: "password", value: password },
  ]});

  console.log("signUp response:", response);
  
  if (response.status !== "OK") throw new Error(response.status);
  return response;
}

export async function signUp(email: string, password: string) {
  const response = await EmailPassword.signUp({ formFields: [
    { id: "email", value: email },
    { id: "password", value: password },
  ]});
  if (response.status !== "OK") throw new Error(response.status);
  return response;
}

export async function signOut() {
  await Session.signOut();
}

export async function isAuthenticated() {
  return await Session.doesSessionExist();
}