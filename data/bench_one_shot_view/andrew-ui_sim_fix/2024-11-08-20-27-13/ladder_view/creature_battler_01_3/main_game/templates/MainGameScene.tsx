import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield } from 'lucide-react';
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

  const { player, foe, player_creature: playerCreature, foe_creature: foeCreature } = props.data.entities;

  if (!playerCreature || !foeCreature || !player || !foe) {
    return <div className="h-screen w-full flex items-center justify-center">
      Loading battle...
    </div>;
  }

  return (
    <div className="h-screen w-full flex flex-col bg-background">
      {/* HUD */}
      <nav className="h-16 bg-primary/10 flex items-center justify-between px-4">
        <div className="flex items-center gap-4">
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
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-between px-8">
        <div className="relative">
          <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-primary/20 px-3 py-1 rounded-full">
            Player
          </div>
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl={`/creatures/${playerCreature.uid}.png`}
          />
        </div>

        <div className="relative">
          <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-destructive/20 px-3 py-1 rounded-full">
            Opponent
          </div>
          <CreatureCard
            uid={foeCreature.uid}
            name={foeCreature.display_name}
            hp={foeCreature.stats.hp}
            maxHp={foeCreature.stats.max_hp}
            imageUrl={`/creatures/${foeCreature.uid}.png`}
          />
        </div>
      </div>

      {/* Skills/UI Area */}
      <div className="h-1/3 bg-secondary/10 p-4">
        <div className="grid grid-cols-2 gap-4 max-w-2xl mx-auto">
          {playerCreature.collections?.skills?.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          )) ?? (
            <div className="col-span-2 text-center text-muted-foreground">
              No skills available
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
