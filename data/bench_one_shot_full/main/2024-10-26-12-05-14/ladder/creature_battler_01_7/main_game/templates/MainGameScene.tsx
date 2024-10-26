import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    damage: number;
  };
}

interface Creature {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
  uid: string;
  display_name: string;
  description: string;
  collections: {
    creatures: Creature[];
  };
}

interface GameUIData {
  entities: {
    player: Player;
    foe: Player;
    player_creature: Creature;
    foe_creature: Creature;
  };
}

const CreatureCard = ({ creature, isPlayer }: { creature: Creature; isPlayer: boolean }) => (
  <Card className={`p-4 ${isPlayer ? 'bg-blue-100' : 'bg-red-100'}`}>
    <h2 className="text-lg font-semibold">{creature.display_name}</h2>
    <p>HP: {creature.stats.hp} / {creature.stats.max_hp}</p>
    <Shield className={`mt-2 ${isPlayer ? 'text-blue-500' : 'text-red-500'}`} />
  </Card>
);

export function MainGameSceneView({ data }: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = data.entities.player_creature;
  const foeCreature = data.entities.foe_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <div className="bg-gray-800 text-white p-2">
        <h1 className="text-xl font-bold">Game HUD</h1>
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-between p-4">
        {playerCreature && <CreatureCard creature={playerCreature} isPlayer={true} />}
        <Swords className="text-red-500" />
        {foeCreature && <CreatureCard creature={foeCreature} isPlayer={false} />}
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-200">
        <Card className="mb-4 h-24 p-2 overflow-y-auto">
          <p>Game progress and actions will be described here...</p>
        </Card>
        <div className="flex flex-wrap gap-2">
          {availableButtonSlugs.includes('tackle') && (
            <Button
              onClick={() => emitButtonClick('tackle')}
              variant="default"
            >
              Tackle
            </Button>
          )}
          {/* Add more buttons here as needed */}
        </div>
      </div>
    </div>
  );
}
