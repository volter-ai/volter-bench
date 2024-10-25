import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, RefreshCw } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";

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
  collections?: {
    skills: Skill[];
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
  message?: string;
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player?.entities.active_creature;
  const opponentCreature = props.data.entities.opponent?.entities.active_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gradient-to-b from-blue-200 to-green-200">
      {/* Battlefield */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Top-left: Opponent creature */}
        <div className="flex justify-start items-start">
          {opponentCreature && (
            <img
              src={`/images/creatures/${opponentCreature.meta.creature_type}_front.png`}
              alt={opponentCreature.display_name}
              className="w-32 h-32 object-contain"
            />
          )}
        </div>

        {/* Top-right: Opponent status */}
        <div className="flex flex-col justify-start items-end">
          <PlayerCard
            uid={props.data.entities.opponent.uid}
            playerName={props.data.entities.opponent.display_name}
            imageUrl="/images/opponent_avatar.png"
          />
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

        {/* Bottom-left: Player creature */}
        <div className="flex justify-start items-end">
          {playerCreature && (
            <img
              src={`/images/creatures/${playerCreature.meta.creature_type}_back.png`}
              alt={playerCreature.display_name}
              className="w-32 h-32 object-contain"
            />
          )}
        </div>

        {/* Bottom-right: Player status */}
        <div className="flex flex-col justify-end items-end">
          <PlayerCard
            uid={props.data.entities.player.uid}
            playerName={props.data.entities.player.display_name}
            imageUrl="/images/player_avatar.png"
          />
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
        {props.data.message ? (
          <div className="text-center text-xl font-bold mb-4">{props.data.message}</div>
        ) : (
          <div className="grid grid-cols-2 gap-4">
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
            {availableButtonSlugs.includes('swap') && (
              <SkillButton
                uid="swap-button"
                skillName="Swap"
                description="Swap your active creature"
                stats=""
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
                stats={`Damage: ${skill.stats.base_damage}`}
                onClick={() => emitButtonClick(skill.uid)}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
