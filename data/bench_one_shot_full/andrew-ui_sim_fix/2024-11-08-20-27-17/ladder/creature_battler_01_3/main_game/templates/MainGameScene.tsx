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

  // Get image URLs from metadata (fallback to placeholder if not present)
  const getImageUrl = (entity: { meta?: { image_url?: string } }) => 
    entity?.meta?.image_url || "/placeholder.png";

  return (
    <div className="flex flex-col h-screen w-full bg-background">
      {/* HUD */}
      <div className="h-16 bg-primary/10 flex items-center justify-between px-4 border-b">
        <div className="flex items-center gap-4">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={getImageUrl(player)}
          />
        </div>
        <div className="flex items-center gap-4">
          <PlayerCard
            uid={bot.uid}
            name={bot.display_name}
            imageUrl={getImageUrl(bot)}
          />
        </div>
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-between px-8">
        {player_creature && (
          <div className="flex flex-col items-center gap-2">
            <span className="text-sm font-bold text-primary">Your Creature</span>
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              hp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
              imageUrl={getImageUrl(player_creature)}
            />
          </div>
        )}

        {bot_creature && (
          <div className="flex flex-col items-center gap-2">
            <span className="text-sm font-bold text-destructive">Opponent's Creature</span>
            <CreatureCard
              uid={bot_creature.uid}
              name={bot_creature.display_name}
              hp={bot_creature.stats.hp}
              maxHp={bot_creature.stats.max_hp}
              imageUrl={getImageUrl(bot_creature)}
            />
          </div>
        )}
      </div>

      {/* Bottom UI */}
      <div className="h-1/3 bg-secondary/10 p-4 border-t">
        <div className="grid grid-cols-2 gap-4 h-full">
          {player_creature?.collections.skills?.length > 0 ? (
            player_creature.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.damage}`}
                disabled={!availableButtonSlugs.includes(skill.uid)}
              />
            ))
          ) : (
            <div className="col-span-2 flex items-center justify-center text-muted-foreground">
              No skills available
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
