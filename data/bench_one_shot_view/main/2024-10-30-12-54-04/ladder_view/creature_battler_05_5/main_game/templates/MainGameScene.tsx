import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';
import { Button } from "@/components/ui/button";
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
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player?.entities.active_creature;
  const opponentCreature = props.data.entities.opponent?.entities.active_creature;

  return (
    <div className="h-screen w-screen flex flex-col">
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        <div className="row-start-2 col-start-1 flex items-end justify-start">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl={`/images/creatures/${playerCreature.display_name.toLowerCase()}_back.png`}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
        <div className="row-start-2 col-start-2 flex items-end justify-end">
          <div className="text-right">
            <h3 className="text-xl font-bold">{playerCreature?.display_name}</h3>
            <p>HP: {playerCreature?.stats.hp} / {playerCreature?.stats.max_hp}</p>
          </div>
        </div>
        <div className="row-start-1 col-start-2 flex items-start justify-end">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              imageUrl={`/images/creatures/${opponentCreature.display_name.toLowerCase()}_front.png`}
              hp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>
        <div className="row-start-1 col-start-1 flex items-start justify-start">
          <div className="text-left">
            <h3 className="text-xl font-bold">{opponentCreature?.display_name}</h3>
            <p>HP: {opponentCreature?.stats.hp} / {opponentCreature?.stats.max_hp}</p>
          </div>
        </div>
      </div>
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="flex flex-wrap gap-2">
          {availableButtonSlugs.includes('attack') && (
            <Button onClick={() => emitButtonClick('attack')}>
              <Sword className="mr-2 h-4 w-4" /> Attack
            </Button>
          )}
          {availableButtonSlugs.includes('back') && (
            <Button onClick={() => emitButtonClick('back')}>
              <ArrowLeft className="mr-2 h-4 w-4" /> Back
            </Button>
          )}
          {availableButtonSlugs.includes('swap') && (
            <Button onClick={() => emitButtonClick('swap')}>
              <Repeat className="mr-2 h-4 w-4" /> Swap
            </Button>
          )}
          {playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Base Damage: ${skill.stats.base_damage}`}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
