import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, User } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  __type: "Skill";
  uid: string;
  display_name: string;
  description: string;
  slug: string;
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

  const { player_creature, foe_creature } = props.data.entities;

  if (!player_creature || !foe_creature) {
    return <div className="w-full h-full flex items-center justify-center">
      Loading battle...
    </div>;
  }

  const getCreatureImage = (creature: Creature) => 
    `/assets/creatures/${creature.meta.prototype_id}.png`;

  const handleSkillClick = (skill: Skill) => {
    if (availableButtonSlugs.includes(skill.slug)) {
      emitButtonClick(skill.slug);
    }
  };

  const skills = player_creature.collections.skills || [];

  return (
    <div className="w-full h-full grid grid-rows-[auto_1fr_auto] gap-4 p-4 bg-background">
      <nav className="flex justify-between items-center p-2 bg-muted rounded-lg">
        <div className="flex items-center gap-2">
          <User className="w-4 h-4" />
          <span>{props.data.entities.player?.display_name || "Unknown Player"}</span>
        </div>
        <div className="flex items-center gap-2">
          <Sword className="w-4 h-4" />
          <Shield className="w-4 h-4" />
        </div>
      </nav>

      <div className="flex justify-between items-center px-8">
        <div className="relative">
          <span className="absolute -top-6 left-1/2 -translate-x-1/2 text-sm font-bold">
            Your Creature
          </span>
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            imageUrl={getCreatureImage(player_creature)}
          />
        </div>

        <div className="relative">
          <span className="absolute -top-6 left-1/2 -translate-x-1/2 text-sm font-bold">
            Opponent's Creature
          </span>
          <CreatureCard
            uid={foe_creature.uid}
            name={foe_creature.display_name}
            hp={foe_creature.stats.hp}
            maxHp={foe_creature.stats.max_hp}
            imageUrl={getCreatureImage(foe_creature)}
          />
        </div>
      </div>

      <div className="bg-muted p-4 rounded-lg">
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
          {skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              disabled={!availableButtonSlugs.includes(skill.slug)}
              onClick={() => handleSkillClick(skill)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
