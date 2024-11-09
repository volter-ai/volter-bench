import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";

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
  description: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  collections: {
    skills: Skill[];
  };
  meta: {
    image_front?: string;
    image_back?: string;
  };
}

interface Player {
  __type: "Player";
  uid: string;
  display_name: string;
  collections: {
    creatures: Creature[];
  };
  meta: {
    image_url?: string;
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
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const { player, opponent, player_creature, opponent_creature } = props.data.entities;

  if (!player_creature || !opponent_creature || !player || !opponent) {
    return <div className="w-full h-full flex items-center justify-center">
      Loading battle...
    </div>;
  }

  return (
    <div className="h-screen w-screen flex flex-col">
      {/* Battlefield Area (upper 2/3) */}
      <div className="h-2/3 grid grid-cols-2 gap-4 p-4 bg-gradient-to-b from-sky-100 to-sky-300">
        {/* Top Left - Opponent Status */}
        <div className="flex flex-col gap-4">
          <PlayerCard
            uid={opponent.uid}
            name={opponent.display_name}
            imageUrl={opponent.meta.image_url || "/default_opponent.png"}
          />
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            hp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
            imageUrl={opponent_creature.meta.image_front || `/creatures/default_front.png`}
          />
        </div>

        {/* Top Right - Opponent Creature */}
        <div className="flex justify-end items-start">
          <div className="relative">
            <div className="absolute bottom-0 w-32 h-8 bg-black/20 rounded-full blur-sm" />
            <img
              src={opponent_creature.meta.image_front || `/creatures/default_front.png`}
              alt={opponent_creature.display_name}
              className="w-48 h-48 object-contain"
            />
          </div>
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex justify-start items-end">
          <div className="relative">
            <div className="absolute bottom-0 w-32 h-8 bg-black/20 rounded-full blur-sm" />
            <img
              src={player_creature.meta.image_back || `/creatures/default_back.png`}
              alt={player_creature.display_name}
              className="w-48 h-48 object-contain"
            />
          </div>
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex flex-col gap-4 items-end">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={player.meta.image_url || "/default_player.png"}
          />
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            imageUrl={player_creature.meta.image_front || `/creatures/default_front.png`}
          />
        </div>
      </div>

      {/* UI Area (lower 1/3) */}
      <div className="h-1/3 grid grid-cols-2 gap-4 p-4 bg-white/80">
        {player_creature.collections.skills.map((skill) => (
          <SkillButton
            key={skill.uid}
            uid={skill.uid}
            skillName={skill.display_name}
            description={skill.description}
            damage={skill.stats.base_damage}
            type={skill.meta.skill_type}
          />
        ))}
      </div>
    </div>
  );
}
