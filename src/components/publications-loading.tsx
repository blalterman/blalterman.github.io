import { Skeleton } from "@/components/ui/skeleton";
import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from "@/components/ui/table";

export function PublicationsLoading() {
  return (
    <div className="container mx-auto py-16 md:py-24 animate-pulse">
      <div className="text-center mb-12">
        <Skeleton className="h-10 w-1/2 mx-auto" />
        <Skeleton className="h-6 w-3/4 mx-auto mt-4" />
      </div>
      <div className="flex justify-center flex-wrap gap-x-8 mb-12">
        <div className="flex flex-col items-center">
            <Skeleton className="h-8 w-12 mb-2" />
            <Skeleton className="h-4 w-20" />
        </div>
        <div className="flex flex-col items-center">
            <Skeleton className="h-8 w-12 mb-2" />
            <Skeleton className="h-4 w-24" />
        </div>
        <div className="flex flex-col items-center">
            <Skeleton className="h-8 w-12 mb-2" />
            <Skeleton className="h-4 w-24" />
        </div>
        <div className="flex flex-col items-center">
            <Skeleton className="h-8 w-12 mb-2" />
            <Skeleton className="h-4 w-28" />
        </div>
        <div className="flex flex-col items-center">
            <Skeleton className="h-8 w-12 mb-2" />
            <Skeleton className="h-4 w-28" />
        </div>
      </div>

      <h2 className="text-2xl font-bold mt-8 text-center">
        <Skeleton className="h-8 w-1/3 mx-auto" />
      </h2>
      <div className="border rounded-lg overflow-hidden shadow-lg max-w-screen-xl mx-auto mt-4">
        <Table>
          <TableHeader>
            <TableRow className="bg-muted/50">
                <TableHead className="w-[100px]"><Skeleton className="h-5 w-full" /></TableHead>
                <TableHead><Skeleton className="h-5 w-full" /></TableHead>
                <TableHead><Skeleton className="h-5 w-full" /></TableHead>
                <TableHead><Skeleton className="h-5 w-full" /></TableHead>
                <TableHead className="text-center w-[100px]"><Skeleton className="h-5 w-full" /></TableHead>
                <TableHead className="text-right w-[150px]"><Skeleton className="h-5 w-full" /></TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {[...Array(5)].map((_, index) => (
              <TableRow key={index} className="hover:bg-muted/30">
                <TableCell><Skeleton className="h-5 w-full" /></TableCell>
                <TableCell><Skeleton className="h-5 w-full" /></TableCell>
                <TableCell><Skeleton className="h-5 w-full" /></TableCell>
                <TableCell><Skeleton className="h-5 w-full" /></TableCell>
                <TableCell><Skeleton className="h-5 w-full" /></TableCell>
                <TableCell className="text-right space-x-2">
                    <div className="flex justify-end gap-2">
                        <Skeleton className="h-8 w-8 rounded-full" />
                    </div>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
