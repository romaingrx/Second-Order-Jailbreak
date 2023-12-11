"use client";

import { NextUIProvider } from "@nextui-org/react";
import { ThemeProvider } from "next-themes";

export default function ClientProvider({ children }) {
  return (
    <ThemeProvider enableSystem={true} attribute="class">
      <NextUIProvider>{children}</NextUIProvider>
    </ThemeProvider>
  );
}
