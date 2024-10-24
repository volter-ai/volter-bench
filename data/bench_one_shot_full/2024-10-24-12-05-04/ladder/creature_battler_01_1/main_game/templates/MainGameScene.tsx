import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Heart, Swords, User } from 'lucide-react';

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
    <div className="w-full h-full aspect-video flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2 flex justify-between items-center">
        <div className="flex items-center">
          <User className="mr-2" />
          <span>{props.data.entities.player.display_name}</span>
        </div>
        <div>
          <Swords className="mr-2 inline" />
          <span>Battle in Progress</span>
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4 bg-green-200">
        {/* Player Creature */}
        <div className="text-center">
          <div className="bg-white rounded-lg p-4 shadow-md">
            <h3 className="font-bold">{playerCreature?.display_name}</h3>
            <p className="flex items-center justify-center">
              <Heart className="text-red-500 mr-1" />
              {playerCreature?.stats.hp} / {playerCreature?.stats.max_hp}
            </p>
          </div>
          <div className="mt-2 text-blue-600 font-semibold">Player's Creature</div>
        </div>

        {/* Opponent Creature */}
        <div className="text-center">
          <div className="bg-white rounded-lg p-4 shadow-md">
            <h3 className="font-bold">{botCreature?.display_name}</h3>
            <p className="flex items-center justify-center">
              <Heart className="text-red-500 mr-1" />
              {botCreature?.stats.hp} / {botCreature?.stats.max_hp}
            </p>
          </div>
          <div className="mt-2 text-red-600 font-semibold">Opponent's Creature</div>
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-gray-200 p-4 h-1/3">
        <div className="bg-white rounded-lg p-4 h-full overflow-y-auto">
          {availableButtonSlugs.includes('tackle') ? (
            <button
              onClick={() => emitButtonClick('tackle')}
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 mr-2 mb-2"
            >
              Tackle
            </button>
          ) : (
            <p className="text-gray-600">Waiting for your turn...</p>
          )}
          {/* Add more buttons here as needed */}
        </div>
      </div>
    </div>
  );
}
