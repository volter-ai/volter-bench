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

  const { player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="w-full h-full flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-7xl aspect-video bg-white shadow-lg rounded-lg overflow-hidden">
        <div className="h-2/3 grid grid-cols-2 grid-rows-2 p-4 gap-4">
          {/* Opponent Creature Status */}
          <div className="flex items-start justify-start">
            <CreatureCard
              uid={opponent_creature?.uid ?? ""}
              name={opponent_creature?.display_name ?? "Unknown"}
              image="/placeholder-opponent.png"
              hp={opponent_creature?.stats.hp ?? 0}
              maxHp={opponent_creature?.stats.max_hp ?? 1}
            />
          </div>

          {/* Opponent Creature */}
          <div className="flex items-center justify-center">
            <img
              src="/placeholder-opponent-front.png"
              alt={opponent_creature?.display_name ?? "Opponent Creature"}
              className="max-h-full max-w-full object-contain"
            />
          </div>

          {/* Player Creature */}
          <div className="flex items-center justify-center">
            <img
              src="/placeholder-player-back.png"
              alt={player_creature?.display_name ?? "Player Creature"}
              className="max-h-full max-w-full object-contain"
            />
          </div>

          {/* Player Creature Status */}
          <div className="flex items-end justify-end">
            <CreatureCard
              uid={player_creature?.uid ?? ""}
              name={player_creature?.display_name ?? "Unknown"}
              image="/placeholder-player.png"
              hp={player_creature?.stats.hp ?? 0}
              maxHp={player_creature?.stats.max_hp ?? 1}
            />
          </div>
        </div>

        {/* User Interface */}
        <div className="h-1/3 p-4">
          <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
            {player_creature?.collections.skills.map((skill, index) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.base_damage}`}
                onClick={() => emitButtonClick(skill.uid)}
                disabled={!availableButtonSlugs.includes(skill.uid)}
                className="w-full h-full text-lg"
              >
                <div className="flex items-center justify-center">
                  {index === 0 && <Sword className="mr-2" />}
                  {index === 1 && <Shield className="mr-2" />}
                  {index === 2 && <Zap className="mr-2" />}
                  {index === 3 && <Heart className="mr-2" />}
                  {skill.display_name}
                </div>
              </SkillButton>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
