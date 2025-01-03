import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Heart, Droplet, Flame } from 'lucide-react';
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

interface Player {
  uid: string;
  display_name: string;
  description: string;
  stats: Record<string, number>;
  meta: {
    prototype_id: string;
    category: string;
  };
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

const CreatureDisplay = ({ creature, isOpponent }: { creature: Creature; isOpponent: boolean }) => (
  <Card className="relative w-full h-full flex flex-col p-4">
    <div className="flex justify-between items-center mb-2">
      <span className="font-bold">{creature.display_name}</span>
      {creature.meta.creature_type === 'water' ? <Droplet className="text-blue-500" /> : <Flame className="text-red-500" />}
    </div>
    
    <div className="space-y-2">
      <div className="flex justify-between text-sm">
        <span>HP</span>
        <span>{creature.stats.hp}/{creature.stats.max_hp}</span>
      </div>
      <Progress value={(creature.stats.hp / creature.stats.max_hp) * 100} />
    </div>

    <div className="mt-2 grid grid-cols-3 gap-2 text-sm">
      <div className="flex items-center gap-1">
        <Sword size={16} />
        {creature.stats.attack}
      </div>
      <div className="flex items-center gap-1">
        <Shield size={16} />
        {creature.stats.defense}
      </div>
      <div className="flex items-center gap-1">
        <Heart size={16} />
        {creature.stats.speed}
      </div>
    </div>

    <div className="flex-grow flex items-center justify-center">
      <div className="relative">
        <div className="w-32 h-32 bg-gray-400 rounded-full opacity-20 absolute bottom-0" />
        <div className={`w-32 h-32 ${isOpponent ? 'bg-red-500' : 'bg-blue-500'} rounded-lg`} />
      </div>
    </div>
  </Card>
);

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="w-full h-full aspect-[16/9] flex flex-col bg-gradient-to-b from-sky-900 to-sky-800">
      {/* Battlefield Area */}
      <div className="flex-grow-[2] grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {opponent_creature && (
          <>
            <CreatureDisplay creature={opponent_creature} isOpponent={true} />
            <div className="col-start-2 row-start-1">
              <Card className="h-full flex items-center justify-center">
                {/* Opponent creature sprite placeholder */}
              </Card>
            </div>
          </>
        )}

        {player_creature && (
          <>
            <div className="col-start-1 row-start-2">
              <Card className="h-full flex items-center justify-center">
                {/* Player creature sprite placeholder */}
              </Card>
            </div>
            <CreatureDisplay creature={player_creature} isOpponent={false} />
          </>
        )}
      </div>

      {/* UI Area */}
      <div className="flex-grow-[1] bg-gray-800/50 p-4">
        <div className="grid grid-cols-2 gap-4 h-full">
          {player_creature?.collections.skills.map((skill) => (
            availableButtonSlugs.includes(skill.meta.prototype_id) && (
              <Button
                key={skill.uid}
                onClick={() => emitButtonClick(skill.meta.prototype_id)}
                variant="secondary"
                className="h-full flex flex-col items-start p-4"
              >
                <span className="font-bold">{skill.display_name}</span>
                <span className="text-sm opacity-80">{skill.description}</span>
              </Button>
            )
          ))}
        </div>
      </div>
    </div>
  );
}
