import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  __type: "Skill";
  stats: { base_damage: number };
  meta: { skill_type: string };
  uid: string;
  display_name: string;
  description: string;
}

interface Creature {
  __type: "Creature";
  stats: { hp: number; max_hp: number; attack: number; defense: number; speed: number };
  meta: { creature_type: string };
  uid: string;
  display_name: string;
  collections: { skills: Skill[] };
}

interface Player {
  __type: "Player";
  uid: string;
  display_name: string;
  collections: { creatures: Creature[] };
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

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  // Debugging: Log availableButtonSlugs and playerCreature skills
  console.log("Available Button Slugs:", availableButtonSlugs);
  console.log("Player Creature Skills:", playerCreature.collections.skills);

  return (
    <div className="flex flex-col h-full w-full bg-gray-100">
      {/* HUD */}
      <div className="bg-gray-800 text-white p-2">
        <h1 className="text-xl font-bold">Creature Battle</h1>
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-between p-4">
        {playerCreature && (
          <div className="flex flex-col items-center">
            <span className="text-sm text-gray-500">Player</span>
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl="/placeholder-creature.png"
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
            <div className="mt-2 flex space-x-2">
              <Shield className="text-blue-500" />
              <span>{playerCreature.stats.defense}</span>
              <Swords className="text-red-500" />
              <span>{playerCreature.stats.attack}</span>
            </div>
          </div>
        )}
        {opponentCreature && (
          <div className="flex flex-col items-center">
            <span className="text-sm text-gray-500">Opponent</span>
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              imageUrl="/placeholder-opponent.png"
              hp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
            <div className="mt-2 flex space-x-2">
              <Shield className="text-blue-500" />
              <span>{opponentCreature.stats.defense}</span>
              <Swords className="text-red-500" />
              <span>{opponentCreature.stats.attack}</span>
            </div>
          </div>
        )}
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-200">
        {availableButtonSlugs.length > 0 ? (
          <div className="grid grid-cols-2 gap-2">
            {availableButtonSlugs.map((slug) => {
              const skill = playerCreature.collections.skills.find(skill => skill.uid === slug);
              return (
                <SkillButton
                  key={slug}
                  uid={slug}
                  skillName={skill?.display_name || ''}
                  description={skill?.description || ''}
                  stats={`Damage: ${skill?.stats.base_damage || 0}, Type: ${skill?.meta.skill_type || ''}`}
                  onClick={() => emitButtonClick(slug)}
                />
              );
            })}
          </div>
        ) : (
          <p className="text-center text-gray-600">Waiting for your turn...</p>
        )}
      </div>
    </div>
  );
}
