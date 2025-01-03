import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Droplet, Flame } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
  meta: {
    prototype_id: string;
    category: string;
    skill_type: string;
    is_physical: boolean;
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

const CreatureStatus = ({ creature, uid }: { creature: Creature; uid: string }) => {
  if (!creature) return null;
  
  const hpPercentage = (creature.stats.hp / creature.stats.max_hp) * 100;
  
  return (
    <Card key={uid} className="p-4">
      <h3 className="font-bold">{creature.display_name}</h3>
      <div className="w-full bg-secondary h-2 rounded-full mt-2">
        <div 
          className="bg-primary h-full rounded-full transition-all duration-300"
          style={{ width: `${Math.max(0, Math.min(100, hpPercentage))}%` }}
        />
      </div>
      <div className="text-sm mt-1">
        {creature.stats.hp}/{creature.stats.max_hp} HP
      </div>
    </Card>
  );
};

const CreatureDisplay = ({ 
  creature, 
  isPlayer, 
  uid 
}: { 
  creature: Creature; 
  isPlayer: boolean; 
  uid: string;
}) => {
  if (!creature) return null;

  const TypeIcon = creature.meta.creature_type === 'water' ? Droplet : Flame;

  return (
    <div key={uid} className="relative w-full h-full">
      <div className={`
        absolute bottom-0 w-32 h-32 
        ${isPlayer ? 'left-0' : 'right-0'}
        after:content-[''] after:absolute after:bottom-0 
        after:w-full after:h-4 after:bg-gradient-to-t 
        after:from-black/20 after:to-transparent
      `}>
        <Card className="w-full h-full flex items-center justify-center">
          <TypeIcon className="h-8 w-8" />
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

  const { player_creature, opponent_creature } = props.data?.entities ?? {};

  if (!player_creature || !opponent_creature) {
    return <div className="w-full h-full flex items-center justify-center">Loading...</div>;
  }

  return (
    <div className="w-full h-full aspect-w-16 aspect-h-9 bg-gradient-to-b from-background to-secondary">
      {/* Battlefield Area */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
        <div className="row-start-2 col-start-1">
          <CreatureDisplay 
            creature={player_creature} 
            isPlayer={true}
            uid={player_creature.uid} 
          />
        </div>
        <div className="row-start-2 col-start-2">
          <CreatureStatus 
            creature={player_creature}
            uid={player_creature.uid} 
          />
        </div>
        <div className="row-start-1 col-start-2">
          <CreatureDisplay 
            creature={opponent_creature} 
            isPlayer={false}
            uid={opponent_creature.uid} 
          />
        </div>
        <div className="row-start-1 col-start-1">
          <CreatureStatus 
            creature={opponent_creature}
            uid={opponent_creature.uid} 
          />
        </div>
      </div>

      {/* UI Area */}
      <Card className="h-1/3 p-4">
        <div className="grid grid-cols-2 gap-4 h-full">
          {availableButtonSlugs.includes('tackle') && (
            <Button
              key="tackle-btn"
              onClick={() => emitButtonClick('tackle')}
              variant="default"
              className="w-full h-full"
            >
              <Sword className="mr-2 h-4 w-4" />
              Tackle
            </Button>
          )}
          {availableButtonSlugs.includes('lick') && (
            <Button
              key="lick-btn"
              onClick={() => emitButtonClick('lick')}
              variant="default"
              className="w-full h-full"
            >
              <Droplet className="mr-2 h-4 w-4" />
              Lick
            </Button>
          )}
        </div>
      </Card>
    </div>
  );
}
