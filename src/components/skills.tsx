import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Code, Database, Rocket, BrainCircuit } from 'lucide-react';
import type { LucideIcon } from 'lucide-react';

const skillsData = {
  "Programming & Software": {
    icon: Code,
    skills: ["Python", "R", "SQL", "MATLAB", "Git & GitHub", "Docker"]
  },
  "Data Analysis & Viz": {
    icon: BrainCircuit,
    skills: ["Machine Learning", "Statistical Modeling", "Pandas & NumPy", "Matplotlib & Seaborn", "Plotly & Dash", "GIS"]
  },
  "Mission Involvement": {
    icon: Rocket,
    skills: ["Mars Rover Mission", "Hubble Telescope", "ExoMars Program", "James Webb ST"]
  },
  "Techniques & Methods": {
    icon: Database,
    skills: ["Spectroscopy", "Image Processing", "Numerical Simulation", "High-Performance Computing"]
  }
};

export function Skills() {
  return (
    <section id="skills" className="py-16 md:py-24">
      <div className="container">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold font-headline">Skills & Tools</h2>
          <p className="text-lg text-muted-foreground mt-2">A selection of my technical abilities and project involvements.</p>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {Object.entries(skillsData).map(([category, data]) => (
            <Card key={category} className="shadow-lg hover:shadow-xl transition-shadow duration-300 flex flex-col">
              <CardHeader className="flex flex-row items-center gap-4 pb-4">
                <data.icon className="h-8 w-8 text-primary" />
                <CardTitle>{category}</CardTitle>
              </CardHeader>
              <CardContent className="flex flex-wrap gap-2 flex-grow">
                {data.skills.map((skill) => (
                  <Badge key={skill} variant="secondary">{skill}</Badge>
                ))}
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
