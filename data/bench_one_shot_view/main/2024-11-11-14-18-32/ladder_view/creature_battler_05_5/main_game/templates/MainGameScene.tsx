import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, SwapHorizontal } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { PlayerCard } from "@/components/ui/custom/player/player_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { Button } from "@/components/ui/button"

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    base_damage: number
  }
  meta: {
    skill_type: string
    is_physical: boolean
  }
}

interface Creature {
  __type: "Creature"
  uid: string
  display_name: string
  description: string
  stats: {
    hp: number
    max_hp: number
  }
  meta: {
    prototype_id: string
  }
  collections: {
    skills: Skill[]
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
  meta: {
    prototype_id: string
  }
  entities: {
    active_creature?: Creature
  }
}

interface GameUIData {
  uid: string
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
    <div className="w-full h-full aspect-video relative bg-background" uid={`${props.data.uid}-container`}>
      {/* Battlefield Area */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4" uid={`${props.data.uid}-battlefield`}>
        {/* Opponent Status */}
        <div className="flex justify-start items-start" uid={`${props.data.uid}-opponent-status`}>
          {props.data.entities.opponent && (
            <PlayerCard
              uid={props.data.entities.opponent.uid}
              name={props.data.entities.opponent.display_name}
              imageUrl={`/players/${props.data.entities.opponent.meta.prototype_id}.png`}
            />
          )}
        </div>

        {/* Opponent Creature */}
        <div className="flex justify-center items-center" uid={`${props.data.uid}-opponent-creature`}>
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              imageUrl={`/creatures/${opponentCreature.meta.prototype_id}/front.png`}
              currentHp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Player Creature */}
        <div className="flex justify-center items-center" uid={`${props.data.uid}-player-creature`}>
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl={`/creatures/${playerCreature.meta.prototype_id}/back.png`}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Player Status */}
        <div className="flex justify-end items-end" uid={`${props.data.uid}-player-status`}>
          {props.data.entities.player && (
            <PlayerCard
              uid={props.data.entities.player.uid}
              name={props.data.entities.player.display_name}
              imageUrl={`/players/${props.data.entities.player.meta.prototype_id}.png`}
            />
          )}
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 p-4 flex flex-col gap-2" uid={`${props.data.uid}-ui`}>
        <div className="flex flex-wrap gap-2" uid={`${props.data.uid}-buttons`}>
          {availableButtonSlugs.includes('attack') && playerCreature?.collections.skills.map(skill => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              description={skill.description}
              stats={{
                damage: skill.stats.base_damage,
                // Add other stats as needed from the skill data
              }}
            >
              <Sword className="mr-2 h-4 w-4" />
              {skill.display_name}
            </SkillButton>
          ))}
          
          {availableButtonSlugs.includes('back') && (
            <SkillButton
              uid={`${props.data.uid}-back`}
              description="Return to previous screen"
              stats={{}}
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back
            </SkillButton>
          )}
          
          {availableButtonSlugs.includes('swap') && (
            <SkillButton
              uid={`${props.data.uid}-swap`}
              description="Switch to a different creature"
              stats={{}}
            >
              <SwapHorizontal className="mr-2 h-4 w-4" />
              Swap
            </SkillButton>
          )}
        </div>
      </div>
    </div>
  )
}
