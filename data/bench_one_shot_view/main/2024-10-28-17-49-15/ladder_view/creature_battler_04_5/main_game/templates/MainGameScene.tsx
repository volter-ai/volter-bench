import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Shield, Zap } from 'lucide-react';

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
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

  const renderCreatureImage = (creature: Creature, isOpponent: boolean) => (
    <div className={`w-full h-full flex items-center ${isOpponent ? 'justify-end' : 'justify-start'}`}>
      <img
        src={`/images/creatures/${creature.meta.creature_type}.png`}
        alt={creature.display_name}
        className={`max-w-[50%] max-h-[80%] ${isOpponent ? '' : 'transform scaleX(-1)'}`}
      />
    </div>
  );

  const renderCreatureStatus = (creature: Creature, isOpponent: boolean) => (
    <div className={`flex flex-col ${isOpponent ? 'items-start' : 'items-end'}`}>
      <h2 className="text-xl font-bold">{creature.display_name}</h2>
      <div className={`flex items-center space-x-2 ${isOpponent ? '' : 'flex-row-reverse'}`}>
        {isOpponent ? <Shield className="w-4 h-4" /> : <Zap className="w-4 h-4" />}
        <span>{creature.stats.hp}/{creature.stats.max_hp}</span>
      </div>
      <div className="w-32 h-2 bg-gray-300 rounded-full mt-1">
        <div
          className="h-full bg-green-500 rounded-full"
          style={{ width: `${(creature.stats.hp / creature.stats.max_hp) * 100}%` }}
        ></div>
      </div>
    </div>
  );

  const renderSkillButtons = () => (
    <div className="grid grid-cols-2 gap-4">
      {availableButtonSlugs.map((slug) => (
        <SkillButton
          key={slug}
          uid={slug}
          skillName={slug}
          description=""
          stats=""
          className="w-full"
          onClick={() => emitButtonClick(slug)}
        />
      ))}
    </div>
  );

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        <div className="row-start-1 col-start-1 flex items-start justify-start">
          {renderCreatureStatus(opponent_creature, true)}
        </div>
        <div className="row-start-1 col-start-2 flex items-start justify-end">
          {renderCreatureImage(opponent_creature, true)}
        </div>
        <div className="row-start-2 col-start-1 flex items-end justify-start">
          {renderCreatureImage(player_creature, false)}
        </div>
        <div className="row-start-2 col-start-2 flex items-end justify-end">
          {renderCreatureStatus(player_creature, false)}
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        {availableButtonSlugs.length > 0 ? (
          renderSkillButtons()
        ) : (
          <div className="text-center text-xl">Waiting for action...</div>
        )}
      </div>
    </div>
  );
}
