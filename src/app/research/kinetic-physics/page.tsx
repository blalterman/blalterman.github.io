
import { Contact } from "@/components/contact";
import { Header } from "@/components/header";

export default function KineticPhysicsPage() {
    return (
        <div className="flex min-h-screen w-full flex-col bg-background">
            <Header />
            <main className="flex-1 container mx-auto py-16 md:py-24">
                <h1 className="text-3xl md:text-4xl font-bold font-headline">Kinetic Physics</h1>
                <p className="text-lg text-muted-foreground mt-4">
                    This page will introduce kinetic physics topics relevant to the heliosphere.
                </p>
            </main>
            <Contact />
        </div>
    );
}
