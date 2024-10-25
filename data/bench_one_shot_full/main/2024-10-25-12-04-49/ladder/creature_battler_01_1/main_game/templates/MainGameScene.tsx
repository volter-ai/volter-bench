import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Heart, Swords, User, Bot } from 'lucide-react';

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
  collections: {
    creatures: Creature[];
  };
}

interface GameUIData {
  entities: {
    player: Player;
    bot: Player;
    player_creature: Creature;
    bot_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const botCreature = props.data.entities.bot_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Battle Arena</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        {/* Player Creature */}
        <div className="w-1/3 bg-white rounded-lg shadow-md p-4 flex flex-col items-center">
          <User className="w-12 h-12 text-blue-500 mb-2" />
          <h2 className="text-lg font-semibold">{playerCreature?.display_name}</h2>
          <div className="flex items-center mt-2">
            <Heart className="w-4 h-4 text-red-500 mr-1" />
            <span>{playerCreature?.stats.hp} / {playerCreature?.stats.max_hp}</span>
          </div>
        </div>

        <Swords className="w-12 h-12 text-gray-500" />

        {/* Bot Creature */}
        <div className="w-1/3 bg-white rounded-lg shadow-md p-4 flex flex-col items-center">
          <Bot className="w-12 h-12 text-red-500 mb-2" />
          <h2 className="text-lg font-semibold">{botCreature?.display_name}</h2>
          <div className="flex items-center mt-2">
            <Heart className="w-4 h-4 text-red-500 mr-1" />
            <span>{botCreature?.stats.hp} / {botCreature?.stats.max_hp}</span>
          </div>
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white border-t-2 border-gray-200 p-4">
        <div className="mb-4 h-24 bg-gray-100 rounded p-2 overflow-y-auto">
          {/* Game text would go here */}
          <p>Battle in progress...</p>
        </div>
        <div className="flex flex-wrap justify-center gap-2">
          {availableButtonSlugs.includes('tackle') && (
            <button
              onClick={() => emitButtonClick('tackle')}
              className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded"
            >
              Tackle
            </button>
          )}
          {/* Add more buttons here as needed */}
        </div>
      </div>
    </div>
  );
}
