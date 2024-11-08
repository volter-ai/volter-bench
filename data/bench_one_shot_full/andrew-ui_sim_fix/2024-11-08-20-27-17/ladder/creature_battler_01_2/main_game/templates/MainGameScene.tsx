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
  description: string;
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
      Loading...
    </div>;
  }

  return (
    <div className="w-full h-full flex flex-col bg-background">
      {/* HUD */}
      <nav className="w-full h-16 bg-primary/10 flex items-center justify-between px-4 border-b">
        <div className="flex items-center gap-2">
          <Sword className="w-6 h-6" />
          <span className="font-bold">Battle Scene</span>
        </div>
        <div className="flex gap-4">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={`/players/player.png`}
          />
          <PlayerCard
            uid={bot.uid}
            name={bot.display_name}
            imageUrl={`/players/bot.png`}
          />
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-between px-8 py-4">
        <div className="flex flex-col items-center gap-4">
          <div className="text-lg font-bold flex items-center gap-2">
            <Shield className="w-5 h-5" />
            Player's Creature
          </div>
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            imageUrl={`/creatures/${player_creature.display_name.toLowerCase()}.png`}
          />
        </div>

        <div className="flex flex-col items-center gap-4">
          <div className="text-lg font-bold flex items-center gap-2">
            <Sword className="w-5 h-5" />
            Opponent's Creature
          </div>
          <CreatureCard
            uid={bot_creature.uid}
            name={bot_creature.display_name}
            hp={bot_creature.stats.hp}
            maxHp={bot_creature.stats.max_hp}
            imageUrl={`/creatures/${bot_creature.display_name.toLowerCase()}.png`}
          />
        </div>
      </div>

      {/* UI Area */}
      <div className="h-48 bg-primary/5 border-t p-4">
        <div className="grid grid-cols-4 gap-4 max-w-2xl mx-auto">
          {player_creature.collections.skills.map((skill) => (
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
