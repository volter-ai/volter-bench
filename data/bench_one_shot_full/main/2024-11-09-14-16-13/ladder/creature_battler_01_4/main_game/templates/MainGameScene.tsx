import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Card, CardContent } from "@/components/ui/custom/creature/creature_card";

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
    <div className="h-screen w-screen aspect-video flex flex-col bg-background">
      {/* Top HUD */}
      <Card uid="hud" className="w-full bg-primary/10">
        <CardContent uid="hud-content" className="flex justify-between items-center p-4">
          {player && (
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl=""
            />
          )}
          <div className="flex items-center gap-2">
            <Sword className="w-4 h-4" />
            <Shield className="w-4 h-4" />
          </div>
          {bot && (
            <PlayerCard
              uid={bot.uid}
              name={bot.display_name}
              imageUrl=""
            />
          )}
        </CardContent>
      </Card>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center px-16 py-8">
        {player_creature && (
          <Card uid={`${player_creature.uid}-container`} className="relative">
            <CardContent uid={`${player_creature.uid}-container-content`}>
              <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-sm font-bold">
                Your Creature
              </span>
              <CreatureCard
                uid={player_creature.uid}
                name={player_creature.display_name}
                hp={player_creature.stats.hp}
                maxHp={player_creature.stats.max_hp}
                imageUrl=""
              />
            </CardContent>
          </Card>
        )}

        {bot_creature && (
          <Card uid={`${bot_creature.uid}-container`} className="relative">
            <CardContent uid={`${bot_creature.uid}-container-content`}>
              <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-sm font-bold">
                Opponent's Creature
              </span>
              <CreatureCard
                uid={bot_creature.uid}
                name={bot_creature.display_name}
                hp={bot_creature.stats.hp}
                maxHp={bot_creature.stats.max_hp}
                imageUrl=""
              />
            </CardContent>
          </Card>
        )}
      </div>

      {/* Bottom UI */}
      <Card uid="skills-container" className="bg-secondary/10">
        <CardContent uid="skills-content" className="p-4">
          <div className="grid grid-cols-4 gap-4 max-w-2xl mx-auto">
            {player_creature?.collections.skills.map((skill) => (
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
        </CardContent>
      </Card>
    </div>
  );
}
