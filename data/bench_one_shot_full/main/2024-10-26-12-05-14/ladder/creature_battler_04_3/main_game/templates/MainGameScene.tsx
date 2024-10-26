import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { X } from 'lucide-react';

interface Creature {
  uid: string;
  display_name: string;
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

interface GameUIData {
  entities: {
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-7xl aspect-video bg-white shadow-lg flex flex-col">
        {/* Battlefield Display */}
        <div className="flex-grow grid grid-cols-2 grid-rows-2 p-4 gap-4">
          {/* Opponent Status */}
          <div className="flex items-start justify-start">
            <CreatureCard
              uid={opponentCreature?.uid || ""}
              name={opponentCreature?.display_name || "Unknown"}
              image={`/images/creatures/${opponentCreature?.meta.creature_type || "unknown"}_front.png`}
              hp={opponentCreature?.stats.hp || 0}
              maxHp={opponentCreature?.stats.max_hp || 1}
            />
          </div>
          
          {/* Opponent Creature */}
          <div className="flex items-end justify-end">
            <img
              src={`/images/creatures/${opponentCreature?.meta.creature_type || "unknown"}_front.png`}
              alt={opponentCreature?.display_name || "Unknown"}
              className="w-48 h-48 object-contain"
            />
          </div>
          
          {/* Player Creature */}
          <div className="flex items-start justify-start">
            <img
              src={`/images/creatures/${playerCreature?.meta.creature_type || "unknown"}_back.png`}
              alt={playerCreature?.display_name || "Unknown"}
              className="w-48 h-48 object-contain"
            />
          </div>
          
          {/* Player Status */}
          <div className="flex items-end justify-end">
            <CreatureCard
              uid={playerCreature?.uid || ""}
              name={playerCreature?.display_name || "Unknown"}
              image={`/images/creatures/${playerCreature?.meta.creature_type || "unknown"}_back.png`}
              hp={playerCreature?.stats.hp || 0}
              maxHp={playerCreature?.stats.max_hp || 1}
            />
          </div>
        </div>

        {/* User Interface */}
        <div className="h-1/3 p-4 bg-gray-200">
          <div className="grid grid-cols-2 gap-4">
            {playerCreature?.collections?.skills?.map((skill: Skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Base Damage: ${skill.stats.base_damage}`}
                onClick={() => emitButtonClick(skill.uid)}
                disabled={!availableButtonSlugs.includes(skill.uid)}
              />
            ))}
            {availableButtonSlugs.includes("quit-game") && (
              <SkillButton
                uid="quit-game"
                skillName="Quit Game"
                description="Exit the current game"
                stats=""
                onClick={() => emitButtonClick("quit-game")}
                className="bg-red-500 hover:bg-red-600"
              >
                <X className="mr-2 h-4 w-4" /> Quit Game
              </SkillButton>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
