"use client"

import { useEffect, useState } from "react"
import { Moon, Sun, Monitor } from "lucide-react"
import { useTheme } from "next-themes"
import { Button } from "@/components/ui/button"

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return <Button variant="ghost" size="icon" aria-label="Toggle theme"><Sun className="h-5 w-5" /></Button>
  }

  const cycleTheme = () => {
    if (theme === "light") setTheme("dark")
    else if (theme === "dark") setTheme("system")
    else setTheme("light")
  }

  const icon = theme === "dark"
    ? <Moon className="h-5 w-5" />
    : theme === "light"
      ? <Sun className="h-5 w-5" />
      : <Monitor className="h-5 w-5" />

  const label = theme === "dark"
    ? "Switch to system theme"
    : theme === "light"
      ? "Switch to dark theme"
      : "Switch to light theme"

  return (
    <Button variant="ghost" size="icon" onClick={cycleTheme} aria-label={label}>
      {icon}
    </Button>
  )
}
