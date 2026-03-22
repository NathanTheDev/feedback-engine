export function Upload({
  label = "File Upload",
  content = "Upload a file...",
}) {
  return (
    <div className="flex flex-col items-center gap-6 pt-16">
      <div className="relative w-full max-w-xl">
        <p className="text-sm font-medium text-neutral-700 mb-2">{label}</p>
        <label className="flex items-center justify-center gap-3 w-full py-3 px-6 rounded-full border border-neutral-200 bg-white shadow-sm text-sm text-neutral-400 cursor-pointer hover:bg-neutral-50 transition-colors">
          <span>{content}</span>
          <input type="file" className="hidden" />
        </label>
      </div>
    </div>
  );
}
