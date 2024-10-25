import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { ArrowLeft, Repeat } from 'lucide-react';

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

  const player = props.data.entities.player;
  const opponent = props.data.entities.opponent;
  const playerCreature = player?.entities.active_creature;
  const opponentCreature = opponent?.entities.active_creature;

  return (
    <div className="w-full h-full flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-7xl aspect-video bg-white shadow-lg rounded-lg overflow-hidden">
        <div className="h-2/3 grid grid-cols-2 grid-rows-2 p-4 gap-4">
          <div className="row-start-2 col-start-1 flex items-end justify-start">
            {playerCreature && (
              <CreatureCard
                uid={playerCreature.uid}
                name={playerCreature.display_name}
                image={`/images/creatures/${playerCreature.uid}.png`}
                hp={playerCreature.stats.hp}
                maxHp={playerCreature.stats.max_hp}
              />
            )}
          </div>
          <div className="row-start-2 col-start-2 flex items-end justify-end">
            {player && (
              <PlayerCard
                uid={player.uid}
                playerName={player.display_name}
                imageUrl={`/images/players/${player.uid}.png`}
              />
            )}
          </div>
          <div className="row-start-1 col-start-2 flex items-start justify-end">
            {opponentCreature && (
              <CreatureCard
                uid={opponentCreature.uid}
                name={opponentCreature.display_name}
                image={`/images/creatures/${opponentCreature.uid}.png`}
                hp={opponentCreature.stats.hp}
                maxHp={opponentCreature.stats.max_hp}
              />
            )}
          </div>
          <div className="row-start-1 col-start-1 flex items-start justify-start">
            {opponent && (
              <PlayerCard
                uid={opponent.uid}
                playerName={opponent.display_name}
                imageUrl={`/images/players/${opponent.uid}.png`}
              />
            )}
          </div>
        </div>
        <div className="h-1/3 p-4">
          <div className="grid grid-cols-2 grid-rows-2 gap-4">
            {availableButtonSlugs.includes('attack') && playerCreature?.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Base Damage: ${skill.stats.base_damage}`}
                onClick={() => emitButtonClick('attack')}
              />
            ))}
            {availableButtonSlugs.includes('back') && (
              <SkillButton
                uid="back-button"
                skillName="Back"
                description="Go back to the previous screen"
                stats="N/A"
                onClick={() => emitButtonClick('back')}
              >
                <ArrowLeft className="mr-2" /> Back
              </SkillButton>
            )}
            {availableButtonSlugs.includes('swap') && (
              <SkillButton
                uid="swap-button"
                skillName="Swap"
                description="Swap your active creature"
                stats="N/A"
                onClick={() => emitButtonClick('swap')}
              >
                <Repeat className="mr-2" /> Swap
              </SkillButton>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
