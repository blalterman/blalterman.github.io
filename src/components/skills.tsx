"use client"

import { useState, useEffect } from 'react';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Code, Database, Rocket, BrainCircuit } from 'lucide-react';

const icons: { [key: string]: React.ElementType } = {
  Code: Code,
  BrainCircuit: BrainCircuit,
  Rocket: Rocket,
  Database: Database
};

interface SkillsData {
  [category: string]: {
    icon: string;
    skills: string[];
  };
}

export function Skills() {
  const [skillsData, setSkillsData] = useState<SkillsData | null>(null);

  useEffect(() => {
    async function fetchSkills() {
      try {
        const response = await fetch('/data/skills.json');
        const data = await response.json();
        setSkillsData(data);
      } catch (error) {
        console.error("Failed to fetch skills data", error);
      }
    }
    fetchSkills();
  }, []);

  if (!skillsData) {
    return (
      <section id="skills" className="py-16 md:py-24">
        <div className="container text-center">
          <p>Loading skills...</p>
        </div>
      </section>
    );
  }

  return (
    <section id="skills" className="py-16 md:py-24">
      <div className="container">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold font-headline">Skills & Tools</h2>
          <p className="text-lg text-muted-foreground mt-2">A selection of my technical abilities and project involvements.</p>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {Object.entries(skillsData).map(([category, data]) => {
            const IconComponent = icons[data.icon];
            return (
              <Card key={category} className="shadow-lg hover:shadow-xl transition-shadow duration-300 flex flex-col">
                <CardHeader className="flex flex-row items-center gap-4 pb-4">
                  {IconComponent && <IconComponent className="h-8 w-8 text-primary" />}
                  <CardTitle>{category}</CardTitle>
                </CardHeader>
                <CardContent className="flex flex-wrap gap-2 flex-grow">
                  {data.skills.map((skill) => (
                    <Badge key={skill} variant="secondary">{skill}</Badge>
                  ))}
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    </section>
  );
}
