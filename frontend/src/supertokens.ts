import SuperTokens from "supertokens-web-js";
import Session from "supertokens-web-js/recipe/session";
import EmailPassword from "supertokens-web-js/recipe/emailpassword";

SuperTokens.init({
  appInfo: {
    appName: "red.ink",
    apiDomain: "http://localhost:3000",
    apiBasePath: "/auth",
  },
  recipeList: [
    Session.init(),
    EmailPassword.init(),
  ],
});