import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, RefreshCw } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

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

interface Player {
  uid: string;
  display_name: string;
  entities: {
    active_creature: Creature;
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
    player: Player;
    opponent: Player;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player?.entities.active_creature;
  const opponentCreature = props.data.entities.opponent?.entities.active_creature;

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        <div className="col-start-1 row-start-1 flex justify-start items-start">
          {opponentCreature && (
            <div>
              <h2>{opponentCreature.display_name}</h2>
              <div className="w-32 bg-gray-200 rounded-full h-2.5">
                <div className="bg-blue-600 h-2.5 rounded-full" style={{width: `${(opponentCreature.stats.hp / opponentCreature.stats.max_hp) * 100}%`}}></div>
              </div>
            </div>
          )}
        </div>
        <div className="col-start-2 row-start-1 flex justify-end items-start">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              image={`/images/creatures/${opponentCreature.meta.creature_type}_front.png`}
              hp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>
        <div className="col-start-1 row-start-2 flex justify-start items-end">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              image={`/images/creatures/${playerCreature.meta.creature_type}_back.png`}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
        <div className="col-start-2 row-start-2 flex justify-end items-end">
          {playerCreature && (
            <div>
              <h2>{playerCreature.display_name}</h2>
              <div className="w-32 bg-gray-200 rounded-full h-2.5">
                <div className="bg-blue-600 h-2.5 rounded-full" style={{width: `${(playerCreature.stats.hp / playerCreature.stats.max_hp) * 100}%`}}></div>
              </div>
            </div>
          )}
        </div>
      </div>
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 grid-rows-2 gap-4">
          {availableButtonSlugs.includes('attack') && (
            <SkillButton
              uid="attack"
              skillName="Attack"
              description="Perform a basic attack"
              stats="Damage varies"
              onClick={() => emitButtonClick('attack')}
            >
              <Sword className="mr-2 h-4 w-4" /> Attack
            </SkillButton>
          )}
          {availableButtonSlugs.includes('swap') && (
            <SkillButton
              uid="swap"
              skillName="Swap"
              description="Swap your active creature"
              stats="No cost"
              onClick={() => emitButtonClick('swap')}
            >
              <RefreshCw className="mr-2 h-4 w-4" /> Swap
            </SkillButton>
          )}
          {playerCreature?.collections?.skills?.map((skill: Skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Base Damage: ${skill.stats.base_damage}`}
              onClick={() => emitButtonClick(skill.uid)}
            >
              {skill.display_name}
            </SkillButton>
          ))}
        </div>
      </div>
    </div>
  );
}
