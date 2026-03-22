import logo from "@assets/pen-icon.png";

export function Title() {
  return (
    <div className="flex items-center gap-4">
      <img src={logo} alt="Red.ink logo" className="w-11 h-10" />
      <h1 className="text-4xl font-bold tracking-tight text-red-500">
        red.ink
      </h1>
    </div>
  );
}
