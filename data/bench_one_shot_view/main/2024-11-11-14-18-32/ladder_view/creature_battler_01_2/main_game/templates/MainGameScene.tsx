import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Sword } from 'lucide-react';
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
  description: string;
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

  const getImageUrl = (type: string, id: string) => `/assets/${type}/${id}.png`;

  const handleSkillClick = (skillUid: string) => {
    const matchingSlug = availableButtonSlugs.find(slug => slug === skillUid);
    if (matchingSlug) {
      emitButtonClick(matchingSlug);
    }
  };

  return (
    <div className="relative h-screen w-screen bg-slate-900 text-white overflow-hidden">
      <div className="grid grid-rows-[auto_1fr_auto] h-full max-w-7xl mx-auto">
        {/* HUD */}
        <nav className="flex justify-between items-center p-4 bg-slate-800 z-10">
          {player && (
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl={getImageUrl('player', player.meta.prototype_id)}
            />
          )}
          <div className="flex items-center gap-2">
            <Sword className="w-6 h-6" />
            <span>Battle Scene</span>
          </div>
          {foe && (
            <PlayerCard
              uid={foe.uid}
              name={foe.display_name}
              imageUrl={getImageUrl('player', foe.meta.prototype_id)}
            />
          )}
        </nav>

        {/* Battlefield */}
        <div className="flex justify-between items-center p-8 gap-8 z-10">
          {player_creature && (
            <div className="relative">
              <span className="absolute -top-8 left-1/2 transform -translate-x-1/2 text-green-400">
                Your Creature
              </span>
              <CreatureCard
                uid={player_creature.uid}
                name={player_creature.display_name}
                hp={player_creature.stats.hp}
                maxHp={player_creature.stats.max_hp}
                imageUrl={getImageUrl('creature', player_creature.meta.prototype_id)}
              />
            </div>
          )}

          {foe_creature && (
            <div className="relative">
              <span className="absolute -top-8 left-1/2 transform -translate-x-1/2 text-red-400">
                Enemy Creature
              </span>
              <CreatureCard
                uid={foe_creature.uid}
                name={foe_creature.display_name}
                hp={foe_creature.stats.hp}
                maxHp={foe_creature.stats.max_hp}
                imageUrl={getImageUrl('creature', foe_creature.meta.prototype_id)}
              />
            </div>
          )}
        </div>

        {/* Skills UI */}
        <div className="relative bg-slate-800 p-4 z-20">
          <div className="grid grid-cols-3 gap-4 max-w-2xl mx-auto">
            {player_creature?.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.damage}`}
                disabled={!availableButtonSlugs.includes(skill.uid)}
                onClick={() => handleSkillClick(skill.uid)}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
