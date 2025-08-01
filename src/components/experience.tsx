import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Briefcase, GraduationCap } from "lucide-react";

const educationData = [
  {
    "Institution": "University of Michigan",
    "Department": "Applied Physics",
    "Location": "Ann Arbor, MI, USA",
    "Dates": "2012--2019"
  },
  {
    "Institution": "Macalester College",
    "Department": "Physics & Philosophy",
    "Location": "St. Paul, MN, USA",
    "Dates": "2008--2012"
  }
];

const professionalData = [
  {
    "Company": "NASA Goddard Space Flight Center",
    "Position Title": "Research Astrophysicist",
    "Dates": "2024 --",
    "Location": "Greenbelt, MD"
  },
  {
    "Company": "Southwest Research Institute",
    "Position Title": "Senior Research Scientist",
    "Dates": "2023 -- 2024",
    "Location": "San Antonio, TX"
  },
  {
    "Company": "Southwest Research Institute",
    "Position Title": "Research Scientist",
    "Dates": "2022 -- 2023",
    "Location": "San Antonio, TX"
  },
  {
    "Company": "Southwest Research Institute",
    "Position Title": "Postdoctoral Researcher",
    "Dates": "2020 -- 2021",
    "Location": "San Antonio, TX"
  },
  {
    "Company": "University of Texas at San Antonio",
    "Position Title": "Postdoctoral Researcher",
    "Dates": "2021--2022",
    "Location": "San Antonio, TX"
  },
  {
    "Company": "University of Michigan",
    "Position Title": "Research Fellow",
    "Dates": "2019--2020",
    "Location": "Ann Arbor, MI"
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
                            <Card key={edu.Institution} className="shadow-lg">
                                <CardHeader>
                                    <CardTitle>{edu.Institution}</CardTitle>
                                    <CardDescription>{edu.Department}</CardDescription>
                                    <p className="text-sm text-muted-foreground pt-1">{edu.Dates}</p>
                                </CardHeader>
                                <CardContent>
                                    <p className="text-sm">{edu.Location}</p>
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
                            <Card key={`${job["Position Title"]}-${job.Company}`} className="shadow-lg">
                                <CardHeader>
                                    <CardTitle>{job["Position Title"]}</CardTitle>
                                    <CardDescription>{job.Company}</CardDescription>
                                     <p className="text-sm text-muted-foreground pt-1">{job.Dates}</p>
                                </CardHeader>
                                <CardContent>
                                    <p className="text-sm">{job.Location}</p>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    );
}
