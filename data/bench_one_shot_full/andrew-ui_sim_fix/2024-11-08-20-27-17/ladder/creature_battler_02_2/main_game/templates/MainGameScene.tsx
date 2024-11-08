import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react';
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
    [key: string]: any;
  };
}

interface Creature {
  __type: "Creature";
  uid: string;
  display_name: string;
  description: string;
  meta: {
    prototype_id: string;
  };
  stats: {
    hp: number;
    max_hp: number;
    attack: number;
    defense: number;
    speed: number;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
  __type: "Player";
  uid: string;
  display_name: string;
  meta: {
    prototype_id: string;
  };
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

  const { player, bot, player_creature, bot_creature } = props.data?.entities || {};

  if (!player || !bot || !player_creature || !bot_creature) {
    return <div className="w-full h-full flex items-center justify-center">
      Loading battle...
    </div>;
  }

  const availableSkills = player_creature.collections.skills.filter(skill => 
    availableButtonSlugs.includes(skill.uid)
  );

  const handleSkillClick = (skillUid: string) => {
    if (availableButtonSlugs.includes(skillUid)) {
      emitButtonClick(skillUid);
    }
  };

  return (
    <div className="w-full h-full flex flex-col">
      {/* HUD */}
      <nav className="h-[10%] bg-slate-800 flex items-center justify-between px-4">
        <PlayerCard
          uid={player.uid}
          name={player.display_name}
          imageUrl={`/players/${player.meta.prototype_id}.png`}
          className="h-full w-auto"
        />
        <PlayerCard
          uid={bot.uid}
          name={bot.display_name}
          imageUrl={`/players/${bot.meta.prototype_id}.png`}
          className="h-full w-auto"
        />
      </nav>

      {/* Battlefield */}
      <div className="h-[60%] flex justify-between items-center px-12 bg-slate-700">
        <div className="relative">
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            currentHp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            imageUrl={`/creatures/${player_creature.meta.prototype_id}.png`}
            className="transform hover:scale-105 transition-transform"
          />
          <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 bg-blue-500 text-white px-3 py-1 rounded-full">
            Player
          </div>
        </div>

        <Zap className="h-12 w-12 text-yellow-400 animate-pulse" />

        <div className="relative">
          <CreatureCard
            uid={bot_creature.uid}
            name={bot_creature.display_name}
            currentHp={bot_creature.stats.hp}
            maxHp={bot_creature.stats.max_hp}
            imageUrl={`/creatures/${bot_creature.meta.prototype_id}.png`}
            className="transform hover:scale-105 transition-transform"
          />
          <div className="absolute -bottom-6 left-1/2 -translate-x-1/2 bg-red-500 text-white px-3 py-1 rounded-full">
            Opponent
          </div>
        </div>
      </div>

      {/* Controls */}
      <div className="h-[30%] bg-slate-800 p-4">
        {availableSkills.length > 0 ? (
          <div className="grid grid-cols-2 gap-4 h-full">
            {availableSkills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={skill.stats}
                className="h-full text-lg cursor-pointer"
                variant="secondary"
                onClick={() => handleSkillClick(skill.uid)}
              />
            ))}
          </div>
        ) : (
          <div className="flex items-center justify-center h-full text-gray-400">
            No actions available
          </div>
        )}
      </div>
    </div>
  );
}
