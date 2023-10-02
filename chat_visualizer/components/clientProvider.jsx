"use client"

import { NextUIProvider } from "@nextui-org/react"

export default function ClientProvider({ children }) {
  return (
    <NextUIProvider>
        {children}
    </NextUIProvider>
  )
}
