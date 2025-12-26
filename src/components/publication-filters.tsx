'use client'

import { useMemo, useState } from 'react'
import type { Publication } from '@/types/publication'
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from '@/components/ui/table'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Popover, PopoverTrigger, PopoverContent } from '@/components/ui/popover'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Label } from '@/components/ui/label'
import { BookOpen, Filter, ChevronDown, X } from 'lucide-react'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip'
import { extractUniqueJournals, extractUniqueYears, isFirstAuthor } from '@/lib/publication-utils'

interface PublicationCategory {
  title: string
  slug: string
  icon: string
  description: string
  publicationType: string | string[]
  showCitations: boolean
}

interface PublicationFiltersProps {
  publications: Publication[]
  categoryData: PublicationCategory
  labels?: {
    journal?: string
  }
}

export function PublicationFilters({
  publications,
  categoryData,
  labels = {},
}: PublicationFiltersProps) {
  // Label customization with fallback
  const journalLabel = labels.journal || 'Journal'

  // Filter state
  const [authorshipFilter, setAuthorshipFilter] = useState<'all' | 'first'>('all')
  const [journalFilter, setJournalFilter] = useState<string>('all')
  const [yearFilter, setYearFilter] = useState<string>('all')
  const [isPopoverOpen, setIsPopoverOpen] = useState(false)

  // Extract unique values for dropdowns
  const uniqueJournals = useMemo(
    () => extractUniqueJournals(publications),
    [publications]
  )

  const uniqueYears = useMemo(
    () => extractUniqueYears(publications),
    [publications]
  )

  // Filter publications based on selected criteria
  const filteredPublications = useMemo(() => {
    return publications.filter(pub => {
      // Authorship filter
      if (authorshipFilter === 'first') {
        if (!isFirstAuthor(pub)) return false
      }

      // Journal filter
      if (journalFilter !== 'all' && pub.journal !== journalFilter) {
        return false
      }

      // Year filter
      if (yearFilter !== 'all' && pub.year.substring(0, 4) !== yearFilter) {
        return false
      }

      return true
    })
  }, [publications, authorshipFilter, journalFilter, yearFilter])

  // Count active filters
  const activeFilterCount = useMemo(() => {
    let count = 0
    if (authorshipFilter !== 'all') count++
    if (journalFilter !== 'all') count++
    if (yearFilter !== 'all') count++
    return count
  }, [authorshipFilter, journalFilter, yearFilter])

  // Reset all filters
  const clearAllFilters = () => {
    setAuthorshipFilter('all')
    setJournalFilter('all')
    setYearFilter('all')
  }

  return (
    <div className="max-w-screen-xl mx-auto mb-8">
      {/* Filter button and result count */}
      <div className="flex items-center justify-between mb-4">
        <Popover open={isPopoverOpen} onOpenChange={setIsPopoverOpen}>
          <PopoverTrigger asChild>
            <Button variant="outline" className="gap-2">
              <Filter className="h-4 w-4" />
              Filter
              {activeFilterCount > 0 && (
                <Badge variant="secondary" className="ml-2">
                  {activeFilterCount}
                </Badge>
              )}
              <ChevronDown className="h-4 w-4 ml-2" />
            </Button>
          </PopoverTrigger>

          <PopoverContent className="w-80" align="start">
            <div className="space-y-4">
              {/* Authorship filter */}
              <div className="space-y-3">
                <Label className="text-sm font-medium">Authorship</Label>
                <RadioGroup value={authorshipFilter} onValueChange={(value: any) => setAuthorshipFilter(value)}>
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="all" id="authorship-all" />
                    <Label htmlFor="authorship-all" className="font-normal cursor-pointer">
                      All publications
                    </Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="first" id="authorship-first" />
                    <Label htmlFor="authorship-first" className="font-normal cursor-pointer">
                      First author only
                    </Label>
                  </div>
                </RadioGroup>
              </div>

              {/* Journal filter */}
              <div className="space-y-2">
                <Label htmlFor="journal-select" className="text-sm font-medium">
                  {journalLabel}
                </Label>
                <Select value={journalFilter} onValueChange={setJournalFilter}>
                  <SelectTrigger id="journal-select">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All {journalLabel}s</SelectItem>
                    {uniqueJournals.map(journal => (
                      <SelectItem key={journal} value={journal}>
                        {journal}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Year filter */}
              <div className="space-y-2">
                <Label htmlFor="year-select" className="text-sm font-medium">
                  Year
                </Label>
                <Select value={yearFilter} onValueChange={setYearFilter}>
                  <SelectTrigger id="year-select">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Years</SelectItem>
                    {uniqueYears.map(year => (
                      <SelectItem key={year} value={year}>
                        {year}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Action buttons */}
              <div className="flex gap-2 pt-2">
                <Button
                  onClick={() => setIsPopoverOpen(false)}
                  className="flex-1"
                >
                  Apply
                </Button>
                {activeFilterCount > 0 && (
                  <Button
                    variant="ghost"
                    onClick={clearAllFilters}
                    className="flex-1"
                  >
                    Clear All
                  </Button>
                )}
              </div>
            </div>
          </PopoverContent>
        </Popover>

        <div className="text-sm text-muted-foreground">
          Showing {filteredPublications.length} of {publications.length} publications
        </div>
      </div>

      {/* Active filter badges */}
      {activeFilterCount > 0 && (
        <div className="flex flex-wrap gap-2 mb-6">
          {authorshipFilter === 'first' && (
            <Badge variant="secondary" className="gap-1">
              First Author
              <X
                className="h-3 w-3 cursor-pointer"
                onClick={() => setAuthorshipFilter('all')}
              />
            </Badge>
          )}
          {journalFilter !== 'all' && (
            <Badge variant="secondary" className="gap-1">
              {journalFilter}
              <X
                className="h-3 w-3 cursor-pointer"
                onClick={() => setJournalFilter('all')}
              />
            </Badge>
          )}
          {yearFilter !== 'all' && (
            <Badge variant="secondary" className="gap-1">
              {yearFilter}
              <X
                className="h-3 w-3 cursor-pointer"
                onClick={() => setYearFilter('all')}
              />
            </Badge>
          )}
        </div>
      )}

      {/* Publications table or empty state */}
      {filteredPublications.length === 0 ? (
        <div className="text-center py-12 text-muted-foreground border rounded-lg overflow-hidden shadow-lg">
          <Filter className="mx-auto h-12 w-12 mb-4 opacity-50" />
          <p className="text-lg font-medium">No publications match these filters</p>
          <Button
            variant="link"
            onClick={clearAllFilters}
            className="mt-2"
          >
            Clear all filters
          </Button>
        </div>
      ) : (
        <div className="border rounded-lg overflow-hidden shadow-lg">
          <Table>
            <TableHeader>
              <TableRow className="bg-muted/50">
                <TableHead className="w-[100px] font-bold">Year</TableHead>
                <TableHead className="font-bold">Title</TableHead>
                <TableHead className="font-bold">Authors</TableHead>
                <TableHead className="font-bold">Journal</TableHead>
                {categoryData.showCitations && (
                  <TableHead className="text-center w-[100px] font-bold">Citations</TableHead>
                )}
                <TableHead className="text-right w-[150px] font-bold">Links</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredPublications.map((pub: Publication, index: number) => (
                <TableRow key={index} className="hover:bg-muted/30">
                  <TableCell className="font-medium">
                    {pub.year.substring(0, 4)}
                  </TableCell>
                  <TableCell>{pub.title}</TableCell>
                  <TableCell>{pub.authors.join(', ')}</TableCell>
                  <TableCell>{pub.journal}</TableCell>
                  {categoryData.showCitations && (
                    <TableCell className="text-center">{pub.citations}</TableCell>
                  )}
                  <TableCell className="text-right space-x-2">
                    {pub.url && (
                      <TooltipProvider>
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <Button variant="outline" size="icon" asChild>
                              <a href={pub.url} target="_blank" rel="noopener noreferrer">
                                <BookOpen className="h-4 w-4" />
                              </a>
                            </Button>
                          </TooltipTrigger>
                          <TooltipContent>
                            <p>Publication</p>
                          </TooltipContent>
                        </Tooltip>
                      </TooltipProvider>
                    )}
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}
    </div>
  )
}
