import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { Upload } from "@/components/ui/Upload";
import { Title } from "@/components/ui/Title";
import { ThemeToggle } from "@/components/ui/ThemeToggle";
import { useTheme } from "@/context/ThemeContext";
import { PButton } from "@/components/ui/PButton";

export const Route = createFileRoute("/trained/$userId")({
  component: TrainedComponent,
});

function TrainedComponent() {
  const { userId } = Route.useParams();
  const navigate = useNavigate();
  const { theme } = useTheme();
  const dark = theme === "dark";

  const [file, setFile] = useState<File[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async () => {
    if (file.length === 0) {
      setError("Please upload an essay before submitting.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const formData = new FormData();
      formData.append("file", file[0]);
      const response = await fetch("http://localhost:8080/check", {
        method: "POST",
        body: formData,
      });
      if (!response.ok) throw new Error("Upload failed");
      const data = await response.json();
      const { annotations, content } = data;
      navigate({
        to: "/feedback",
        search: { annotations, userId, content },
      });
    } catch (e) {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`min-h-screen flex flex-col items-center p-8 transition-colors duration-300 ${dark ? "bg-[#1C1714]" : "bg-[#F5F0EB]"}`}>
      <ThemeToggle />
      <Title />
      <div className={`w-full max-w-xl rounded-3xl shadow-sm border px-8 py-6 mt-4 transition-colors duration-300 ${
        dark ? "bg-[#252019] border-[#2E2820]" : "bg-white border-[#E2D9CE]"
      }`}>
        <Upload
          label="Upload your essay for feedback"
          content="Upload a .docx file..."
          files={file}
          onFilesChange={setFile}
        />
        {error && (
          <p className="text-red-400 text-sm text-center mt-4">{error}</p>
        )}
        <div className="flex justify-center mt-6">
          <PButton submit={handleSubmit} content={loading ? "Uploading..." : "Get Feedback"} />
        </div>
      </div>
    </div>
  );
}