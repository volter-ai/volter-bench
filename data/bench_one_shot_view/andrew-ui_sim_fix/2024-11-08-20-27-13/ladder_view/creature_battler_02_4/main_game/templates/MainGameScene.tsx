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
    <Card 
      className={`p-4 w-[300px] ${isPlayer ? 'ml-8' : 'mr-8'}`}
      uid={uid}
    >
      <div className="space-y-4">
        <div className="text-lg font-bold">{creature.display_name}</div>
        
        <Progress 
          value={hpPercentage} 
          className="w-full"
          uid={`${uid}-hp-bar`}
        />
        
        <div className="text-sm">
          {creature.stats.hp}/{creature.stats.max_hp} HP
        </div>

        <div className="flex justify-between text-sm">
          <div className="flex items-center">
            <Sword className="w-4 h-4 mr-1" />
            {creature.stats.attack}
          </div>
          <div className="flex items-center">
            <Shield className="w-4 h-4 mr-1" />
            {creature.stats.defense}
          </div>
          <div className="flex items-center">
            <Zap className="w-4 h-4 mr-1" />
            {creature.stats.speed}
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
      <Card className="w-full p-4 rounded-none" uid={`${props.data.uid}-hud`}>
        <h1 className="text-xl font-bold">Battle Arena</h1>
      </Card>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center" uid={`${props.data.uid}-battlefield`}>
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

      {/* Action UI */}
      <Card className="w-full p-4" uid={`${props.data.uid}-ui`}>
        <div className="grid grid-cols-2 gap-4">
          {playerCreature?.collections?.skills?.map(skill => 
            availableButtonSlugs.includes(skill.display_name.toLowerCase()) ? (
              <Button
                key={skill.uid}
                onClick={() => emitButtonClick(skill.display_name.toLowerCase())}
                variant="outline"
                className="h-auto py-4"
                uid={`${props.data.uid}-skill-${skill.uid}`}
              >
                <div className="text-left">
                  <div className="font-semibold">{skill.display_name}</div>
                  <div className="text-sm text-muted-foreground">
                    {skill.description}
                  </div>
                </div>
              </Button>
            ) : null
          )}
        </div>
      </Card>
    </div>
  );
}
