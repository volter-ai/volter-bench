import { useCurrentButtons } from "@/lib/useChoices"
import { Sword, ArrowLeft, SwapHorizontal } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { PlayerCard } from "@/components/ui/custom/player/player_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"

interface Creature {
  uid: string
  display_name: string
  description: string
  stats: {
    hp: number
    max_hp: number
    [key: string]: number
  }
  meta: {
    creature_type: string
    [key: string]: any
  }
  collections: {
    skills: Skill[]
  }
}

interface Skill {
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

interface Player {
  uid: string
  display_name: string
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

  const playerCreature = props.data.entities.player?.entities?.active_creature
  const opponentCreature = props.data.entities.opponent?.entities?.active_creature
  const player = props.data.entities.player
  const opponent = props.data.entities.opponent

  if (!player || !opponent) {
    return <div uid={`${props.data.uid}-error`}>Error: Missing player data</div>
  }

  return (
    <div uid={`${props.data.uid}-container`} className="w-full h-full aspect-video bg-background">
      <div uid={`${props.data.uid}-layout`} className="grid grid-rows-[2fr_1fr] h-full">
        {/* Battlefield */}
        <div uid={`${props.data.uid}-battlefield`} className="grid grid-cols-2 gap-4 p-4">
          {/* Opponent Status */}
          <div uid={`${props.data.uid}-opponent-status`} className="flex items-start justify-start">
            <PlayerCard
              uid={opponent.uid}
              name={opponent.display_name}
              imageUrl="" // Left empty as we don't have image data
            />
            {opponentCreature && (
              <CreatureCard
                uid={opponentCreature.uid}
                name={opponentCreature.display_name}
                imageUrl="" // Left empty as we don't have image data
                currentHp={opponentCreature.stats.hp}
                maxHp={opponentCreature.stats.max_hp}
              />
            )}
          </div>
          
          {/* Player Status */}
          <div uid={`${props.data.uid}-player-status`} className="flex items-end justify-end">
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl="" // Left empty as we don't have image data
            />
            {playerCreature && (
              <CreatureCard
                uid={playerCreature.uid}
                name={playerCreature.display_name}
                imageUrl="" // Left empty as we don't have image data
                currentHp={playerCreature.stats.hp}
                maxHp={playerCreature.stats.max_hp}
              />
            )}
          </div>
        </div>

        {/* UI Area */}
        <div uid={`${props.data.uid}-ui-area`} className="bg-muted p-4 flex flex-col gap-4">
          <div uid={`${props.data.uid}-buttons`} className="flex gap-4 justify-center">
            {availableButtonSlugs.includes('attack') && (
              <Button 
                uid={`${props.data.uid}-attack-button`}
                onClick={() => emitButtonClick('attack')}
              >
                <Sword className="mr-2 h-4 w-4" />
                Attack
              </Button>
            )}
            {availableButtonSlugs.includes('swap') && (
              <Button 
                uid={`${props.data.uid}-swap-button`}
                onClick={() => emitButtonClick('swap')}
              >
                <SwapHorizontal className="mr-2 h-4 w-4" />
                Swap
              </Button>
            )}
            {availableButtonSlugs.includes('back') && (
              <Button 
                uid={`${props.data.uid}-back-button`}
                onClick={() => emitButtonClick('back')}
              >
                <ArrowLeft className="mr-2 h-4 w-4" />
                Back
              </Button>
            )}
          </div>

          {/* Skills */}
          {playerCreature?.collections?.skills && (
            <div uid={`${props.data.uid}-skills`} className="grid grid-cols-2 gap-4">
              {playerCreature.collections.skills.map(skill => (
                <SkillButton
                  key={skill.uid}
                  uid={skill.uid}
                  description={skill.description}
                  stats={{
                    damage: skill.stats.base_damage
                  }}
                >
                  {skill.display_name}
                </SkillButton>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
