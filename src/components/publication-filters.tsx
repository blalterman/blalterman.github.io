'use client'

import React, { useMemo, useState } from 'react'
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
import { Checkbox } from '@/components/ui/checkbox'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Label } from '@/components/ui/label'
import { MultiSelect } from '@/components/ui/multi-select'
import { BookOpen, Filter, ChevronDown, X } from 'lucide-react'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip'
import { extractUniqueJournals, extractUniqueYears, isFirstAuthor, formatAuthorNames, isAlterman, decodeHtmlEntities } from '@/lib/publication-utils'

interface PublicationCategory {
  title: string
  slug: string
  icon: string
  description: string
  publicationType: string | string[]
  showCitations: boolean
  showFilters?: boolean
  showJournal?: boolean          // Default: true. Set false to hide column
  journalLabel?: string           // Default: 'Journal'. Custom header label
  journalField?: string           // Default: 'journal'. Which field to display
  showLinks?: boolean             // Default: true. Set false to hide Links column
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
  const journalLabel = labels.journal || categoryData.journalLabel || 'Journal'

  // Determine which field to display in Journal column
  const journalFieldName = categoryData.journalField || 'journal'
  const getJournalValue = (pub: Publication): string => {
    if (journalFieldName === 'location') {
      return pub.location || pub.booktitle || '—'
    }
    return pub.journal || '—'
  }

