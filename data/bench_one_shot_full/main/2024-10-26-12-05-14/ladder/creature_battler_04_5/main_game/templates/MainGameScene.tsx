import { useCurrentButtons } from "@/lib/useChoices.ts";
import { ArrowLeft } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { Button } from "@/components/ui/button";

interface Creature {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  meta: {
    creature_type: string;
  };
}

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
}

interface Player {
  uid: string;
  display_name: string;
  description: string;
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
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const player = props.data.entities.player;
  const opponent = props.data.entities.opponent;
  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-6xl aspect-video bg-white shadow-lg rounded-lg overflow-hidden flex flex-col">
        {/* Battlefield Display */}
        <div className="flex-grow grid grid-cols-2 grid-rows-2 p-4 gap-4">
          {/* Opponent Creature Status */}
          <div className="row-start-1 col-start-1 flex items-start justify-start">
            <CreatureCard
              uid={opponentCreature?.uid || ""}
              name={opponentCreature?.display_name || "Unknown"}
              image={`/creatures/${opponentCreature?.meta.creature_type || 'unknown'}_front.png`}
              hp={opponentCreature?.stats.hp || 0}
              maxHp={opponentCreature?.stats.max_hp || 1}
            />
          </div>

          {/* Opponent Creature */}
          <div className="row-start-1 col-start-2 flex items-start justify-end">
            <img 
              src={`/creatures/${opponentCreature?.meta.creature_type || 'unknown'}_front.png`} 
              alt={opponentCreature?.display_name || "Opponent Creature"} 
              className="w-48 h-48 object-contain"
            />
          </div>

          {/* Player Creature */}
          <div className="row-start-2 col-start-1 flex items-end justify-start">
            <img 
              src={`/creatures/${playerCreature?.meta.creature_type || 'unknown'}_back.png`} 
              alt={playerCreature?.display_name || "Player Creature"} 
              className="w-48 h-48 object-contain"
            />
          </div>

          {/* Player Creature Status */}
          <div className="row-start-2 col-start-2 flex items-end justify-end">
            <CreatureCard
              uid={playerCreature?.uid || ""}
              name={playerCreature?.display_name || "Unknown"}
              image={`/creatures/${playerCreature?.meta.creature_type || 'unknown'}_front.png`}
              hp={playerCreature?.stats.hp || 0}
              maxHp={playerCreature?.stats.max_hp || 1}
            />
          </div>
        </div>

        {/* User Interface */}
        <div className="h-1/3 bg-gray-200 p-4">
          <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
            {playerCreature?.collections?.skills?.slice(0, 3).map((skill: Skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Base Damage: ${skill.stats.base_damage}`}
              />
            ))}
            {availableButtonSlugs.includes("return-to-main-menu") && (
              <Button onClick={() => emitButtonClick("return-to-main-menu")}>
                <ArrowLeft className="mr-2 h-4 w-4" /> Return to Main Menu
              </Button>
            )}
          </div>
        </div>

        {/* Player and Opponent Cards (hidden, but included for completeness) */}
        <div className="hidden">
          <PlayerCard
            uid={player?.uid || ""}
            playerName={player?.display_name || "Unknown Player"}
            imageUrl={`/players/${player?.uid || 'unknown'}.png`}
          />
          <PlayerCard
            uid={opponent?.uid || ""}
            playerName={opponent?.display_name || "Unknown Opponent"}
            imageUrl={`/players/${opponent?.uid || 'unknown'}.png`}
          />
        </div>
      </div>
    </div>
  );
}
