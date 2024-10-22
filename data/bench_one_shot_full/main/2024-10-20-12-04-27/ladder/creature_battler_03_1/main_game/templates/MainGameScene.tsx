import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Button } from "@/components/ui/button";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Shield, Swords } from 'lucide-react';

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

  const { player, opponent, player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <div className="bg-gray-800 text-white p-2 flex justify-between items-center">
        <PlayerCard
          uid={player?.uid || ""}
          playerName={player?.display_name || "Unknown Player"}
          imageUrl="/placeholder-player.png"
        />
        <PlayerCard
          uid={opponent?.uid || ""}
          playerName={opponent?.display_name || "Unknown Opponent"}
          imageUrl="/placeholder-opponent.png"
        />
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <Shield className="w-8 h-8 mb-2 text-blue-500" />
          <CreatureCard
            uid={player_creature?.uid || ""}
            name={player_creature?.display_name || "Unknown"}
            imageUrl={`/creatures/${player_creature?.uid || 'placeholder'}.png`}
            hp={player_creature?.stats.hp || 0}
            maxHp={player_creature?.stats.max_hp || 1}
          />
        </div>
        <div className="flex flex-col items-center">
          <Swords className="w-8 h-8 mb-2 text-red-500" />
          <CreatureCard
            uid={opponent_creature?.uid || ""}
            name={opponent_creature?.display_name || "Unknown"}
            imageUrl={`/creatures/${opponent_creature?.uid || 'placeholder'}.png`}
            hp={opponent_creature?.stats.hp || 0}
            maxHp={opponent_creature?.stats.max_hp || 1}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t border-gray-300">
        <div className="grid grid-cols-2 gap-2">
          {player_creature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}`}
            />
          ))}
        </div>
        <div className="mt-4 flex justify-center space-x-2">
          {availableButtonSlugs.includes("play-again") && (
            <Button onClick={() => emitButtonClick("play-again")}>Play Again</Button>
          )}
          {availableButtonSlugs.includes("quit-to-main-menu") && (
            <Button onClick={() => emitButtonClick("quit-to-main-menu")}>Quit to Main Menu</Button>
          )}
        </div>
      </div>
    </div>
  );
}
