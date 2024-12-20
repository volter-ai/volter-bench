import { useCurrentButtons } from "@/lib/useChoices.ts";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Home, ArrowLeft } from 'lucide-react';

interface Skill {
  __type: "Skill";
  stats: {
    base_damage: number;
  };
  uid: string;
  display_name: string;
  description: string;
}

interface Creature {
  __type: "Creature";
  stats: {
    hp: number;
    max_hp: number;
    attack: number;
    defense: number;
    speed: number;
  };
  uid: string;
  display_name: string;
  description: string;
  collections: {
    skills: Skill[];
  };
}

interface Player {
  __type: "Player";
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

  const renderButtons = () => {
    return (
      <div className="flex space-x-2">
        {availableButtonSlugs.includes("quit-game") && (
          <button
            className="px-4 py-2 bg-red-500 text-white rounded"
            onClick={() => emitButtonClick("quit-game")}
          >
            <Home className="inline-block mr-2" />
            Quit Game
          </button>
        )}
        {availableButtonSlugs.includes("return-to-main-menu") && (
          <button
            className="px-4 py-2 bg-blue-500 text-white rounded"
            onClick={() => emitButtonClick("return-to-main-menu")}
          >
            <ArrowLeft className="inline-block mr-2" />
            Return to Main Menu
          </button>
        )}
      </div>
    );
  };

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <div className="bg-gray-800 text-white p-2 flex justify-between items-center">
        <span>{props.data.entities.player?.display_name}</span>
        {renderButtons()}
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <PlayerCard
            uid={props.data.entities.player?.uid || ""}
            playerName={props.data.entities.player?.display_name || "Player"}
            imageUrl=""
          />
          <CreatureCard
            uid={props.data.entities.player_creature?.uid || ""}
            name={props.data.entities.player_creature?.display_name || "Player Creature"}
            hp={props.data.entities.player_creature?.stats.hp || 0}
            maxHp={props.data.entities.player_creature?.stats.max_hp || 0}
          />
        </div>
        <div className="flex flex-col items-center">
          <PlayerCard
            uid={props.data.entities.opponent?.uid || ""}
            playerName={props.data.entities.opponent?.display_name || "Opponent"}
            imageUrl=""
          />
          <CreatureCard
            uid={props.data.entities.opponent_creature?.uid || ""}
            name={props.data.entities.opponent_creature?.display_name || "Opponent Creature"}
            hp={props.data.entities.opponent_creature?.stats.hp || 0}
            maxHp={props.data.entities.opponent_creature?.stats.max_hp || 0}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t border-gray-300">
        <div className="mb-4">
          <h3 className="text-lg font-bold mb-2">Player Skills</h3>
          <div className="flex space-x-2">
            {props.data.entities.player_creature?.collections.skills?.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.base_damage}`}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
