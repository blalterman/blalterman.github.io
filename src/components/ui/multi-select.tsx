'use client'

import * as React from 'react'
import { ChevronsUpDown } from 'lucide-react'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { Checkbox } from '@/components/ui/checkbox'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

interface MultiSelectProps {
  options: string[]
  selected: string[]
  onChange: (selected: string[]) => void
  placeholder?: string
  searchPlaceholder?: string
  className?: string
}

export function MultiSelect({
  options,
  selected,
  onChange,
  placeholder = 'Select items...',
  searchPlaceholder = 'Search...',
  className
}: MultiSelectProps) {
  const [open, setOpen] = React.useState(false)
  const [search, setSearch] = React.useState('')

  // Filter options based on search
  const filtered = React.useMemo(() => {
    if (!search) return options
    return options.filter(option =>
      option.toLowerCase().includes(search.toLowerCase())
    )
  }, [options, search])

  // Toggle selection
  const toggle = (option: string) => {
    if (selected.includes(option)) {
      onChange(selected.filter(s => s !== option))
    } else {
      onChange([...selected, option])
    }
  }

  // Select/clear all
  const selectAll = () => onChange(filtered)
  const clearAll = () => onChange([])

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button
          variant="outline"
          role="combobox"
          aria-expanded={open}
          className={cn("justify-between w-full", className)}
        >
          <span className="truncate">
            {selected.length === 0
              ? placeholder
              : `${selected.length} selected`}
          </span>
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[300px] p-0" align="start">
        <div className="p-2">
          {/* Search input */}
          <Input
            placeholder={searchPlaceholder}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="h-8 text-sm mb-2"
          />

          {/* Select all / Clear buttons */}
          <div className="flex gap-2 mb-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={selectAll}
              className="h-7 text-xs flex-1"
            >
              Select All
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={clearAll}
              className="h-7 text-xs flex-1"
            >
              Clear
            </Button>
          </div>

          {/* Options list */}
          <div className="max-h-[200px] overflow-y-auto">
            {filtered.length === 0 ? (
              <div className="py-6 text-center text-sm text-muted-foreground">
                No results found
              </div>
            ) : (
              <div className="space-y-1">
                {filtered.map(option => (
                  <div
                    key={option}
                    className="flex items-center space-x-2 px-2 py-1.5 hover:bg-accent rounded-sm cursor-pointer"
                    onClick={() => toggle(option)}
                  >
                    <Checkbox
                      checked={selected.includes(option)}
                      onCheckedChange={() => toggle(option)}
                      className="pointer-events-none"
                    />
                    <Label className="flex-1 cursor-pointer text-sm font-normal">
                      {option}
                    </Label>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </PopoverContent>
    </Popover>
  )
}
