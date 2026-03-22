import { useTheme } from "@/context/ThemeContext";

interface UploadProps {
  label?: string;
  content?: string;
  multiple?: boolean;
  files: File[];
  onFilesChange: (files: File[]) => void;
}

export function Upload({
  label = "File Upload",
  content = "Upload a file...",
  multiple = false,
  files,
  onFilesChange,
}: UploadProps) {
  const { theme } = useTheme();
  const dark = theme === "dark";

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onFilesChange(Array.from(e.target.files ?? []));
  };

  return (
    <div className="flex flex-col items-center gap-2 pt-8">
      <div className="relative w-full max-w-xl">
        <p className={`text-sm font-bold mb-2 ${dark ? "text-[#A89880]" : "text-[#6B5744]"}`}>
          {label}
        </p>
        <label className={`flex items-center justify-center gap-3 w-full py-3 px-6 rounded-full border text-sm cursor-pointer transition-colors ${
          dark
            ? "border-[#4A3E30] bg-[#3D3328] text-[#A89880] hover:bg-[#45392D]"
            : "border-[#C8B89A] bg-[#EDE5DC] text-[#6B5744] hover:bg-[#E5D9CC]"
        }`}>
          <span>
            {files.length === 0
              ? content
              : files.length === 1
                ? files[0].name
                : `${files.length} files selected`}
          </span>
          <input
            type="file"
            accept=".docx"
            multiple={multiple}
            onChange={handleChange}
            className="hidden"
          />
        </label>
      </div>
    </div>
  );
}