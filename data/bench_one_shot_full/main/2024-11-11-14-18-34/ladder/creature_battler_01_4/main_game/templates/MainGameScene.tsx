import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword } from 'lucide-react';
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

  return (
    <div className="w-full h-full flex flex-col bg-background min-h-[600px]" style={{ aspectRatio: '16/9' }}>
      {/* HUD */}
      <div className="h-16 bg-primary/10 flex items-center justify-between px-6 border-b">
        {player && (
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl=""
          />
        )}
        <div className="flex items-center gap-2">
          <Sword className="w-5 h-5" />
          <span className="font-bold">Battle Arena</span>
        </div>
        {bot && (
          <PlayerCard
            uid={bot.uid}
            name={bot.display_name}
            imageUrl=""
          />
        )}
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center px-12 py-6">
        {player_creature && (
          <div className="flex flex-col items-center gap-2">
            <span className="text-sm font-semibold text-primary">Your Creature</span>
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              hp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
              imageUrl=""
            />
          </div>
        )}

        {bot_creature && (
          <div className="flex flex-col items-center gap-2">
            <span className="text-sm font-semibold text-destructive">Opponent's Creature</span>
            <CreatureCard
              uid={bot_creature.uid}
              name={bot_creature.display_name}
              hp={bot_creature.stats.hp}
              maxHp={bot_creature.stats.max_hp}
              imageUrl=""
            />
          </div>
        )}
      </div>

      {/* UI Section */}
      <div className="h-48 bg-secondary/10 rounded-t-xl border-t p-4">
        <div className="grid grid-cols-4 gap-4">
          {player_creature?.collections.skills?.map((skill) => (
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
