import { useCurrentButtons } from "@/lib/useChoices.ts";
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
  meta: {
    prototype_id: string;
  };
}

interface Player {
  __type: "Player";
  uid: string;
  display_name: string;
  collections: {
    creatures: Creature[];
  };
  meta: {
    prototype_id: string;
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
    return <div className="h-screen w-full flex items-center justify-center">Loading...</div>;
  }

  const { player, bot, player_creature, bot_creature } = props.data.entities;

  const handleSkillClick = (skillUid: string) => {
    if (!skillUid || !availableButtonSlugs) return;
    
    const buttonSlug = availableButtonSlugs.find(slug => slug === skillUid);
    if (buttonSlug) {
      emitButtonClick(buttonSlug);
    }
  };

  const renderSkillButtons = () => {
    if (!player_creature?.collections?.skills) return null;

    return player_creature.collections.skills
      .filter(skill => skill.__type === "Skill")
      .map((skill) => (
        <SkillButton
          key={skill.uid}
          uid={skill.uid}
          name={skill.display_name}
          description={skill.description}
          stats={`Damage: ${skill.stats.damage}`}
          disabled={!availableButtonSlugs.includes(skill.uid)}
          onClick={() => handleSkillClick(skill.uid)}
        />
      ));
  };

  return (
    <div className="flex flex-col h-screen w-full bg-background">
      <nav className="h-16 border-b flex items-center justify-between px-4 bg-card">
        <div className="flex items-center gap-2">
          <Shield className="h-6 w-6" />
          <span className="font-bold">Battle Arena</span>
        </div>
        <div className="flex gap-4">
          {player && player.__type === "Player" && (
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl={`/avatars/${player.meta.prototype_id || 'default'}`}
            />
          )}
          {bot && bot.__type === "Player" && (
            <PlayerCard
              uid={bot.uid}
              name={bot.display_name}
              imageUrl={`/avatars/${bot.meta.prototype_id || 'default'}`}
            />
          )}
        </div>
      </nav>

      <main className="flex-grow flex flex-col">
        <div className="flex-grow flex items-center justify-between px-8 bg-muted/20">
          <div className="flex flex-col items-center gap-4">
            <div className="text-sm font-medium">Player's Creature</div>
            {player_creature && player_creature.__type === "Creature" && (
              <CreatureCard
                uid={player_creature.uid}
                name={player_creature.display_name}
                hp={player_creature.stats.hp}
                maxHp={player_creature.stats.max_hp}
                imageUrl={`/creatures/${player_creature.meta.prototype_id || 'default'}`}
              />
            )}
          </div>

          <Swords className="h-8 w-8 text-muted-foreground" />

          <div className="flex flex-col items-center gap-4">
            <div className="text-sm font-medium">Opponent's Creature</div>
            {bot_creature && bot_creature.__type === "Creature" && (
              <CreatureCard
                uid={bot_creature.uid}
                name={bot_creature.display_name}
                hp={bot_creature.stats.hp}
                maxHp={bot_creature.stats.max_hp}
                imageUrl={`/creatures/${bot_creature.meta.prototype_id || 'default'}`}
              />
            )}
          </div>
        </div>

        <div className="min-h-[200px] border-t bg-card p-6">
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            {renderSkillButtons()}
          </div>
        </div>
      </main>
    </div>
  );
}
