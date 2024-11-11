import { useCurrentButtons } from "@/lib/useChoices.ts"
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
  entities: {
    player: Player
    opponent: Player
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons()

  const playerCreature = props.data.entities.player?.entities.active_creature
  const opponentCreature = props.data.entities.opponent?.entities.active_creature

  return (
    <div className="h-screen w-full aspect-video flex flex-col">
      {/* Battlefield Area (upper 2/3) */}
      <div className="h-2/3 grid grid-cols-2 gap-4 p-4 bg-slate-100">
        {/* Top Left - Opponent Status */}
        <div className="flex justify-start items-start">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              imageUrl={`/creatures/${opponentCreature.meta.prototype_id}_front.png`}
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
              imageUrl={`/players/${props.data.entities.opponent.meta.prototype_id}.png`}
            />
          )}
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex justify-start items-end">
          {props.data.entities.player && (
            <PlayerCard
              uid={props.data.entities.player.uid}
              name={props.data.entities.player.display_name}
              imageUrl={`/players/${props.data.entities.player.meta.prototype_id}.png`}
            />
          )}
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex justify-end items-end">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl={`/creatures/${playerCreature.meta.prototype_id}_back.png`}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* UI Area (lower 1/3) */}
      <div className="h-1/3 p-4 bg-white flex flex-col gap-2">
        <div className="flex flex-wrap gap-2">
          {availableButtonSlugs.includes('attack') && 
            playerCreature?.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                description={skill.description}
                stats={{
                  damage: skill.stats.base_damage,
                  type: skill.meta.skill_type
                }}
              >
                {skill.display_name}
              </SkillButton>
            ))
          }
        </div>
        
        <div className="flex gap-2">
          {availableButtonSlugs.includes('back') && (
            <Button onClick={() => emitButtonClick('back')}>
              <ArrowLeft className="mr-2" />
              Back
            </Button>
          )}
          
          {availableButtonSlugs.includes('swap') && (
            <Button onClick={() => emitButtonClick('swap')}>
              <SwapHorizontal className="mr-2" />
              Swap
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
