import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button"; 
import { Progress } from "@/components/ui/progress";

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
  uid: string;
}

const CreatureCard = ({ 
  creature, 
  isPlayer, 
  uid 
}: { 
  creature: Creature; 
  isPlayer: boolean; 
  uid: string;
}) => {
  if (!creature) return null;

  const hpPercentage = (creature.stats.hp / creature.stats.max_hp) * 100;

  return (
    <Card uid={uid} className={`p-4 w-[300px] ${isPlayer ? 'ml-8' : 'mr-8'}`}>
      <div className="space-y-4">
        <h3 className="text-lg font-semibold text-center">
          {creature.display_name}
          <span className="text-sm ml-2 text-muted-foreground">
            {isPlayer ? '(Player)' : '(Opponent)'}
          </span>
        </h3>

        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span>HP</span>
            <span>{creature.stats.hp}/{creature.stats.max_hp}</span>
          </div>
          <Progress value={hpPercentage} uid={`${uid}-hp`} />
        </div>

        <div className="flex justify-between text-sm">
          <div className="flex items-center gap-1">
            <Sword className="w-4 h-4" />
            <span>{creature.stats.attack}</span>
          </div>
          <div className="flex items-center gap-1">
            <Shield className="w-4 h-4" />
            <span>{creature.stats.defense}</span>
          </div>
          <div className="flex items-center gap-1">
            <Zap className="w-4 h-4" />
            <span>{creature.stats.speed}</span>
          </div>
        </div>
      </div>
    </Card>
  );
};

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="relative w-full h-full flex flex-col" uid={props.data.uid}>
      {/* HUD */}
      <div className="flex-none h-16 bg-background border-b px-4 flex items-center">
        <h1 className="text-xl font-bold">Battle Arena</h1>
      </div>

      {/* Battlefield */}
      <div className="flex-1 flex items-center justify-between p-4 bg-muted/20">
        {playerCreature && (
          <CreatureCard 
            creature={playerCreature} 
            isPlayer={true}
            uid={`${props.data.uid}-player-creature`}
          />
        )}
        {opponentCreature && (
          <CreatureCard 
            creature={opponentCreature} 
            isPlayer={false}
            uid={`${props.data.uid}-opponent-creature`}
          />
        )}
      </div>

      {/* Skills UI */}
      <Card className="flex-none p-4 rounded-t-xl" uid={`${props.data.uid}-skills`}>
        <div className="grid grid-cols-2 gap-4">
          {playerCreature?.collections.skills?.map(skill => 
            availableButtonSlugs.includes(skill.display_name.toLowerCase()) && (
              <Button
                key={skill.uid}
                uid={`${props.data.uid}-skill-${skill.uid}`}
                onClick={() => emitButtonClick(skill.display_name.toLowerCase())}
                variant="secondary"
                className="h-auto flex flex-col items-start p-4 space-y-1"
              >
                <span className="font-semibold">{skill.display_name}</span>
                <span className="text-sm text-muted-foreground">{skill.description}</span>
              </Button>
            )
          )}
        </div>
      </Card>
    </div>
  );
}
