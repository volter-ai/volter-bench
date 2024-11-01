import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

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

  const { player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Creature Status */}
        <div className="flex justify-start items-start">
          <CreatureCard
            uid={opponent_creature?.uid ?? ""}
            name={opponent_creature?.display_name ?? "Unknown"}
            image={`/creatures/${opponent_creature?.meta.prototype_id ?? "unknown"}_front.png`}
            hp={opponent_creature?.stats.hp ?? 0}
            maxHp={opponent_creature?.stats.max_hp ?? 1}
          />
        </div>

        {/* Opponent Creature */}
        <div className="flex justify-end items-start">
          <img
            src={`/creatures/${opponent_creature?.meta.prototype_id ?? "unknown"}_front.png`}
            alt={opponent_creature?.display_name ?? "Opponent Creature"}
            className="w-32 h-32 object-contain"
          />
        </div>

        {/* Player Creature */}
        <div className="flex justify-start items-end">
          <img
            src={`/creatures/${player_creature?.meta.prototype_id ?? "unknown"}_back.png`}
            alt={player_creature?.display_name ?? "Player Creature"}
            className="w-32 h-32 object-contain"
          />
        </div>

        {/* Player Creature Status */}
        <div className="flex justify-end items-end">
          <CreatureCard
            uid={player_creature?.uid ?? ""}
            name={player_creature?.display_name ?? "Unknown"}
            image={`/creatures/${player_creature?.meta.prototype_id ?? "unknown"}_front.png`}
            hp={player_creature?.stats.hp ?? 0}
            maxHp={player_creature?.stats.max_hp ?? 1}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4 flex items-center justify-center">
        <div className="w-full max-w-2xl">
          <div className="grid grid-cols-2 gap-4">
            {availableButtonSlugs.length > 0 ? (
              availableButtonSlugs.map((slug) => {
                const skill = player_creature?.collections.skills.find(s => s.uid === slug);
                return (
                  <SkillButton
                    key={slug}
                    uid={slug}
                    skillName={skill?.display_name ?? "Unknown Skill"}
                    description={skill?.description ?? ""}
                    stats={`Damage: ${skill?.stats.base_damage ?? 0}`}
                    onClick={() => emitButtonClick(slug)}
                  />
                );
              })
            ) : (
              <>
                <SkillButton
                  uid="default_attack"
                  skillName="Attack"
                  description="Basic attack"
                  stats="Damage: 10"
                  onClick={() => emitButtonClick("default_attack")}
                />
                <SkillButton
                  uid="default_defend"
                  skillName="Defend"
                  description="Defensive stance"
                  stats="Defense: +5"
                  onClick={() => emitButtonClick("default_defend")}
                />
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
