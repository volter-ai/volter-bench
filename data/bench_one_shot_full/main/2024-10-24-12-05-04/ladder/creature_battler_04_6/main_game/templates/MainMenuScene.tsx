import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';
import { Button } from "@/components/ui/button";

// Interfaces for reused view data
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
  collections: {
    creatures: Creature[];
  };
}

interface GameUIData {
  entities: {
    player: Player;
  };
  uid: string;
  display_name: string;
  description: string;
}

export function MainMenuSceneView({ data }: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const player = data.entities.player;

  return (
    <div className="w-full h-full flex flex-col justify-between items-center p-4 bg-gradient-to-b from-blue-500 to-purple-600 text-white" style={{ aspectRatio: '16/9' }}>
      {/* Title Section */}
      <div className="flex-1 flex items-center">
        <h1 className="text-4xl md:text-6xl font-bold text-center">
          {data.display_name || 'Awesome Game Title'}
        </h1>
      </div>

      {/* Buttons Section */}
      <div className="mb-8">
        <p className="text-lg text-center mb-4">
          Welcome, {player?.display_name || 'Player'}!
        </p>
        <div className="flex flex-col space-y-4">
          {availableButtonSlugs.includes('play') && (
            <Button
              onClick={() => emitButtonClick('play')}
              className="flex items-center justify-center space-x-2"
            >
              <Play className="w-4 h-4" />
              <span>Play Game</span>
            </Button>
          )}
          {availableButtonSlugs.includes('quit') && (
            <Button
              onClick={() => emitButtonClick('quit')}
              variant="destructive"
              className="flex items-center justify-center space-x-2"
            >
              <X className="w-4 h-4" />
              <span>Quit Game</span>
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
