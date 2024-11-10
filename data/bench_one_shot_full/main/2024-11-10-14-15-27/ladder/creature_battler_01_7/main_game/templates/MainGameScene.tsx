import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
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

  const { player, bot, player_creature, bot_creature } = props.data.entities;

  if (!player_creature || !bot_creature || !player || !bot) {
    return <div className="text-center p-4">Loading game...</div>;
  }

  return (
    <div className="w-full h-full aspect-video bg-background flex flex-col">
      {/* Top HUD */}
      <nav className="w-full bg-secondary p-2 flex justify-between items-center">
        <PlayerCard
          uid={player.uid}
          name={player.display_name}
          imageUrl="/images/player-avatar.png"
          className="w-[200px] h-[60px]"
        />
        <div className="flex items-center gap-2">
          <Sword className="w-4 h-4" />
          <Shield className="w-4 h-4" />
        </div>
        <PlayerCard
          uid={bot.uid}
          name={bot.display_name}
          imageUrl="/images/bot-avatar.png"
          className="w-[200px] h-[60px]"
        />
      </nav>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center px-8 py-4">
        <div className="flex flex-col items-center gap-4">
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            imageUrl={`/images/creatures/${player_creature.meta?.prototype_id || 'default'}.png`}
          />
          <span className="text-sm font-bold">Your Creature</span>
        </div>

        <div className="flex flex-col items-center gap-4">
          <CreatureCard
            uid={bot_creature.uid}
            name={bot_creature.display_name}
            hp={bot_creature.stats.hp}
            maxHp={bot_creature.stats.max_hp}
            imageUrl={`/images/creatures/${bot_creature.meta?.prototype_id || 'default'}.png`}
          />
          <span className="text-sm font-bold">Opponent's Creature</span>
        </div>
      </div>

      {/* Bottom UI */}
      <div className="bg-secondary/50 p-4">
        <div className="flex flex-wrap gap-2 justify-center">
          {player_creature.collections.skills?.map((skill) => (
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
