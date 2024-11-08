import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  __type: "Skill";
  uid: string;
  display_name: string;
  description: string;
  stats: {
    damage: number;
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
}

interface Player {
  __type: "Player";
  uid: string;
  display_name: string;
  collections: {
    creatures: Creature[];
  };
}

interface GameUIData {
  entities: {
    player: Player;
    bot: Player;
    player_creature: Creature;
    bot_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  if (!props.data?.entities) {
    return null;
  }

  const { player_creature, bot_creature } = props.data.entities;

  return (
    <div className="h-full w-full aspect-video relative flex flex-col">
      {/* HUD */}
      <div className="w-full h-16 bg-slate-800 flex items-center justify-between px-6">
        <div className="flex items-center gap-4">
          <Sword className="h-6 w-6 text-white" />
          <span className="text-white font-bold">Battle Arena</span>
        </div>
        <Shield className="h-6 w-6 text-white" />
      </div>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center px-12 bg-slate-100">
        {player_creature && (
          <div className="relative">
            <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-blue-500 text-white px-3 py-1 rounded-full text-sm">
              Player
            </div>
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              hp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
            />
          </div>
        )}

        {bot_creature && (
          <div className="relative">
            <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-red-500 text-white px-3 py-1 rounded-full text-sm">
              Opponent
            </div>
            <CreatureCard
              uid={bot_creature.uid}
              name={bot_creature.display_name}
              hp={bot_creature.stats.hp}
              maxHp={bot_creature.stats.max_hp}
            />
          </div>
        )}
      </div>

      {/* UI Area */}
      <div className="h-2/5 bg-slate-700 p-4 rounded-t-lg">
        <div className="grid grid-cols-4 gap-4">
          {player_creature?.collections?.skills?.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
