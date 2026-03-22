import { useTheme } from "@/context/ThemeContext";

export function ThemeToggle() {
  const { theme, toggle } = useTheme();
  const dark = theme === "dark";
  return (
    <div className="absolute top-6 right-8">
      <button
        onClick={toggle}
        role="switch"
        aria-checked={!dark}
        className={`relative inline-flex items-center w-14 h-7 rounded-full border transition-colors duration-100 focus:outline-none ${
          dark
            ? "bg-[#3D3328] border-[#4A3E30]"
            : "bg-[#EDE5DC] border-[#C8B89A]"
        } hover: cursor-pointer`}
      >
        <span
          className={`absolute left-1 w-5 h-5 rounded-full shadow transition-transform duration-300 flex items-center justify-center text-xs ${
            dark ? "translate-x-0 bg-[#A89880]" : "translate-x-7 bg-[#6B5744]"
          }`}
        >
          {dark ? "🌙" : "☀️"}
        </span>
      </button>
    </div>
  );
}
