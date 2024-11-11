import { useCurrentButtons } from "@/lib/useChoices";
import { Sword, ArrowLeft, SwapHorizontal } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";

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
  entities: {
    active_creature?: Creature;
  };
  meta: {
    prototype_id: string;
    category: string;
  };
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player?.entities?.active_creature;
  const opponentCreature = props.data.entities.opponent?.entities?.active_creature;

  if (!playerCreature || !opponentCreature) {
    return <div className="w-full h-full flex items-center justify-center">Loading battle...</div>;
  }

  return (
    <div className="w-full h-full aspect-video bg-background flex flex-col">
      {/* Battlefield (upper 2/3) */}
      <div className="h-2/3 grid grid-cols-2 gap-4 p-4">
        {/* Top left - Opponent Status */}
        <div className="flex items-start justify-start">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            imageUrl={`/creatures/${opponentCreature.meta.prototype_id}_front.png`}
            currentHp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
          />
        </div>

        {/* Top right - Opponent Creature */}
        <div className="flex items-center justify-center relative">
          <div className="absolute bottom-0 w-32 h-4 bg-black/20 rounded-full blur-sm" />
          <img 
            src={`/creatures/${opponentCreature.meta.prototype_id}_front.png`}
            alt={opponentCreature.display_name}
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Bottom left - Player Creature */}
        <div className="flex items-center justify-center relative">
          <div className="absolute bottom-0 w-32 h-4 bg-black/20 rounded-full blur-sm" />
          <img 
            src={`/creatures/${playerCreature.meta.prototype_id}_back.png`}
            alt={playerCreature.display_name}
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Bottom right - Player Status */}
        <div className="flex items-end justify-end">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl={`/creatures/${playerCreature.meta.prototype_id}_back.png`}
            currentHp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
        </div>
      </div>

      {/* UI Area (lower 1/3) */}
      <div className="h-1/3 p-4 bg-muted">
        <div className="grid grid-cols-4 gap-2">
          {availableButtonSlugs.includes('attack') && playerCreature.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              description={skill.description}
              stats={{
                damage: skill.stats.base_damage,
                // We could add accuracy and cost if the data included them
              }}
            >
              <Sword className="mr-2 h-4 w-4" />
              {skill.display_name}
            </SkillButton>
          ))}
          
          {availableButtonSlugs.includes('back') && (
            <Button 
              onClick={() => emitButtonClick('back')}
              variant="secondary"
              className="w-full"
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back
            </Button>
          )}

          {availableButtonSlugs.includes('swap') && (
            <Button 
              onClick={() => emitButtonClick('swap')}
              variant="secondary"
              className="w-full"
            >
              <SwapHorizontal className="mr-2 h-4 w-4" />
              Swap
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
