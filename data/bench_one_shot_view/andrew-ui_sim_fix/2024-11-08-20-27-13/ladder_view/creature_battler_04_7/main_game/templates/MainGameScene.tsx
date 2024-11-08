import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  __type: "Skill";
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
  meta: {
    skill_type: string;
  };
}

interface Creature {
  __type: "Creature";
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

  if (!playerCreature || !opponentCreature) {
    return <div className="text-center p-4">Loading battle...</div>;
  }

  return (
    <div className="h-screen w-screen flex flex-col">
      {/* Battlefield Area (upper 2/3) */}
      <div className="h-2/3 grid grid-cols-2 gap-4 p-8 bg-gradient-to-b from-blue-100 to-blue-200">
        {/* Top Left - Opponent Status */}
        <div className="flex justify-start items-start">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
            className="transform scale-75"
          />
        </div>

        {/* Top Right - Opponent Creature */}
        <div className="flex justify-end items-start">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
            className="transform scale-100"
          />
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex justify-start items-end">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            className="transform scale-100"
          />
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex justify-end items-end">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            className="transform scale-75"
          />
        </div>
      </div>

      {/* UI Area (lower 1/3) */}
      <div className="h-1/3 grid grid-cols-2 gap-4 p-4 bg-white/80">
        {playerCreature.collections.skills.map((skill) => (
          <SkillButton
            key={skill.uid}
            uid={skill.uid}
            skillName={skill.display_name}
            description={skill.description}
            damage={skill.stats.base_damage}
            type={skill.meta.skill_type}
            className="h-24 text-lg"
          />
        ))}
      </div>
    </div>
  );
}
