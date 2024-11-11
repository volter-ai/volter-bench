import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";

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
}

interface GameUIData {
  entities: {
    player: Player;
    bot: Player;
    player_creature: Creature;
    bot_creature: Creature;
  };
}

function isCreature(entity: any): entity is Creature {
  return entity?.__type === "Creature";
}

function isSkill(entity: any): entity is Skill {
  return entity?.__type === "Skill";
}

function isPlayer(entity: any): entity is Player {
  return entity?.__type === "Player";
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const { player, bot, player_creature, bot_creature } = props.data.entities;

  if (!isPlayer(player) || !isPlayer(bot) || !isCreature(player_creature) || !isCreature(bot_creature)) {
    return <div>Invalid game state</div>;
  }

  return (
    <div className="w-full h-full flex flex-col bg-background">
      {/* HUD */}
      <div className="h-16 bg-secondary flex items-center justify-between px-4 border-b">
        <div className="flex items-center gap-4">
          <Shield className="h-6 w-6" />
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={`/players/default.png`}
          />
        </div>
        <div className="flex items-center gap-4">
          <PlayerCard
            uid={bot.uid}
            name={bot.display_name}
            imageUrl={`/players/default.png`}
          />
          <Swords className="h-6 w-6" />
        </div>
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-between px-8 py-4">
        <div className="flex flex-col items-center gap-2">
          <span className="text-sm font-semibold">Your Creature</span>
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            imageUrl={`/creatures/${player_creature.display_name.toLowerCase()}.png`}
          />
        </div>

        <div className="flex flex-col items-center gap-2">
          <span className="text-sm font-semibold">Opponent's Creature</span>
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
      <div className="h-48 bg-secondary/50 border-t p-4">
        <div className="grid grid-cols-3 gap-4">
          {player_creature.collections.skills.map((skill) => {
            if (!isSkill(skill)) return null;
            
            return (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.damage}`}
                disabled={!availableButtonSlugs.includes(skill.uid)}
                onClick={() => emitButtonClick(skill.uid)}
              />
            );
          })}
        </div>
      </div>
    </div>
  );
}
