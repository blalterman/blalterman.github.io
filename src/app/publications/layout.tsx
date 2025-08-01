import { Contact } from "@/components/contact";
import { Header } from "@/components/header";

export default function PublicationsLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    return (
        <div className="flex min-h-screen w-full flex-col bg-background">
            <Header />
            <main className="flex-1">{children}</main>
            <Contact />
        </div>
    );
}
