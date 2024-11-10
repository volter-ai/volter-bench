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
    damage: number;
  };
  meta: {
    prototype_id: string;
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
  meta: {
    prototype_id: string;
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

  const { player, bot, player_creature, bot_creature } = props.data.entities;

  const getImageUrl = (prototypeId: string) => `/assets/${prototypeId}.png`;

  const handleSkillClick = (skillSlug: string) => {
    if (availableButtonSlugs.includes(skillSlug)) {
      emitButtonClick(skillSlug);
    }
  };

  return (
    <div className="h-screen w-screen flex flex-col bg-background">
      <nav className="w-full h-20 bg-primary/10 flex items-center justify-between px-6 border-b">
        {player && (
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={getImageUrl(player.meta.prototype_id)}
          />
        )}
        <div className="flex items-center gap-2">
          <Swords className="h-6 w-6" />
          <span className="text-lg font-semibold">Battle Phase</span>
        </div>
        {bot && (
          <PlayerCard
            uid={bot.uid}
            name={bot.display_name}
            imageUrl={getImageUrl(bot.meta.prototype_id)}
          />
        )}
      </nav>

      <main className="flex-grow flex justify-between items-center px-12">
        {player_creature && (
          <div className="flex flex-col items-center gap-4">
            <span className="text-lg font-bold text-primary">Your Creature</span>
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              hp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
              imageUrl={getImageUrl(player_creature.meta.prototype_id)}
            />
          </div>
        )}

        {bot_creature && (
          <div className="flex flex-col items-center gap-4">
            <span className="text-lg font-bold text-destructive">Opponent's Creature</span>
            <CreatureCard
              uid={bot_creature.uid}
              name={bot_creature.display_name}
              hp={bot_creature.stats.hp}
              maxHp={bot_creature.stats.max_hp}
              imageUrl={getImageUrl(bot_creature.meta.prototype_id)}
            />
          </div>
        )}
      </main>

      <footer className="h-48 bg-primary/5 border-t p-4">
        <div 
          className="grid grid-cols-4 gap-4 h-full" 
          role="group" 
          aria-label="Available Skills"
        >
          {player_creature?.collections.skills.map((skill) => {
            const buttonSlug = `skill_${skill.uid}`;
            return (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.damage}`}
                disabled={!availableButtonSlugs.includes(buttonSlug)}
                onClick={() => handleSkillClick(buttonSlug)}
              />
            );
          })}
        </div>
      </footer>
    </div>
  );
}
