import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Sword, Shield, Zap, Heart } from 'lucide-react';

interface Skill {
  __type: "Skill";
  stats: {
    base_damage: number;
  };
  meta: {
    prototype_id: string;
    category: string;
    skill_type: string;
    is_physical: boolean;
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
    sp_attack: number;
    sp_defense: number;
    speed: number;
  };
  meta: {
    prototype_id: string;
    category: string;
    creature_type: string;
  };
  collections: {
    skills: Skill[];
  };
  uid: string;
  display_name: string;
  description: string;
}

interface Player {
  __type: "Player";
  meta: {
    prototype_id: string;
    category: string;
  };
  collections: {
    creatures: Creature[];
  };
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

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Creature Status */}
        <div className="flex justify-start items-start">
          <CreatureCard
            uid={opponentCreature?.uid ?? ""}
            name={opponentCreature?.display_name ?? "Unknown"}
            image={`/images/creatures/${opponentCreature?.meta.prototype_id ?? "unknown"}_front.png`}
            hp={opponentCreature?.stats.hp ?? 0}
            maxHp={opponentCreature?.stats.max_hp ?? 1}
          />
        </div>

        {/* Opponent Creature */}
        <div className="flex justify-end items-start">
          <img
            src={`/images/creatures/${opponentCreature?.meta.prototype_id ?? "unknown"}_front.png`}
            alt={opponentCreature?.display_name ?? "Unknown Creature"}
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Player Creature */}
        <div className="flex justify-start items-end">
          <img
            src={`/images/creatures/${playerCreature?.meta.prototype_id ?? "unknown"}_back.png`}
            alt={playerCreature?.display_name ?? "Unknown Creature"}
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Player Creature Status */}
        <div className="flex justify-end items-end">
          <CreatureCard
            uid={playerCreature?.uid ?? ""}
            name={playerCreature?.display_name ?? "Unknown"}
            image={`/images/creatures/${playerCreature?.meta.prototype_id ?? "unknown"}_back.png`}
            hp={playerCreature?.stats.hp ?? 0}
            maxHp={playerCreature?.stats.max_hp ?? 1}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 gap-4">
          {playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}`}
              disabled={!availableButtonSlugs.includes(skill.uid)}
              onClick={() => emitButtonClick(skill.uid)}
            >
              <div className="flex items-center">
                {skill.meta.skill_type === "normal" && <Sword className="mr-2" />}
                {skill.meta.skill_type === "water" && <Zap className="mr-2" />}
                {skill.meta.skill_type === "fire" && <Heart className="mr-2" />}
                {skill.display_name}
              </div>
            </SkillButton>
          ))}
        </div>
      </div>
    </div>
  );
}
