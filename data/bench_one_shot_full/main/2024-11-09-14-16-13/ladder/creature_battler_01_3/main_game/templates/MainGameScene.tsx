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

  if (!player || !bot || !player_creature || !bot_creature) {
    return <div className="h-screen w-full flex items-center justify-center">
      Loading battle...
    </div>;
  }

  // Derive image URLs from prototype IDs (assuming this is how we handle images)
  const getCreatureImageUrl = (creature: Creature) => 
    `/assets/creatures/${creature.meta?.prototype_id || 'default'}.png`;
  
  const getPlayerImageUrl = (player: Player) =>
    `/assets/players/${player.meta?.prototype_id || 'default'}.png`;

  return (
    <div className="h-screen w-full flex flex-col bg-background">
      {/* HUD */}
      <nav className="h-16 bg-primary/10 flex items-center justify-between px-4">
        <div className="flex items-center gap-4">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={getPlayerImageUrl(player)}
          />
        </div>
        <div className="flex items-center gap-4">
          <PlayerCard
            uid={bot.uid}
            name={bot.display_name}
            imageUrl={getPlayerImageUrl(bot)}
          />
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-between px-8">
        <div className="relative">
          <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-blue-500 text-white px-2 py-1 rounded">
            Player
          </div>
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            imageUrl={getCreatureImageUrl(player_creature)}
          />
        </div>

        <div className="relative">
          <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-red-500 text-white px-2 py-1 rounded">
            Opponent
          </div>
          <CreatureCard
            uid={bot_creature.uid}
            name={bot_creature.display_name}
            hp={bot_creature.stats.hp}
            maxHp={bot_creature.stats.max_hp}
            imageUrl={getCreatureImageUrl(bot_creature)}
          />
        </div>
      </div>

      {/* UI Region */}
      <div className="h-1/3 bg-secondary/10 p-4">
        <div className="grid grid-cols-4 gap-4">
          {player_creature.collections.skills?.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          )) ?? (
            <div className="col-span-4 text-center text-muted-foreground">
              No skills available
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