  // Filter state
  const [authorshipFilter, setAuthorshipFilter] = useState<'all' | 'first' | 'coauthor'>('all')
  const [invitedFilter, setInvitedFilter] = useState<'all' | 'invited' | 'contributed'>('all')
  const [journalFilters, setJournalFilters] = useState<string[]>([])
  const [yearFilters, setYearFilters] = useState<string[]>([])
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
      } else if (authorshipFilter === 'coauthor') {
        if (isFirstAuthor(pub)) return false
      }

      // Journal filter - OR logic (match any selected)
      if (journalFilters.length > 0 && !journalFilters.includes(pub.journal)) {
        return false
      }

      // Year filter - OR logic (match any selected)
      const pubYear = pub.year.substring(0, 4)
      if (yearFilters.length > 0 && !yearFilters.includes(pubYear)) {
        return false
      }

      // Invited filter (only for conferences)
      if (categoryData.slug === 'conferences' && invitedFilter !== 'all') {
        if (invitedFilter === 'invited' && !pub.invited) return false
        if (invitedFilter === 'contributed' && pub.invited) return false
      }

      return true
    })
  }, [publications, authorshipFilter, invitedFilter, journalFilters, yearFilters, categoryData.slug])

  // Count active filters
  const activeFilterCount = useMemo(() => {
    let count = 0
    if (authorshipFilter !== 'all') count++
    if (categoryData.slug === 'conferences' && invitedFilter !== 'all') count++
    count += journalFilters.length
    count += yearFilters.length
    return count
  }, [authorshipFilter, invitedFilter, journalFilters, yearFilters, categoryData.slug])

  // Reset all filters
  const clearAllFilters = () => {
    setAuthorshipFilter('all')
    setInvitedFilter('all')
    setJournalFilters([])
    setYearFilters([])
  }

  return (
    <div className="max-w-screen-xl mx-auto mb-8">
      {/* Only show filters if enabled */}
      {categoryData.showFilters !== false && (
        <>
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
                      First author
                    </Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <RadioGroupItem value="coauthor" id="authorship-coauthor" />
                    <Label htmlFor="authorship-coauthor" className="font-normal cursor-pointer">
                      Co-author
                    </Label>
                  </div>
                </RadioGroup>
              </div>

              {/* Invited filter (conferences only) */}
              {categoryData.slug === 'conferences' && (
                <div className="space-y-3">
                  <Label className="text-sm font-medium">Type</Label>
                  <RadioGroup value={invitedFilter} onValueChange={(value: any) => setInvitedFilter(value)}>
                    <div className="flex items-center space-x-2">
                      <RadioGroupItem value="all" id="invited-all" />
                      <Label htmlFor="invited-all" className="font-normal cursor-pointer">
                        All conferences
                      </Label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <RadioGroupItem value="invited" id="invited-invited" />
                      <Label htmlFor="invited-invited" className="font-normal cursor-pointer">
                        Invited talks only
                      </Label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <RadioGroupItem value="contributed" id="invited-contributed" />
                      <Label htmlFor="invited-contributed" className="font-normal cursor-pointer">
                        Contributed only
                      </Label>
                    </div>
                  </RadioGroup>
                </div>
              )}

              {/* Journal filter */}
              <div className="space-y-2">
                <Label className="text-sm font-medium">{journalLabel}</Label>
                <MultiSelect
                  options={uniqueJournals}
                  selected={journalFilters}
                  onChange={setJournalFilters}
                  placeholder={`All ${journalLabel}s`}
                  searchPlaceholder={`Search ${journalLabel.toLowerCase()}s...`}
                />
              </div>

              {/* Year filter */}
              <div className="space-y-2">
                <Label className="text-sm font-medium">Year</Label>
                <MultiSelect
                  options={uniqueYears}
                  selected={yearFilters}
                  onChange={setYearFilters}
                  placeholder="All Years"
                  searchPlaceholder="Search years..."
                />
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
          {authorshipFilter === 'coauthor' && (
            <Badge variant="secondary" className="gap-1">
              Co-Author
              <X
                className="h-3 w-3 cursor-pointer"
                onClick={() => setAuthorshipFilter('all')}
              />
            </Badge>
          )}
          {categoryData.slug === 'conferences' && invitedFilter === 'invited' && (
            <Badge variant="secondary" className="gap-1">
              Invited Talks Only
              <X
                className="h-3 w-3 cursor-pointer"
                onClick={() => setInvitedFilter('all')}
              />
            </Badge>
          )}
          {categoryData.slug === 'conferences' && invitedFilter === 'contributed' && (
            <Badge variant="secondary" className="gap-1">
              Contributed Only
              <X
                className="h-3 w-3 cursor-pointer"
                onClick={() => setInvitedFilter('all')}
              />
            </Badge>
          )}
          {journalFilters.map(journal => (
            <Badge key={`journal-${journal}`} variant="secondary" className="gap-1 max-w-full">
              <span className="truncate">{journal}</span>
              <X
                className="h-3 w-3 cursor-pointer shrink-0"
                onClick={() => setJournalFilters(journalFilters.filter(j => j !== journal))}
              />
            </Badge>
          ))}
          {yearFilters.map(year => (
            <Badge key={`year-${year}`} variant="secondary" className="gap-1">
              <span className="truncate">{year}</span>
              <X
                className="h-3 w-3 cursor-pointer shrink-0"
                onClick={() => setYearFilters(yearFilters.filter(y => y !== year))}
              />
            </Badge>
          ))}
        </div>
      )}
      </>
    )}

      {/* Show publication count when filters are disabled */}
      {categoryData.showFilters === false && (
        <div className="text-sm text-muted-foreground mb-4">
          Showing {publications.length} publication{publications.length !== 1 ? 's' : ''}
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
                {categoryData.slug !== 'invited-talks' && categoryData.slug !== 'phd-thesis' && (
                  <TableHead className="font-bold">Authors</TableHead>
                )}
                {(categoryData.showJournal !== false) && (
                  <TableHead className="font-bold">{journalLabel}</TableHead>
                )}
                {categoryData.showCitations && (
                  <TableHead className="text-center w-[100px] font-bold">Citations</TableHead>
                )}
                {(categoryData.showLinks !== false) && (
                  <TableHead className="text-right w-[150px] font-bold">Links</TableHead>
                )}
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredPublications.map((pub: Publication, index: number) => (
                <TableRow key={index} className="hover:bg-muted/30">
                  <TableCell className="font-medium">
                    {pub.year.substring(0, 4)}
                  </TableCell>
                  <TableCell>
                    {decodeHtmlEntities(pub.title)}
                    {pub.invited && categoryData.slug !== 'invited-talks' && (
                      <Badge variant="outline" className="ml-2 text-xs">
                        Invited
                      </Badge>
                    )}
                  </TableCell>
                  {categoryData.slug !== 'invited-talks' && categoryData.slug !== 'phd-thesis' && (
                    <TableCell>
                      {formatAuthorNames(pub.authors).map((author, idx, arr) => (
                        <React.Fragment key={idx}>
                          {isAlterman(author) ? (
                            <span className="font-semibold">{author}</span>
                          ) : (
                            author
                          )}
                          {idx < arr.length - 1 && ', '}
                        </React.Fragment>
                      ))}
                    </TableCell>
                  )}
                  {(categoryData.showJournal !== false) && (
                    <TableCell>{getJournalValue(pub)}</TableCell>
                  )}
                  {categoryData.showCitations && (
                    <TableCell className="text-center">{pub.citations}</TableCell>
                  )}
                  {(categoryData.showLinks !== false) && (
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
                  )}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}
    </div>
  )
}
