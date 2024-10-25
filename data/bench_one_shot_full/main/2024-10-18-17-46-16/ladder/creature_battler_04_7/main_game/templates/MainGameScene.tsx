import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Sword, Shield, Zap } from 'lucide-react';

interface Creature {
  uid: string;
  display_name: string;
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
    creature_type: string;
  };
}

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
  meta: {
    skill_type: string;
    is_physical: boolean;
  };
}

interface GameUIData {
  entities: {
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const { player_creature, opponent_creature } = props.data.entities;

  const renderCreatureStats = (creature: Creature) => (
    <div className="flex flex-col space-y-2">
      <div className="flex items-center">
        <Sword className="w-4 h-4 mr-2" />
        <span>ATK: {creature.stats.attack}</span>
      </div>
      <div className="flex items-center">
        <Shield className="w-4 h-4 mr-2" />
        <span>DEF: {creature.stats.defense}</span>
      </div>
      <div className="flex items-center">
        <Zap className="w-4 h-4 mr-2" />
        <span>SPD: {creature.stats.speed}</span>
      </div>
    </div>
  );

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Player Creature Status */}
        <div className="flex flex-col items-start justify-center">
          <h2 className="text-xl font-bold mb-2">{player_creature.display_name}</h2>
          {renderCreatureStats(player_creature)}
        </div>

        {/* Opponent Creature */}
        <div className="flex items-center justify-center">
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            image={`/images/creatures/${opponent_creature.meta.creature_type}.png`}
            hp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
          />
        </div>

        {/* Player Creature */}
        <div className="flex items-center justify-center">
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            image={`/images/creatures/${player_creature.meta.creature_type}_back.png`}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
          />
        </div>

        {/* Opponent Creature Status */}
        <div className="flex flex-col items-end justify-center">
          <h2 className="text-xl font-bold mb-2">{opponent_creature.display_name}</h2>
          {renderCreatureStats(opponent_creature)}
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-white p-4">
        {availableButtonSlugs.length > 0 ? (
          <div className="grid grid-cols-2 gap-4">
            {availableButtonSlugs.map((slug) => (
              <SkillButton
                key={slug}
                uid={slug}
                skillName={slug}
                description=""
                stats=""
                onClick={() => emitButtonClick(slug)}
              />
            ))}
          </div>
        ) : (
          <div className="flex items-center justify-center h-full">
            <p className="text-xl">Waiting for action...</p>
          </div>
        )}
      </div>
    </div>
  );
}
