import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Swords, Shield, Heart } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Separator } from "@/components/ui/separator";

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
}

interface Creature {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    hp: number;
    max_hp: number;
    attack: number;
    defense: number;
    speed: number;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
  uid: string;
  display_name: string;
  collections: {
    creatures: Creature[];
  };
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

export function MainGameSceneView(props: { data?: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  if (!props.data) {
    return (
      <div className="w-full h-full flex items-center justify-center">
        <Card className="p-4">
          <p>Loading game data...</p>
        </Card>
      </div>
    );
  }

  const formatSkillSlug = (name: string): string => {
    return name.toLowerCase().replace(/\s+/g, '_');
  };

  const renderCreatureStats = (creature: Creature | undefined, isPlayer: boolean) => {
    if (!creature) return null;
    
    const healthPercentage = (creature.stats.hp / creature.stats.max_hp) * 100;
    
    return (
      <Card className={`w-[300px] ${isPlayer ? 'ml-4' : 'mr-4'}`}>
        <div className="p-4 space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-bold">{creature.display_name}</h3>
            <span className="text-sm text-muted-foreground">
              {creature.stats.hp}/{creature.stats.max_hp} HP
            </span>
          </div>
          
          <Progress value={healthPercentage} className="w-full" />
          
          <div className="grid grid-cols-3 gap-2 text-sm">
            <div className="flex items-center">
              <Heart className="w-4 h-4 mr-1" />
              {creature.stats.hp}
            </div>
            <div className="flex items-center">
              <Swords className="w-4 h-4 mr-1" />
              {creature.stats.attack}
            </div>
            <div className="flex items-center">
              <Shield className="w-4 h-4 mr-1" />
              {creature.stats.defense}
            </div>
          </div>
        </div>
      </Card>
    );
  };

  const renderSkillButtons = () => {
    if (!props.data?.entities.player_creature?.collections.skills) {
      return null;
    }

    return props.data.entities.player_creature.collections.skills.map((skill) => {
      const skillSlug = formatSkillSlug(skill.display_name);
      if (!availableButtonSlugs.includes(skillSlug)) {
        return null;
      }

      return (
        <Button
          key={skill.uid}
          variant="default"
          className="w-full justify-start text-left h-auto"
          onClick={() => emitButtonClick(skillSlug)}
          data-testid={`skill-button-${skillSlug}`}
          role="button"
          aria-label={skill.display_name}
        >
          <div className="flex flex-col items-start">
            <span className="font-semibold">{skill.display_name}</span>
            <span className="text-sm text-muted-foreground">{skill.description}</span>
          </div>
        </Button>
      );
    });
  };

  return (
    <div className="w-full h-full flex flex-col">
      <header className="h-[10%] bg-background border-b">
        <div className="container h-full flex items-center">
          <h1 className="text-xl font-bold">Battle Arena</h1>
        </div>
      </header>

      <main className="flex-grow flex flex-col min-h-0">
        <div className="flex-1 flex justify-between items-center px-8 bg-muted/50">
          <div className="flex-1 flex justify-start">
            {renderCreatureStats(props.data.entities.player_creature, true)}
          </div>
          <Separator orientation="vertical" className="h-1/2" />
          <div className="flex-1 flex justify-end">
            {renderCreatureStats(props.data.entities.opponent_creature, false)}
          </div>
        </div>

        <Card className="h-[30%] rounded-none border-t">
          <div className="h-full p-4 space-y-2 overflow-y-auto">
            {renderSkillButtons()}
          </div>
        </Card>
      </main>
    </div>
  );
}
