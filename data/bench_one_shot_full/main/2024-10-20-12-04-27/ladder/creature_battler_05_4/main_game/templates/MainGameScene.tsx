import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';

interface Skill {
  __type: "Skill";
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
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
    creature_type: string;
  };
}

interface Player {
  __type: "Player";
  uid: string;
  display_name: string;
  entities: {
    active_creature: Creature;
  };
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data.entities.player?.entities.active_creature;
  const opponentCreature = props.data.entities.opponent?.entities.active_creature;

  const getCreatureImage = (creature: Creature, isOpponent: boolean) => {
    const baseUrl = `/images/creatures/${creature.meta.creature_type}/`;
    return `${baseUrl}${creature.display_name.toLowerCase()}_${isOpponent ? 'front' : 'back'}.png`;
  };

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Creature Status */}
        <div className="col-start-1 row-start-1 flex items-start justify-start">
          {opponentCreature && (
            <div className="text-left">
              <h3 className="font-bold">{opponentCreature.display_name}</h3>
              <div className="w-32 bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
                <div 
                  className="bg-blue-600 h-2.5 rounded-full" 
                  style={{width: `${(opponentCreature.stats.hp / opponentCreature.stats.max_hp) * 100}%`}}
                ></div>
              </div>
              <p className="text-sm">HP: {opponentCreature.stats.hp}/{opponentCreature.stats.max_hp}</p>
            </div>
          )}
        </div>

        {/* Opponent Creature */}
        <div className="col-start-2 row-start-1 flex items-center justify-center">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              image={getCreatureImage(opponentCreature, true)}
              hp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Player Creature */}
        <div className="col-start-1 row-start-2 flex items-center justify-center">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              image={getCreatureImage(playerCreature, false)}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Player Creature Status */}
        <div className="col-start-2 row-start-2 flex items-end justify-end">
          {playerCreature && (
            <div className="text-right">
              <h3 className="font-bold">{playerCreature.display_name}</h3>
              <div className="w-32 bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
                <div 
                  className="bg-green-600 h-2.5 rounded-full" 
                  style={{width: `${(playerCreature.stats.hp / playerCreature.stats.max_hp) * 100}%`}}
                ></div>
              </div>
              <p className="text-sm">HP: {playerCreature.stats.hp}/{playerCreature.stats.max_hp}</p>
            </div>
          )}
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
          {availableButtonSlugs.includes('attack') && (
            <SkillButton
              uid="attack-button"
              skillName="Attack"
              description="Choose an attack"
              stats=""
              onClick={() => emitButtonClick('attack')}
            >
              <Sword className="mr-2 h-4 w-4" /> Attack
            </SkillButton>
          )}
          {availableButtonSlugs.includes('back') && (
            <SkillButton
              uid="back-button"
              skillName="Back"
              description="Go back"
              stats=""
              onClick={() => emitButtonClick('back')}
            >
              <ArrowLeft className="mr-2 h-4 w-4" /> Back
            </SkillButton>
          )}
          {availableButtonSlugs.includes('swap') && (
            <SkillButton
              uid="swap-button"
              skillName="Swap"
              description="Swap creatures"
              stats=""
              onClick={() => emitButtonClick('swap')}
            >
              <Repeat className="mr-2 h-4 w-4" /> Swap
            </SkillButton>
          )}
          {playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}`}
              onClick={() => emitButtonClick(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
