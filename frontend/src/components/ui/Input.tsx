import { useTheme } from "@/context/ThemeContext";

interface InputProps {
  label?: string;
  placeholder?: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

export function Input({ label = "Input", placeholder = "Type here...", value, onChange }: InputProps) {
  const { theme } = useTheme();
  const dark = theme === "dark";

  return (
    <div className="flex flex-col items-center gap-2 pt-8">
      <div className="relative w-full max-w-xl">
        <p className={`text-sm font-bold mb-2 ${dark ? "text-[#A89880]" : "text-[#6B5744]"}`}>
          {label}
        </p>
        <input
          type="text"
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          className={`w-full py-3 px-6 rounded-full border text-sm focus:outline-none focus:ring-1 transition-colors ${
            dark
              ? "border-[#4A3E30] bg-[#3D3328] text-[#D4C4A8] placeholder:text-[#6B5C4A] focus:ring-[#4A3E30] hover:bg-[#45392D]"
              : "border-[#C8B89A] bg-[#EDE5DC] text-[#3D2E20] placeholder:text-[#A89880] focus:ring-[#C8B89A] hover:bg-[#E5D9CC]"
          }`}
        />
      </div>
    </div>
  );
}