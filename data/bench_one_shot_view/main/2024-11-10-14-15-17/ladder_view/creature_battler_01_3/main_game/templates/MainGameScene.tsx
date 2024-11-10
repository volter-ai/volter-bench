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

  // Generate image URLs based on prototype IDs
  const getImageUrl = (entity: { meta: { prototype_id: string } }) => 
    `/assets/sprites/${entity.meta.prototype_id}.png`;

  if (!player || !foe || !player_creature || !foe_creature) {
    return <div className="h-screen w-full flex items-center justify-center">
      Loading battle...
    </div>;
  }

  return (
    <div className="flex flex-col h-screen w-full bg-background">
      {/* HUD */}
      <nav className="h-16 bg-primary/10 flex items-center justify-between px-4">
        <div className="flex items-center gap-4">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={getImageUrl(player)}
          />
          <Sword className="h-6 w-6" />
        </div>
        <div className="flex items-center gap-4">
          <Shield className="h-6 w-6" />
          <PlayerCard
            uid={foe.uid}
            name={foe.display_name}
            imageUrl={getImageUrl(foe)}
          />
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-between px-8">
        <div className="relative">
          <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-primary/20 px-4 py-1 rounded-full">
            Player
          </div>
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            imageUrl={getImageUrl(player_creature)}
          />
        </div>

        <div className="relative">
          <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-destructive/20 px-4 py-1 rounded-full">
            Opponent
          </div>
          <CreatureCard
            uid={foe_creature.uid}
            name={foe_creature.display_name}
            hp={foe_creature.stats.hp}
            maxHp={foe_creature.stats.max_hp}
            imageUrl={getImageUrl(foe_creature)}
          />
        </div>
      </div>

      {/* UI Area */}
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
          ))}
        </div>
      </div>
    </div>
  );
}
