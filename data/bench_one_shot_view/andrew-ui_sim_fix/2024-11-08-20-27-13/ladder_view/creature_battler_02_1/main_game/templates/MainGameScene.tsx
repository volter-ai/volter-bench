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

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const renderCreatureStats = (creature: Creature | undefined, isPlayer: boolean) => {
    if (!creature) return null;
    
    const healthPercentage = (creature.stats.hp / creature.stats.max_hp) * 100;
    
    return (
      <Card className={`w-[300px] ${isPlayer ? 'ml-4' : 'mr-4'}`}>
        <div className="p-4 space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-bold">{creature.display_name}</h3>
            <div className="text-sm text-muted-foreground">
              {creature.stats.hp}/{creature.stats.max_hp} HP
            </div>
          </div>
          
          <Progress value={healthPercentage} className="w-full" />
          
          <div className="grid grid-cols-3 gap-2 pt-2">
            <div className="flex items-center justify-center">
              <Heart className="w-4 h-4 mr-1" />
              <span className="text-sm">{creature.stats.hp}</span>
            </div>
            <div className="flex items-center justify-center">
              <Swords className="w-4 h-4 mr-1" />
              <span className="text-sm">{creature.stats.attack}</span>
            </div>
            <div className="flex items-center justify-center">
              <Shield className="w-4 h-4 mr-1" />
              <span className="text-sm">{creature.stats.defense}</span>
            </div>
          </div>
        </div>
      </Card>
    );
  };

  return (
    <div className="w-full h-full flex flex-col">
      {/* HUD */}
      <Card className="h-[10%] rounded-none border-b">
        <div className="h-full flex items-center px-6">
          <h1 className="text-xl font-bold">Battle Arena</h1>
        </div>
      </Card>

      {/* Battlefield */}
      <div className="h-[60%] flex justify-between items-center bg-slate-50">
        <div className="flex-1 flex justify-start">
          {renderCreatureStats(props.data.entities.player_creature, true)}
        </div>
        <Separator orientation="vertical" className="h-1/2" />
        <div className="flex-1 flex justify-end">
          {renderCreatureStats(props.data.entities.opponent_creature, false)}
        </div>
      </div>

      {/* Action UI */}
      <Card className="h-[30%] rounded-none border-t">
        <div className="h-full p-4 space-y-2 overflow-y-auto">
          {props.data.entities.player_creature?.collections.skills.map((skill) => (
            availableButtonSlugs.includes(skill.display_name.toLowerCase()) && (
              <Button
                key={skill.uid}
                variant="default"
                className="w-full justify-start"
                onClick={() => emitButtonClick(skill.display_name.toLowerCase())}
              >
                <div className="flex flex-col items-start">
                  <span className="font-semibold">{skill.display_name}</span>
                  <span className="text-sm text-muted-foreground">{skill.description}</span>
                </div>
              </Button>
            )
          ))}
        </div>
      </Card>
    </div>
  );
}
