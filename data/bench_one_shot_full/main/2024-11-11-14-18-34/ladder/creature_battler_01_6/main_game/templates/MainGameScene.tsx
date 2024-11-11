import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Loader2 } from 'lucide-react';
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

  const { player, bot, player_creature, bot_creature } = props.data?.entities || {};

  if (!player || !bot || !player_creature || !bot_creature) {
    return (
      <div className="h-screen w-full aspect-[16/9] flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  const handleSkillClick = (skillUid: string) => {
    if (availableButtonSlugs.includes(skillUid)) {
      emitButtonClick(skillUid);
    }
  };

  return (
    <div className="h-screen w-full aspect-[16/9] flex flex-col bg-background">
      {/* HUD */}
      <nav className="w-full p-4 bg-secondary/10 flex justify-between items-center">
        <div className="flex items-center gap-4">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={`/players/${player.uid}.png`}
          />
          <Sword className="h-5 w-5" />
        </div>
        <div className="flex items-center gap-4">
          <Shield className="h-5 w-5" />
          <PlayerCard
            uid={bot.uid}
            name={bot.display_name}
            imageUrl={`/players/${bot.uid}.png`}
          />
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center px-16 py-8">
        <div className="relative">
          <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-sm font-bold">
            Your Creature
          </span>
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            hp={player_creature.stats?.hp ?? 0}
            maxHp={player_creature.stats?.max_hp ?? 0}
            imageUrl={`/creatures/${player_creature.uid}.png`}
          />
        </div>

        <div className="relative">
          <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-sm font-bold">
            Opponent's Creature
          </span>
          <CreatureCard
            uid={bot_creature.uid}
            name={bot_creature.display_name}
            hp={bot_creature.stats?.hp ?? 0}
            maxHp={bot_creature.stats?.max_hp ?? 0}
            imageUrl={`/creatures/${bot_creature.uid}.png`}
          />
        </div>
      </div>

      {/* UI Region */}
      <div className="min-h-[200px] bg-secondary/10 p-6">
        <div className="grid grid-cols-3 gap-4">
          {player_creature.collections?.skills?.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description ?? ""}
              stats={`Damage: ${skill.stats?.damage ?? 0}`}
              disabled={!availableButtonSlugs.includes(skill.uid)}
              onClick={() => handleSkillClick(skill.uid)}
            />
          )) ?? (
            <div className="col-span-3 text-center text-muted-foreground">
              No skills available
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
