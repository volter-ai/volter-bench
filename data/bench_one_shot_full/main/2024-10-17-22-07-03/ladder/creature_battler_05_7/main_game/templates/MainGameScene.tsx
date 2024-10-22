import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { Button } from "@/components/ui/button";

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
}

interface Creature {
  uid: string;
  display_name: string;
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
  const { enabledUIDs } = useThingInteraction();

  const playerCreature = props.data.entities.player?.entities.active_creature;
  const opponentCreature = props.data.entities.opponent?.entities.active_creature;

  const getCreatureImage = (creature: Creature | undefined) => {
    if (!creature) return "/placeholder-creature.png";
    return `/creatures/${creature.meta.creature_type}.png`;
  };

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Creature Status */}
        <div className="row-start-1 col-start-1 flex items-start justify-start">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              image={getCreatureImage(opponentCreature)}
              hp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Opponent Creature */}
        <div className="row-start-1 col-start-2 flex items-center justify-center">
          {props.data.entities.opponent && (
            <PlayerCard
              uid={props.data.entities.opponent.uid}
              playerName={props.data.entities.opponent.display_name}
              imageUrl={getCreatureImage(opponentCreature)}
            />
          )}
        </div>

        {/* Player Creature */}
        <div className="row-start-2 col-start-1 flex items-center justify-center">
          {props.data.entities.player && (
            <PlayerCard
              uid={props.data.entities.player.uid}
              playerName={props.data.entities.player.display_name}
              imageUrl={getCreatureImage(playerCreature)}
            />
          )}
        </div>

        {/* Player Creature Status */}
        <div className="row-start-2 col-start-2 flex items-end justify-end">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              image={getCreatureImage(playerCreature)}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 gap-4">
          {availableButtonSlugs.includes('attack') && (
            <Button onClick={() => emitButtonClick('attack')} disabled={!enabledUIDs.includes('attack')}>
              <Sword className="mr-2 h-4 w-4" /> Attack
            </Button>
          )}
          {availableButtonSlugs.includes('back') && (
            <Button onClick={() => emitButtonClick('back')} disabled={!enabledUIDs.includes('back')}>
              <ArrowLeft className="mr-2 h-4 w-4" /> Back
            </Button>
          )}
          {availableButtonSlugs.includes('swap') && (
            <Button onClick={() => emitButtonClick('swap')} disabled={!enabledUIDs.includes('swap')}>
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
              disabled={!enabledUIDs.includes(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
