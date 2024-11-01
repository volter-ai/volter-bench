import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Heart, Swords, User } from 'lucide-react';
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { NavBar } from "@/components/ui/navbar";

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
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player_creature;
  const botCreature = props.data.entities.bot_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <NavBar uid="main-game-navbar" className="bg-blue-600 text-white p-2 flex justify-between items-center">
        <div className="flex items-center">
          <User className="mr-2" />
          <span>{props.data.entities.player.display_name}</span>
        </div>
        <div>
          <Swords className="inline mr-2" />
          <span>Battle in Progress</span>
        </div>
      </NavBar>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        {/* Player Creature */}
        <Card uid={`player-creature-${playerCreature?.uid}`} className="w-1/3 bg-white rounded-lg shadow p-4 flex flex-col items-center">
          <h2 className="text-xl font-bold mb-2">{playerCreature?.display_name || 'Player Creature'}</h2>
          <div className="flex items-center">
            <Heart className="text-red-500 mr-2" />
            <span>{playerCreature?.stats.hp || 0} / {playerCreature?.stats.max_hp || 0}</span>
          </div>
        </Card>

        <div className="text-2xl font-bold">VS</div>

        {/* Bot Creature */}
        <Card uid={`bot-creature-${botCreature?.uid}`} className="w-1/3 bg-white rounded-lg shadow p-4 flex flex-col items-center">
          <h2 className="text-xl font-bold mb-2">{botCreature?.display_name || 'Opponent Creature'}</h2>
          <div className="flex items-center">
            <Heart className="text-red-500 mr-2" />
            <span>{botCreature?.stats.hp || 0} / {botCreature?.stats.max_hp || 0}</span>
          </div>
        </Card>
      </div>

      {/* User Interface */}
      <Card uid="user-interface" className="bg-white p-4 rounded-t-lg shadow">
        <div className="mb-4 h-20 bg-gray-200 rounded p-2">
          {/* Game description text would go here */}
          <p>Battle in progress. Choose your action!</p>
        </div>
        <div className="flex flex-wrap justify-center gap-2">
          {availableButtonSlugs.includes('tackle') && (
            <Button
              uid="tackle-button"
              onClick={() => emitButtonClick('tackle')}
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >
              Tackle
            </Button>
          )}
          {/* Add more buttons here as needed */}
        </div>
      </Card>
    </div>
  )
}
