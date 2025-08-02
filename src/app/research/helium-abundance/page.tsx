
import { Contact } from "@/components/contact";
import { Header } from "@/components/header";

export default function HeliumAbundancePage() {
    return (
        <div className="flex min-h-screen w-full flex-col bg-background">
            <Header />
            <main className="flex-1 container mx-auto py-16 md:py-24">
                <h1 className="text-3xl md:text-4xl font-bold font-headline">Helium Abundance</h1>
                <p className="text-lg text-muted-foreground mt-4">
                    This page will discuss research on helium abundance in the solar wind.
                </p>
            </main>
            <Contact />
        </div>
    );
}
