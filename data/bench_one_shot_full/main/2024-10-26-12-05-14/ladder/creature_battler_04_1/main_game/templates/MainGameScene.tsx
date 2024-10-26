import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react';
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

interface Player {
  __type: "Player";
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
  meta: {
    battle_over: boolean;
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
        {/* Top-left: Opponent Status */}
        <div className="flex items-start justify-start">
          <div className="text-lg font-bold">{opponent_creature?.display_name}</div>
        </div>

        {/* Top-right: Opponent Creature */}
        <div className="flex items-start justify-end">
          {opponent_creature && (
            <CreatureCard
              uid={opponent_creature.uid}
              name={opponent_creature.display_name}
              image="/placeholder-opponent.png"
              hp={opponent_creature.stats.hp}
              maxHp={opponent_creature.stats.max_hp}
            />
          )}
        </div>

        {/* Bottom-left: Player Creature */}
        <div className="flex items-end justify-start">
          {player_creature && (
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              image="/placeholder-player.png"
              hp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
            />
          )}
        </div>

        {/* Bottom-right: Player Status */}
        <div className="flex items-end justify-end">
          <div className="text-lg font-bold">{player_creature?.display_name}</div>
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        {availableButtonSlugs.length > 0 && player_creature?.collections.skills ? (
          <div className="grid grid-cols-2 gap-4">
            {player_creature.collections.skills.map((skill: Skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.base_damage}`}
                onClick={() => emitButtonClick(skill.uid)}
              >
                <div className="flex items-center">
                  {skill.meta.skill_type === "normal" && <Sword className="mr-2" />}
                  {skill.meta.skill_type === "water" && <Shield className="mr-2" />}
                  {skill.meta.skill_type === "fire" && <Zap className="mr-2" />}
                  {skill.display_name}
                </div>
              </SkillButton>
            ))}
          </div>
        ) : (
          <div className="flex items-center justify-center h-full">
            <p className="text-xl font-semibold">Waiting for opponent...</p>
          </div>
        )}
      </div>
    </div>
  );
}
