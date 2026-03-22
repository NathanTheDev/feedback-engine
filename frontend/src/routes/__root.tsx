import * as React from "react";
import { Link, Outlet, createRootRoute } from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/router-devtools";
import Session from "supertokens-web-js";
import { ThemeToggle } from "@/components/ui/ThemeToggle";
import { useTheme } from "@/context/ThemeContext";

export const Route = createRootRoute({
  component: RootComponent,
});

function RootComponent() {
  const { theme, toggle } = useTheme();
  const dark = theme === "dark";

  return (
    <div className="flex min-h-screen w-full bg-[#EDD9B0]">
      <main className="flex-1 relative">
        <ThemeToggle />
        <Outlet />
      </main>
      <TanStackRouterDevtools position="bottom-right" />
    </div>
  );
}
