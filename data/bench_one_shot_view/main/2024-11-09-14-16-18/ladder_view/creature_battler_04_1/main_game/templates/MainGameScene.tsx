import { useCurrentButtons } from "@/lib/useChoices";
import { Sword, Shield, Zap } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  __type: "Skill";
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
  meta: {
    prototype_id: string;
    category: string;
    skill_type: string;
    is_physical: boolean;
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
    attack: number;
    defense: number;
    sp_attack: number;
    sp_defense: number;
    speed: number;
  };
  meta: {
    prototype_id: string;
    category: string;
    creature_type: string;
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
    opponent: Player;
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  if (!playerCreature || !opponentCreature) {
    return <div className="w-screen h-screen flex items-center justify-center">
      Loading battle...
    </div>;
  }

  return (
    <div className="w-screen h-screen bg-background">
      <div className="aspect-video h-full max-h-screen mx-auto">
        {/* Battlefield Section */}
        <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4 bg-muted/20">
          {/* Opponent Status */}
          <div className="flex items-start justify-start">
            {opponentCreature && (
              <CreatureCard
                uid={opponentCreature.uid}
                name={opponentCreature.display_name}
                currentHp={opponentCreature.stats.hp}
                maxHp={opponentCreature.stats.max_hp}
                image={`/assets/creatures/${opponentCreature.meta.prototype_id}.png`}
              />
            )}
          </div>

          {/* Opponent Creature */}
          <div className="flex items-center justify-center">
            <div className="relative">
              <div className="absolute bottom-0 w-32 h-8 bg-black/20 rounded-full blur-sm" />
              {opponentCreature && (
                <img
                  src={`/assets/creatures/${opponentCreature.meta.prototype_id}.png`}
                  alt={opponentCreature.display_name}
                  className="w-32 h-32 object-contain"
                />
              )}
            </div>
          </div>

          {/* Player Creature */}
          <div className="flex items-center justify-center">
            <div className="relative">
              <div className="absolute bottom-0 w-32 h-8 bg-black/20 rounded-full blur-sm" />
              {playerCreature && (
                <img
                  src={`/assets/creatures/${playerCreature.meta.prototype_id}.png`}
                  alt={playerCreature.display_name}
                  className="w-32 h-32 object-contain"
                />
              )}
            </div>
          </div>

          {/* Player Status */}
          <div className="flex items-end justify-end">
            {playerCreature && (
              <CreatureCard
                uid={playerCreature.uid}
                name={playerCreature.display_name}
                currentHp={playerCreature.stats.hp}
                maxHp={playerCreature.stats.max_hp}
                image={`/assets/creatures/${playerCreature.meta.prototype_id}.png`}
              />
            )}
          </div>
        </div>

        {/* UI Section */}
        <div className="h-1/3 grid grid-cols-2 gap-4 p-4 bg-muted">
          {playerCreature?.collections?.skills?.map((skill: Skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              damage={skill.stats.base_damage}
              type={skill.meta.skill_type}
              variant="secondary"
              className="h-full text-lg"
            />
          ))}
        </div>
      </div>
    </div>
  );
}
