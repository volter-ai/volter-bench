import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Shield, Zap } from 'lucide-react';
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";

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
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { enabledUIDs } = useThingInteraction();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield (upper 2/3) */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Top-left: Opponent creature status */}
        <div className="flex justify-start items-start">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            image={`/images/creatures/${opponentCreature.meta.prototype_id}_front.png`}
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
          />
        </div>

        {/* Top-right: Opponent creature */}
        <div className="flex justify-end items-start">
          <img
            src={`/images/creatures/${opponentCreature.meta.prototype_id}_front.png`}
            alt={opponentCreature.display_name}
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Bottom-left: Player creature */}
        <div className="flex justify-start items-end">
          <img
            src={`/images/creatures/${playerCreature.meta.prototype_id}_back.png`}
            alt={playerCreature.display_name}
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Bottom-right: Player creature status */}
        <div className="flex justify-end items-end">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            image={`/images/creatures/${playerCreature.meta.prototype_id}_back.png`}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
        </div>
      </div>

      {/* User Interface (lower 1/3) */}
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 gap-4">
          {playerCreature.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}`}
              disabled={!enabledUIDs.includes(skill.uid)}
            >
              {skill.meta.is_physical ? <Shield className="mr-2" /> : <Zap className="mr-2" />}
              {skill.display_name}
            </SkillButton>
          ))}
        </div>
      </div>
    </div>
  );
}
