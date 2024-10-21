import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, RefreshCw } from 'lucide-react';
import { CreatureCard, Progress } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

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

  return (
    <div className="w-full h-full flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-7xl aspect-video bg-white shadow-lg rounded-lg overflow-hidden flex flex-col">
        <div className="h-2/3 grid grid-cols-2 grid-rows-2 p-4 gap-4">
          <div className="row-start-2 col-start-1 flex items-end justify-start">
            {playerCreature && (
              <CreatureCard
                uid={playerCreature.uid}
                name={playerCreature.display_name}
                image={`/images/creatures/${playerCreature.uid}_back.png`}
                hp={playerCreature.stats.hp}
                maxHp={playerCreature.stats.max_hp}
              />
            )}
          </div>
          <div className="row-start-2 col-start-2 flex items-end justify-end">
            {playerCreature && (
              <div className="text-right">
                <h3 className="font-bold">{playerCreature.display_name}</h3>
                <Progress 
                  uid={`${playerCreature.uid}-hp`}
                  value={(playerCreature.stats.hp / playerCreature.stats.max_hp) * 100} 
                  className="w-32"
                />
                <p>HP: {playerCreature.stats.hp} / {playerCreature.stats.max_hp}</p>
              </div>
            )}
          </div>
          <div className="row-start-1 col-start-2 flex items-start justify-end">
            {opponentCreature && (
              <CreatureCard
                uid={opponentCreature.uid}
                name={opponentCreature.display_name}
                image={`/images/creatures/${opponentCreature.uid}_front.png`}
                hp={opponentCreature.stats.hp}
                maxHp={opponentCreature.stats.max_hp}
              />
            )}
          </div>
          <div className="row-start-1 col-start-1 flex items-start justify-start">
            {opponentCreature && (
              <div className="text-left">
                <h3 className="font-bold">{opponentCreature.display_name}</h3>
                <Progress 
                  uid={`${opponentCreature.uid}-hp`}
                  value={(opponentCreature.stats.hp / opponentCreature.stats.max_hp) * 100} 
                  className="w-32"
                />
                <p>HP: {opponentCreature.stats.hp} / {opponentCreature.stats.max_hp}</p>
              </div>
            )}
          </div>
        </div>
        <div className="h-1/3 p-4 bg-gray-100">
          <div className="grid grid-cols-2 gap-4">
            {availableButtonSlugs.includes('attack') && (
              <SkillButton
                uid="attack-button"
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
                uid="swap-button"
                skillName="Swap"
                description="Swap your active creature"
                stats="No damage"
                onClick={() => emitButtonClick('swap')}
              >
                <RefreshCw className="mr-2 h-4 w-4" /> Swap
              </SkillButton>
            )}
            {playerCreature?.collections?.skills?.map((skill: Skill) => (
              availableButtonSlugs.includes(skill.uid) && (
                <SkillButton
                  key={skill.uid}
                  uid={skill.uid}
                  skillName={skill.display_name}
                  description={skill.description}
                  stats={`Base Damage: ${skill.stats.base_damage}`}
                  onClick={() => emitButtonClick(skill.uid)}
                />
              )
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
