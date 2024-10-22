import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';
import { CreatureCard, Progress } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { Button } from "@/components/ui/button";

interface Skill {
  __type: "Skill";
  stats: { base_damage: number };
  meta: { skill_type: string; is_physical: boolean };
  uid: string;
  display_name: string;
  description: string;
}

interface Creature {
  __type: "Creature";
  stats: { hp: number; max_hp: number };
  meta: { creature_type: string };
  collections: { skills: Skill[] };
  uid: string;
  display_name: string;
  description: string;
}

interface Player {
  __type: "Player";
  collections: { creatures: Creature[] };
  uid: string;
  display_name: string;
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
  };
  stats: { turn_counter: number };
  meta: { battle_ended: boolean };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player.collections.creatures[0];
  const opponentCreature = props.data.entities.opponent.collections.creatures[0];

  return (
    <div className="w-full h-full" style={{ aspectRatio: '16/9' }}>
      <div className="flex flex-col h-full">
        {/* Battlefield Display */}
        <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
          {/* Opponent Creature */}
          <div className="row-start-1 col-start-2 flex items-start justify-end">
            {opponentCreature && (
              <img
                src={`/images/creatures/${opponentCreature.meta.creature_type}.png`}
                alt={opponentCreature.display_name}
                className="w-48 h-48 object-contain"
              />
            )}
          </div>

          {/* Opponent Creature Status */}
          <div className="row-start-1 col-start-1 flex items-start justify-start">
            {opponentCreature && (
              <CreatureCard
                uid={opponentCreature.uid}
                name={opponentCreature.display_name}
                image={`/images/creatures/${opponentCreature.meta.creature_type}.png`}
                hp={opponentCreature.stats.hp}
                maxHp={opponentCreature.stats.max_hp}
              />
            )}
          </div>

          {/* Player Creature */}
          <div className="row-start-2 col-start-1 flex items-end justify-start">
            {playerCreature && (
              <img
                src={`/images/creatures/${playerCreature.meta.creature_type}.png`}
                alt={playerCreature.display_name}
                className="w-48 h-48 object-contain"
              />
            )}
          </div>

          {/* Player Creature Status */}
          <div className="row-start-2 col-start-2 flex items-end justify-end">
            {playerCreature && (
              <CreatureCard
                uid={playerCreature.uid}
                name={playerCreature.display_name}
                image={`/images/creatures/${playerCreature.meta.creature_type}.png`}
                hp={playerCreature.stats.hp}
                maxHp={playerCreature.stats.max_hp}
              />
            )}
          </div>
        </div>

        {/* User Interface */}
        <div className="h-1/3 bg-gray-100 p-4">
          <div className="grid grid-cols-2 gap-4 mb-4">
            {availableButtonSlugs.includes('attack') && (
              <Button onClick={() => emitButtonClick('attack')} uid="attack-button">
                <Sword className="mr-2 h-4 w-4" /> Attack
              </Button>
            )}
            {availableButtonSlugs.includes('back') && (
              <Button onClick={() => emitButtonClick('back')} uid="back-button">
                <ArrowLeft className="mr-2 h-4 w-4" /> Back
              </Button>
            )}
            {availableButtonSlugs.includes('swap') && (
              <Button onClick={() => emitButtonClick('swap')} uid="swap-button">
                <Repeat className="mr-2 h-4 w-4" /> Swap
              </Button>
            )}
          </div>
          
          {/* Skill Buttons */}
          <div className="grid grid-cols-2 gap-4 mb-4">
            {playerCreature?.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
              />
            ))}
          </div>
          
          {/* Player and Opponent Cards */}
          <div className="flex justify-between">
            <PlayerCard
              uid={props.data.entities.player.uid}
              playerName={props.data.entities.player.display_name}
              imageUrl="/images/player.png"
            />
            <PlayerCard
              uid={props.data.entities.opponent.uid}
              playerName={props.data.entities.opponent.display_name}
              imageUrl="/images/opponent.png"
            />
          </div>
        </div>
      </div>
    </div>
  );
}
