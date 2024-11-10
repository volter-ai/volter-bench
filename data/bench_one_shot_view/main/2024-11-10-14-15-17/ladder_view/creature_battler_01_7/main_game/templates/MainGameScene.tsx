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

  const { player, foe, player_creature, foe_creature } = props.data.entities;

  // Generate deterministic image URLs based on prototype_id or uid
  const getImageUrl = (entity: { uid: string }) => 
    `/assets/images/${entity.uid}.png`;

  return (
    <div className="h-screen w-full flex flex-col">
      {/* HUD */}
      <nav className="h-16 bg-primary/10 flex items-center justify-between px-4">
        {player && (
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={getImageUrl(player)}
          />
        )}
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <Sword className="w-4 h-4" />
            <span>Battle Phase</span>
          </div>
          <div className="flex items-center gap-2">
            <Shield className="w-4 h-4" />
            <span>Defense Active</span>
          </div>
        </div>
        {foe && (
          <PlayerCard
            uid={foe.uid}
            name={foe.display_name}
            imageUrl={getImageUrl(foe)}
          />
        )}
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-between px-8 bg-secondary/5">
        {player_creature && (
          <div className="relative">
            <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-primary px-3 py-1 rounded-full text-sm">
              Your Creature
            </div>
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              hp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
              imageUrl={getImageUrl(player_creature)}
            />
          </div>
        )}

        {foe_creature && (
          <div className="relative">
            <div className="absolute -top-8 left-1/2 -translate-x-1/2 bg-destructive px-3 py-1 rounded-full text-sm">
              Opponent's Creature
            </div>
            <CreatureCard
              uid={foe_creature.uid}
              name={foe_creature.display_name}
              hp={foe_creature.stats.hp}
              maxHp={foe_creature.stats.max_hp}
              imageUrl={getImageUrl(foe_creature)}
            />
          </div>
        )}
      </div>

      {/* Controls */}
      <div className="h-1/3 bg-background border-t">
        <div className="p-4 grid grid-cols-4 gap-4">
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
      </div>
    </div>
  );
}
