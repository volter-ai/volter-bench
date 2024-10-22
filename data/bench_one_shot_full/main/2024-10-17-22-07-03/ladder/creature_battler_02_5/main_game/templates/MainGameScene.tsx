import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Heart, Swords, Shield, Wind } from 'lucide-react';

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
    opponent: Player;
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { enabledUIDs } = useThingInteraction();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Creature Battle</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-between p-4">
        {/* Player Creature */}
        <div className="w-1/3 p-4 bg-green-100 rounded-lg shadow-md">
          <h2 className="text-lg font-bold">{playerCreature?.display_name || 'Player Creature'}</h2>
          <div className="flex items-center mt-2">
            <Heart className="w-5 h-5 text-red-500 mr-2" />
            <span>{playerCreature?.stats.hp || 0} / {playerCreature?.stats.max_hp || 0}</span>
          </div>
          <div className="flex items-center mt-1">
            <Swords className="w-5 h-5 text-orange-500 mr-2" />
            <span>{playerCreature?.stats.attack || 0}</span>
          </div>
          <div className="flex items-center mt-1">
            <Shield className="w-5 h-5 text-blue-500 mr-2" />
            <span>{playerCreature?.stats.defense || 0}</span>
          </div>
          <div className="flex items-center mt-1">
            <Wind className="w-5 h-5 text-green-500 mr-2" />
            <span>{playerCreature?.stats.speed || 0}</span>
          </div>
        </div>

        {/* Opponent Creature */}
        <div className="w-1/3 p-4 bg-red-100 rounded-lg shadow-md">
          <h2 className="text-lg font-bold">{opponentCreature?.display_name || 'Opponent Creature'}</h2>
          <div className="flex items-center mt-2">
            <Heart className="w-5 h-5 text-red-500 mr-2" />
            <span>{opponentCreature?.stats.hp || 0} / {opponentCreature?.stats.max_hp || 0}</span>
          </div>
          <div className="flex items-center mt-1">
            <Swords className="w-5 h-5 text-orange-500 mr-2" />
            <span>{opponentCreature?.stats.attack || 0}</span>
          </div>
          <div className="flex items-center mt-1">
            <Shield className="w-5 h-5 text-blue-500 mr-2" />
            <span>{opponentCreature?.stats.defense || 0}</span>
          </div>
          <div className="flex items-center mt-1">
            <Wind className="w-5 h-5 text-green-500 mr-2" />
            <span>{opponentCreature?.stats.speed || 0}</span>
          </div>
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 rounded-t-lg shadow-md">
        <div className="mb-4 h-24 overflow-y-auto bg-gray-100 p-2 rounded">
          {/* Game text would go here */}
          <p>Battle in progress...</p>
        </div>
        <div className="flex flex-wrap justify-center gap-2">
          {availableButtonSlugs.includes('play-again') && (
            <button
              onClick={() => emitButtonClick('play-again')}
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
              Play Again
            </button>
          )}
          {availableButtonSlugs.includes('quit') && (
            <button
              onClick={() => emitButtonClick('quit')}
              className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
            >
              Quit
            </button>
          )}
          {availableButtonSlugs.includes('tackle') && (
            <button
              onClick={() => emitButtonClick('tackle')}
              className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
            >
              Tackle
            </button>
          )}
          {playerCreature?.collections.skills.map((skill) => (
            <button
              key={skill.uid}
              onClick={() => emitButtonClick(skill.uid)}
              className="bg-purple-500 text-white px-4 py-2 rounded hover:bg-purple-600"
            >
              {skill.display_name}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
