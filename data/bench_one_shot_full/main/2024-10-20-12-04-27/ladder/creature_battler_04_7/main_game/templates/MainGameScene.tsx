import { useCurrentButtons } from "@/lib/useChoices.ts";
import { ArrowLeftCircle } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";

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
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Creature Status */}
        <div className="col-start-1 row-start-1 flex items-start justify-start">
          <CreatureCard
            uid={opponentCreature?.uid || ''}
            name={opponentCreature?.display_name || 'Unknown'}
            image={`/images/creatures/${opponentCreature?.meta.creature_type || 'unknown'}_front.png`}
            hp={opponentCreature?.stats.hp || 0}
            maxHp={opponentCreature?.stats.max_hp || 1}
          />
        </div>

        {/* Opponent Creature */}
        <div className="col-start-2 row-start-1 flex items-center justify-center">
          <img
            src={`/images/creatures/${opponentCreature?.meta.creature_type || 'unknown'}_front.png`}
            alt={opponentCreature?.display_name || 'Unknown'}
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Player Creature */}
        <div className="col-start-1 row-start-2 flex items-center justify-center">
          <img
            src={`/images/creatures/${playerCreature?.meta.creature_type || 'unknown'}_back.png`}
            alt={playerCreature?.display_name || 'Unknown'}
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Player Creature Status */}
        <div className="col-start-2 row-start-2 flex items-end justify-end">
          <CreatureCard
            uid={playerCreature?.uid || ''}
            name={playerCreature?.display_name || 'Unknown'}
            image={`/images/creatures/${playerCreature?.meta.creature_type || 'unknown'}_back.png`}
            hp={playerCreature?.stats.hp || 0}
            maxHp={playerCreature?.stats.max_hp || 1}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 gap-4">
          {playerCreature?.collections?.skills?.map((skill: Skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Base Damage: ${skill.stats.base_damage}`}
            />
          ))}
          {availableButtonSlugs.includes('return-to-main-menu') && (
            <Button
              onClick={() => emitButtonClick('return-to-main-menu')}
              className="col-span-2"
            >
              <ArrowLeftCircle className="mr-2 h-4 w-4" />
              Return to Main Menu
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
