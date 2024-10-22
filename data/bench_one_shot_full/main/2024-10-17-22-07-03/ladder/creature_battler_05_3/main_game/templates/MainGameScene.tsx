import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';
import { CreatureCard, Progress } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";

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

  const player = props.data.entities.player;
  const opponent = props.data.entities.opponent;
  const playerCreature = player?.entities.active_creature;
  const opponentCreature = opponent?.entities.active_creature;

  return (
    <div className="w-full h-full flex justify-center items-center bg-gray-100">
      <div className="aspect-[16/9] w-full max-w-7xl max-h-full flex flex-col">
        <div className="h-2/3 grid grid-cols-2 gap-4 p-4">
          <div className="flex items-end justify-start">
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
          <div className="flex items-end justify-end">
            {playerCreature && (
              <div className="text-right">
                <h3 className="text-xl font-bold">{playerCreature.display_name}</h3>
                <Progress 
                  uid={`${playerCreature.uid}-hp`}
                  value={(playerCreature.stats.hp / playerCreature.stats.max_hp) * 100} 
                  className="w-full"
                />
                <p>HP: {playerCreature.stats.hp} / {playerCreature.stats.max_hp}</p>
              </div>
            )}
          </div>
          <div className="flex items-start justify-start">
            {opponentCreature && (
              <div className="text-left">
                <h3 className="text-xl font-bold">{opponentCreature.display_name}</h3>
                <Progress 
                  uid={`${opponentCreature.uid}-hp`}
                  value={(opponentCreature.stats.hp / opponentCreature.stats.max_hp) * 100} 
                  className="w-full"
                />
                <p>HP: {opponentCreature.stats.hp} / {opponentCreature.stats.max_hp}</p>
              </div>
            )}
          </div>
          <div className="flex items-start justify-end">
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
        </div>
        <div className="h-1/3 p-4">
          <div className="grid grid-cols-2 gap-4">
            {availableButtonSlugs.includes('attack') && playerCreature?.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Base Damage: ${skill.stats.base_damage}`}
                onClick={() => emitButtonClick('attack', skill.uid)}
              >
                <Sword className="mr-2" /> {skill.display_name}
              </SkillButton>
            ))}
            {availableButtonSlugs.includes('back') && (
              <SkillButton
                uid="back-button"
                skillName="Back"
                description="Go back to the previous screen"
                stats=""
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
                stats=""
                onClick={() => emitButtonClick('swap')}
              >
                <Repeat className="mr-2" /> Swap
              </SkillButton>
            )}
          </div>
        </div>
      </div>
      {player && (
        <PlayerCard
          uid={player.uid}
          playerName={player.display_name}
          imageUrl={`/images/players/${player.uid}.png`}
          className="absolute bottom-4 left-4"
        />
      )}
      {opponent && (
        <PlayerCard
          uid={opponent.uid}
          playerName={opponent.display_name}
          imageUrl={`/images/players/${opponent.uid}.png`}
          className="absolute top-4 right-4"
        />
      )}
    </div>
  );
}
