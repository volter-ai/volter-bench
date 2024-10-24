import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Sword, RefreshCw } from 'lucide-react';

interface Skill {
  __type: "Skill";
  stats: { base_damage: number };
  meta: { skill_type: string; is_physical: boolean };
  uid: string;
  display_name: string;
  description: string;
}

interface Creature {
  __type: "Creature";
  stats: { hp: number; max_hp: number };
  meta: { creature_type: string };
  uid: string;
  display_name: string;
  description: string;
  collections: { skills: Skill[] };
}

interface Player {
  __type: "Player";
  entities: { active_creature: Creature };
  uid: string;
  display_name: string;
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const player = props.data.entities.player;
  const opponent = props.data.entities.opponent;

  return (
    <div className="w-full h-full bg-gradient-to-b from-blue-200 to-green-200 flex flex-col">
      {/* Battlefield */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Status */}
        <div className="flex items-start justify-start">
          <CreatureCard
            uid={opponent.entities.active_creature?.uid || ""}
            name={opponent.entities.active_creature?.display_name || "Unknown"}
            image="/placeholder-opponent.png"
            hp={opponent.entities.active_creature?.stats.hp || 0}
            maxHp={opponent.entities.active_creature?.stats.max_hp || 1}
          />
        </div>

        {/* Opponent Creature */}
        <div className="flex items-start justify-end">
          <img
            src="/placeholder-opponent-creature.png"
            alt="Opponent Creature"
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Player Creature */}
        <div className="flex items-end justify-start">
          <img
            src="/placeholder-player-creature.png"
            alt="Player Creature"
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Player Status */}
        <div className="flex items-end justify-end">
          <CreatureCard
            uid={player.entities.active_creature?.uid || ""}
            name={player.entities.active_creature?.display_name || "Unknown"}
            image="/placeholder-player.png"
            hp={player.entities.active_creature?.stats.hp || 0}
            maxHp={player.entities.active_creature?.stats.max_hp || 1}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-800 p-4">
        <div className="grid grid-cols-2 gap-4">
          {availableButtonSlugs.includes("attack") && (
            <SkillButton
              uid="attack-button"
              skillName="Attack"
              description="Choose an attack"
              stats=""
              onClick={() => emitButtonClick("attack")}
            >
              <Sword className="mr-2" /> Attack
            </SkillButton>
          )}
          {availableButtonSlugs.includes("swap") && (
            <SkillButton
              uid="swap-button"
              skillName="Swap"
              description="Swap your active creature"
              stats=""
              onClick={() => emitButtonClick("swap")}
            >
              <RefreshCw className="mr-2" /> Swap
            </SkillButton>
          )}
          {player.entities.active_creature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
              onClick={() => emitButtonClick(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
