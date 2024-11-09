import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";

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

interface GameUIData {
  entities: {
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  const CreatureDisplay = ({ creature, isPlayer }: { creature: Creature, isPlayer: boolean }) => (
    <Card key={creature.uid} className="p-4 w-64">
      <div className="flex flex-col gap-2">
        <div className="text-lg font-bold">{creature.display_name}</div>
        <div className="text-sm text-muted-foreground">
          {isPlayer ? "Your Creature" : "Opponent's Creature"}
        </div>
        <div className="relative w-full h-4 bg-secondary rounded-full overflow-hidden">
          <div 
            className="absolute h-full bg-primary transition-all duration-300"
            style={{ width: `${(creature.stats.hp / creature.stats.max_hp) * 100}%` }}
          />
        </div>
        <div className="text-sm text-muted-foreground">
          {creature.stats.hp}/{creature.stats.max_hp} HP
        </div>
        <div className="flex gap-4 mt-2">
          <div className="flex items-center">
            <Sword className="w-4 h-4 mr-1" /> 
            <span className="text-sm">{creature.stats.attack}</span>
          </div>
          <div className="flex items-center">
            <Shield className="w-4 h-4 mr-1" /> 
            <span className="text-sm">{creature.stats.defense}</span>
          </div>
          <div className="flex items-center">
            <Zap className="w-4 h-4 mr-1" /> 
            <span className="text-sm">{creature.stats.speed}</span>
          </div>
        </div>
      </div>
    </Card>
  );

  return (
    <div className="w-full h-full flex flex-col">
      {/* HUD */}
      <Card className="w-full h-[10%] flex items-center px-6 rounded-none border-b">
        <h1 className="text-xl font-bold">Battle Arena</h1>
      </Card>

      {/* Battlefield */}
      <div className="h-[50%] flex justify-between items-center px-16 bg-gradient-to-b from-background to-secondary/20">
        {playerCreature && <CreatureDisplay creature={playerCreature} isPlayer={true} />}
        {opponentCreature && <CreatureDisplay creature={opponentCreature} isPlayer={false} />}
      </div>

      {/* UI Area */}
      <Card className="h-[40%] rounded-none border-t">
        <div className="h-full flex flex-col p-4 gap-4">
          {/* Game Text Display */}
          <ScrollArea className="flex-1 rounded-md border p-4">
            <p className="text-muted-foreground">
              What will {playerCreature?.display_name} do?
            </p>
          </ScrollArea>

          {/* Skills Grid */}
          <div className="grid grid-cols-2 gap-4">
            {playerCreature?.collections.skills.map(skill => (
              availableButtonSlugs.includes(skill.display_name.toLowerCase()) && (
                <Button
                  key={skill.uid}
                  variant="secondary"
                  onClick={() => emitButtonClick(skill.display_name.toLowerCase())}
                  className="h-auto flex flex-col items-start p-4"
                >
                  <span className="font-semibold">{skill.display_name}</span>
                  <span className="text-sm text-muted-foreground">{skill.description}</span>
                </Button>
              )
            ))}
          </div>
        </div>
      </Card>
    </div>
  );
}
