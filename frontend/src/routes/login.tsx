import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { signIn, signUp } from "@/lib/auth";
import { Title } from "@/components/ui/Title";
import { useTheme } from "@/context/ThemeContext";
import { ThemeToggle } from "@/components/ui/ThemeToggle";
import { PButton } from "@/components/ui/PButton";

export const Route = createFileRoute("/login")({
  component: LoginComponent,
});

function LoginComponent() {
  const navigate = useNavigate();
  const { theme, toggle } = useTheme();
  const dark = theme === "dark";

  const [isSignUp, setIsSignUp] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (isSignUp && password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }
    try {
      if (isSignUp) {
        await signUp(email, password);
      } else {
        await signIn(email, password);
      }
      navigate({ to: "/" });
    } catch (e) {
      setError(isSignUp ? "Could not create account" : "Invalid email or password");
    }
  };

  const handleToggle = () => {
    setIsSignUp((s) => !s);
    setError("");
    setConfirmPassword("");
  };

  const inputClass = `w-full py-3 px-6 rounded-full border text-sm focus:outline-none transition-colors ${
    dark
      ? "border-[#4A3E30] bg-[#3D3328] text-[#D4C4A8] placeholder:text-[#6B5C4A]"
      : "border-[#C8B89A] bg-[#EDE5DC] text-[#3D2E20] placeholder:text-[#A89880]"
  }`;

  return (
    <div className={`min-h-screen flex flex-col items-center justify-center p-8 transition-colors duration-300 ${dark ? "bg-[#1C1714]" : "bg-[#F5F0EB]"}`}>

      <Title />

      <div className={`w-full max-w-sm rounded-3xl border px-8 py-6 flex flex-col gap-4 mt-4 transition-colors duration-300 ${
        dark ? "bg-[#252019] border-[#2E2820]" : "bg-white border-[#E2D9CE]"
      }`}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className={inputClass}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className={inputClass}
        />
        {isSignUp && (
          <input
            type="password"
            placeholder="Confirm password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className={`${inputClass} ${
              confirmPassword && confirmPassword !== password
                ? "!border-red-500"
                : ""
            }`}
          />
        )}
        {error && <p className="text-red-400 text-sm text-center">{error}</p>}

        <PButton submit={handleSubmit} content={isSignUp ? "Create account" : "Sign in"} />
        
        <p className={`text-center text-sm ${dark ? "text-[#6B5C4A]" : "text-[#A89880]"}`}>
          {isSignUp ? "Already have an account?" : "Don't have an account?"}{" "}
          <button
            onClick={handleToggle}
            className={`transition-colors cursor-pointer ${
              dark ? "text-[#A89880] hover:text-[#D4C4A8]" : "text-[#6B5744] hover:text-[#3D2E20]"
            }`}
          >
            {isSignUp ? "Sign in" : "Sign up"}
          </button>
        </p>
      </div>
    </div>
  );
}