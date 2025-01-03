import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Droplet, Flame } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";

interface Skill {
  __type: string;
  uid: string;
  display_name: string;
  description: string;
  meta: {
    prototype_id: string;
    category: string;
    skill_type: string;
    is_physical: boolean;
  };
  stats: {
    base_damage: number;
  };
}

interface Creature {
  __type: string;
  uid: string;
  display_name: string;
  description: string;
  stats: {
    hp: number;
    max_hp: number;
    attack: number;
    defense: number;
    sp_attack: number;
    sp_defense: number;
    speed: number;
  };
  meta: {
    prototype_id: string;
    category: string;
    creature_type: string;
  };
  collections: {
    skills: Skill[];
  };
}

interface GameUIData {
  entities: {
    player: {
      uid: string;
      collections: {
        creatures: Creature[];
      };
    };
    opponent: {
      uid: string;
      collections: {
        creatures: Creature[];
      };
    };
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

interface StatusDisplayProps {
  uid: string;
  creature: Creature | undefined;
}

const StatusDisplay = ({ uid, creature }: StatusDisplayProps) => {
  if (!creature) return null;

  const hpPercentage = (creature.stats.hp / creature.stats.max_hp) * 100;
  
  return (
    <Card className="p-4" key={uid}>
      <h3 className="font-bold">{creature.display_name}</h3>
      <Progress value={hpPercentage} className="mt-2" />
      <p className="text-sm mt-1">
        {creature.stats.hp}/{creature.stats.max_hp} HP
      </p>
    </Card>
  );
};

interface CreatureDisplayProps {
  uid: string;
  creature: Creature | undefined;
  isPlayer: boolean;
}

const CreatureDisplay = ({ uid, creature, isPlayer }: CreatureDisplayProps) => {
  if (!creature) return null;

  return (
    <div className="relative w-full h-full" key={uid}>
      <div className={`
        absolute bottom-0 w-32 h-32 
        ${isPlayer ? 'left-0' : 'right-0'}
        after:content-[''] after:absolute after:bottom-0 
        after:w-full after:h-4 after:bg-gradient-to-t 
        after:from-black/20 after:to-transparent
      `}>
        <Card className="w-full h-full flex items-center justify-center">
          {creature.meta.creature_type === 'water' ? 
            <Droplet className="h-8 w-8" /> : 
            <Flame className="h-8 w-8" />
          }
        </Card>
      </div>
    </div>
  );
};

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data?.entities?.player_creature;
  const opponentCreature = props.data?.entities?.opponent_creature;

  if (!playerCreature || !opponentCreature) {
    return <div>Loading...</div>;
  }

  return (
    <div className="w-full h-full aspect-w-16 aspect-h-9 bg-gradient-to-b from-slate-900 to-slate-800">
      {/* Battlefield Area */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
        <div className="row-start-2 col-start-1">
          <CreatureDisplay 
            uid={`player_creature_${playerCreature.uid}`}
            creature={playerCreature} 
            isPlayer={true} 
          />
        </div>
        <div className="row-start-2 col-start-2">
          <StatusDisplay 
            uid={`player_status_${playerCreature.uid}`}
            creature={playerCreature} 
          />
        </div>
        <div className="row-start-1 col-start-2">
          <CreatureDisplay 
            uid={`opponent_creature_${opponentCreature.uid}`}
            creature={opponentCreature} 
            isPlayer={false} 
          />
        </div>
        <div className="row-start-1 col-start-1">
          <StatusDisplay 
            uid={`opponent_status_${opponentCreature.uid}`}
            creature={opponentCreature} 
          />
        </div>
      </div>

      {/* UI Area */}
      <Card className="h-1/3 bg-slate-900/80 p-4">
        <div className="grid grid-cols-2 gap-4 h-full">
          {availableButtonSlugs.includes('tackle') && (
            <Button
              onClick={() => emitButtonClick('tackle')}
              className="flex items-center justify-center gap-2"
              variant="secondary"
            >
              <Sword className="h-5 w-5" />
              Tackle
            </Button>
          )}
          {availableButtonSlugs.includes('lick') && (
            <Button
              onClick={() => emitButtonClick('lick')}
              className="flex items-center justify-center gap-2"
              variant="secondary"
            >
              <Droplet className="h-5 w-5" />
              Lick
            </Button>
          )}
        </div>
      </Card>
    </div>
  );
}
