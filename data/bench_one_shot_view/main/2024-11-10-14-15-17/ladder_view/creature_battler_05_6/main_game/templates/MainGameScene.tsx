import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, SwapHorizontal } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";

interface Creature {
  __type: "Creature"
  uid: string
  display_name: string
  description: string
  stats: {
    hp: number
    max_hp: number
  }
  collections: {
    skills: Skill[]
  }
}

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    base_damage: number
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
  entities: {
    active_creature?: Creature
  }
}

interface GameUIData {
  entities: {
    player: Player
    opponent: Player
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player?.entities.active_creature
  const opponentCreature = props.data.entities.opponent?.entities.active_creature

  return (
    <div className="h-screen w-screen aspect-video flex flex-col">
      {/* Battlefield Area - Upper 2/3 */}
      <div className="h-2/3 grid grid-cols-2 gap-4 p-4 bg-slate-100">
        {/* Top Left - Opponent Status */}
        <div className="flex justify-start items-start">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              imageUrl={`/creatures/${opponentCreature.uid}/front.png`}
              currentHp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Top Right - Opponent Creature */}
        <div className="flex justify-end items-start">
          {props.data.entities.opponent && (
            <PlayerCard
              uid={props.data.entities.opponent.uid}
              name={props.data.entities.opponent.display_name}
              imageUrl={`/players/${props.data.entities.opponent.uid}/avatar.png`}
            />
          )}
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex justify-start items-end">
          {props.data.entities.player && (
            <PlayerCard
              uid={props.data.entities.player.uid}
              name={props.data.entities.player.display_name}
              imageUrl={`/players/${props.data.entities.player.uid}/avatar.png`}
            />
          )}
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex justify-end items-end">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl={`/creatures/${playerCreature.uid}/back.png`}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* UI Area - Lower 1/3 */}
      <div className="h-1/3 p-4 bg-white flex flex-col gap-4">
        <div className="flex gap-4 justify-center">
          {availableButtonSlugs.includes('attack') && playerCreature?.collections.skills.map(skill => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              description={skill.description}
              stats={{
                damage: skill.stats.base_damage
              }}
            >
              <Sword className="mr-2 h-4 w-4" />
              {skill.display_name}
            </SkillButton>
          ))}
        </div>

        <div className="flex gap-4 justify-center">
          {availableButtonSlugs.includes('back') && (
            <Button onClick={() => emitButtonClick('back')}>
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back
            </Button>
          )}
          
          {availableButtonSlugs.includes('swap') && (
            <Button onClick={() => emitButtonClick('swap')}>
              <SwapHorizontal className="mr-2 h-4 w-4" />
              Swap
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
