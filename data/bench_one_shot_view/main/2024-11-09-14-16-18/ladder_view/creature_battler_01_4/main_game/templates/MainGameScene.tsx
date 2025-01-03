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
    foe: Player;
    player_creature: Creature;
    foe_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const { player, foe, player_creature, foe_creature } = props.data.entities;

  if (!player || !foe || !player_creature || !foe_creature) {
    return null;
  }

  return (
    <div className="h-screen w-screen aspect-video flex flex-col bg-background">
      {/* HUD */}
      <nav className="w-full bg-secondary p-4 flex justify-between items-center">
        <div className="flex items-center gap-4">
          <Sword className="h-5 w-5" />
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={`/players/${player.uid}.png`}
          />
        </div>
        <div className="flex items-center gap-4">
          <PlayerCard
            uid={foe.uid}
            name={foe.display_name}
            imageUrl={`/players/${foe.uid}.png`}
          />
          <Shield className="h-5 w-5" />
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center px-16 py-8">
        <div className="relative">
          <div className="absolute -top-8 left-1/2 -translate-x-1/2 text-sm font-bold">
            Your Creature
          </div>
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            imageUrl={`/creatures/${player_creature.uid}.png`}
          />
        </div>

        <div className="relative">
          <div className="absolute -top-8 left-1/2 -translate-x-1/2 text-sm font-bold">
            Opponent's Creature
          </div>
          <CreatureCard
            uid={foe_creature.uid}
            name={foe_creature.display_name}
            hp={foe_creature.stats.hp}
            maxHp={foe_creature.stats.max_hp}
            imageUrl={`/creatures/${foe_creature.uid}.png`}
          />
        </div>
      </div>

      {/* Skills/UI Area */}
      <div className="bg-secondary/50 p-8">
        <div className="grid grid-cols-4 gap-4 max-w-2xl mx-auto">
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
