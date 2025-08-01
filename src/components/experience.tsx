import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Briefcase, GraduationCap } from "lucide-react";

const educationData = [
    {
        institution: "Massachusetts Institute of Technology (MIT)",
        degree: "Ph.D. in Planetary Science",
        period: "2016 - 2020",
        notes: "Dissertation: 'Atmospheric Dynamics of Hot Jupiters'. Advised by Dr. Sara Seager."
    },
    {
        institution: "California Institute of Technology (Caltech)",
        degree: "B.S. in Astrophysics, with Honors",
        period: "2012 - 2016",
        notes: "Senior Thesis: 'Spectroscopic Analysis of K-type Stars'."
    }
];

const professionalData = [
    {
        title: "Postdoctoral Research Fellow",
        institution: "NASA Jet Propulsion Laboratory (JPL)",
        period: "2020 - Present",
        responsibilities: [
            "Lead investigator on the Mars 2020 mission's PIXL instrument data analysis.",
            "Developed machine learning pipelines for identifying biosignatures in planetary data.",
            "Collaborated with international teams on exoplanet atmosphere characterization."
        ]
    },
    {
        title: "Graduate Research Assistant",
        institution: "MIT Department of Earth, Atmospheric and Planetary Sciences",
        period: "2016 - 2020",
        responsibilities: [
            "Conducted numerical simulations of exoplanetary atmospheres.",
            "Authored and co-authored 4 peer-reviewed publications.",
            "Mentored undergraduate students in research projects."
        ]
    }
];

export function Experience() {
    return (
        <section id="experience" className="container py-16 md:py-24">
            <div className="text-center mb-16">
                <h2 className="text-3xl md:text-4xl font-bold font-headline">Experience & Education</h2>
                <p className="text-lg text-muted-foreground mt-2">My academic journey and professional background.</p>
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
                <div>
                    <h3 className="flex items-center text-2xl font-bold mb-6">
                        <GraduationCap className="mr-3 h-7 w-7 text-primary" />
                        Education
                    </h3>
                    <div className="space-y-8">
                        {educationData.map((edu) => (
                            <Card key={edu.institution} className="shadow-lg">
                                <CardHeader>
                                    <CardTitle>{edu.institution}</CardTitle>
                                    <CardDescription>{edu.degree}</CardDescription>
                                    <p className="text-sm text-muted-foreground pt-1">{edu.period}</p>
                                </CardHeader>
                                <CardContent>
                                    <p className="text-sm">{edu.notes}</p>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </div>
                <div>
                    <h3 className="flex items-center text-2xl font-bold mb-6">
                        <Briefcase className="mr-3 h-7 w-7 text-primary" />
                        Professional Positions
                    </h3>
                    <div className="space-y-8">
                        {professionalData.map((job) => (
                            <Card key={job.title} className="shadow-lg">
                                <CardHeader>
                                    <CardTitle>{job.title}</CardTitle>
                                    <CardDescription>{job.institution}</CardDescription>
                                     <p className="text-sm text-muted-foreground pt-1">{job.period}</p>
                                </CardHeader>
                                <CardContent>
                                    <ul className="list-disc list-inside space-y-2 text-sm">
                                        {job.responsibilities.map((item, index) => (
                                            <li key={index}>{item}</li>
                                        ))}
                                    </ul>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    );
}
