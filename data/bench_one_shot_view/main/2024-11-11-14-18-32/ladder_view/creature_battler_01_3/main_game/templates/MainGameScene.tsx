import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, User } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
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
    category: string;
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
    category: string;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
  __type: "Player";
  uid: string;
  display_name: string;
  description: string;
  meta: {
    prototype_id: string;
    category: string;
  };
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
  collections: {
    player_skill_queue: any[];
    foe_skill_queue: any[];
  };
  meta: Record<string, unknown>;
  stats: Record<string, unknown>;
  uid: string;
  display_name: string;
  description: string;
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const { player_creature, foe_creature } = props.data.entities;

  const getCreatureImageUrl = (creature: Creature) => {
    return `/assets/creatures/${creature.meta.prototype_id}.png`;
  };

  const handleSkillClick = (skillUid: string) => {
    // Find the matching button slug for the skill
    const matchingSlug = availableButtonSlugs.find(slug => 
      slug.toLowerCase().includes(skillUid.toLowerCase()) || 
      skillUid.toLowerCase().includes(slug.toLowerCase())
    );
    
    if (matchingSlug) {
      emitButtonClick(matchingSlug);
    }
  };

  return (
    <div className="h-screen w-screen bg-slate-900">
      <div className="container mx-auto h-full grid grid-rows-[auto_1fr_auto] gap-4 p-4">
        {/* HUD */}
        <nav className="flex justify-between items-center bg-slate-800 rounded-lg p-4">
          <div className="flex items-center gap-2">
            <User className="w-6 h-6 text-white" />
            <span className="text-white font-semibold">{props.data.display_name}</span>
          </div>
          <div className="flex gap-4">
            <Sword className="w-6 h-6 text-white" />
            <Shield className="w-6 h-6 text-white" />
          </div>
        </nav>

        {/* Battlefield */}
        <div className="flex justify-between items-center px-8">
          {player_creature && (
            <div className="relative">
              <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-white font-semibold">
                Your Creature
              </span>
              <CreatureCard
                uid={player_creature.uid}
                name={player_creature.display_name}
                hp={player_creature.stats.hp}
                maxHp={player_creature.stats.max_hp}
                imageUrl={getCreatureImageUrl(player_creature)}
              />
            </div>
          )}

          {foe_creature && (
            <div className="relative">
              <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-white font-semibold">
                Opponent's Creature
              </span>
              <CreatureCard
                uid={foe_creature.uid}
                name={foe_creature.display_name}
                hp={foe_creature.stats.hp}
                maxHp={foe_creature.stats.max_hp}
                imageUrl={getCreatureImageUrl(foe_creature)}
              />
            </div>
          )}
        </div>

        {/* Skills UI */}
        <div className="bg-slate-800 rounded-lg p-4">
          <div className="grid grid-cols-3 gap-4">
            {player_creature?.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.damage}`}
                disabled={!availableButtonSlugs.some(slug => 
                  slug.toLowerCase().includes(skill.uid.toLowerCase()) || 
                  skill.uid.toLowerCase().includes(slug.toLowerCase())
                )}
                onClick={() => handleSkillClick(skill.uid)}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
