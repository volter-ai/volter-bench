import { useCurrentButtons } from "@/lib/useChoices";
import { Shield, Swords } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  __type: "Skill";
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
}

interface Creature {
  __type: "Creature";
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
    attack: number;
    defense: number;
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

  if (!props.data?.entities) {
    return <div className="w-full h-full aspect-video bg-slate-900" />;
  }

  const { player, opponent, player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="w-full h-full aspect-video bg-slate-900 text-white">
      <div className="grid grid-rows-6 h-full">
        {/* HUD */}
        <div className="row-span-1 bg-slate-800 p-4 flex justify-between items-center">
          {player && player.__type === "Player" && (
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl="/player-avatar.png"
            />
          )}
          
          {player_creature && player_creature.__type === "Creature" && (
            <div className="flex gap-4">
              <div className="flex items-center gap-2">
                <Swords className="w-5 h-5" />
                <span>{player_creature.stats.attack}</span>
              </div>
              <div className="flex items-center gap-2">
                <Shield className="w-5 h-5" />
                <span>{player_creature.stats.defense}</span>
              </div>
            </div>
          )}
        </div>

        {/* Battlefield */}
        <div className="row-span-3 p-8 flex justify-between items-center">
          {player_creature && player_creature.__type === "Creature" && (
            <div className="relative">
              <CreatureCard
                uid={player_creature.uid}
                name={player_creature.display_name}
                currentHp={player_creature.stats.hp}
                maxHp={player_creature.stats.max_hp}
                imageUrl="/creature-placeholder.png"
              />
              <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 bg-blue-500 px-3 py-1 rounded-full text-sm">
                Player
              </div>
            </div>
          )}

          {opponent_creature && opponent_creature.__type === "Creature" && (
            <div className="relative">
              <CreatureCard
                uid={opponent_creature.uid}
                name={opponent_creature.display_name}
                currentHp={opponent_creature.stats.hp}
                maxHp={opponent_creature.stats.max_hp}
                imageUrl="/creature-placeholder.png"
              />
              <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 bg-red-500 px-3 py-1 rounded-full text-sm">
                Opponent
              </div>
            </div>
          )}
        </div>

        {/* UI Area */}
        <div className="row-span-2 bg-slate-800 p-6">
          <div className="grid grid-cols-2 gap-4">
            {player_creature?.collections.skills
              ?.filter(skill => skill.__type === "Skill")
              ?.map((skill) => (
                <SkillButton
                  key={skill.uid}
                  uid={skill.uid}
                  name={skill.display_name}
                  description={skill.description}
                  damage={skill.stats.base_damage}
                />
              ))}
          </div>
        </div>
      </div>
    </div>
  );
}
