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
    prototype_id: string
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
  description: string
  meta: {
    prototype_id: string
    [key: string]: any
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

  const playerCreature = props.data.entities.player?.entities?.active_creature
  const opponentCreature = props.data.entities.opponent?.entities?.active_creature
  const player = props.data.entities.player
  const opponent = props.data.entities.opponent

  if (!playerCreature || !opponentCreature || !player || !opponent) {
    return <div className="text-center p-4">Loading battle...</div>
  }

  return (
    <div className="h-screen w-screen bg-gradient-to-b from-blue-100 to-blue-200">
      <div className="grid grid-rows-[2fr_1fr] h-full">
        {/* Battlefield */}
        <div className="grid grid-cols-2 gap-4 p-4">
          {/* Opponent Status */}
          <div className="flex items-start justify-start">
            <PlayerCard
              uid={opponent.uid}
              name={opponent.display_name}
              imageUrl={`/players/${opponent.meta.prototype_id}.png`}
            />
          </div>
          
          {/* Opponent Creature */}
          <div className="flex items-center justify-center">
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              imageUrl={`/creatures/${opponentCreature.meta.prototype_id}.png`}
              currentHp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          </div>

          {/* Player Creature */}
          <div className="flex items-center justify-center">
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl={`/creatures/${playerCreature.meta.prototype_id}.png`}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          </div>

          {/* Player Status */}
          <div className="flex items-end justify-end">
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl={`/players/${player.meta.prototype_id}.png`}
            />
          </div>
        </div>

        {/* UI Area */}
        <div className="bg-white/90 p-4 flex flex-col gap-4">
          <div className="flex gap-4 justify-center">
            {availableButtonSlugs.includes('attack') && (
              <Button
                onClick={() => emitButtonClick('attack')}
                className="flex gap-2 items-center"
              >
                <Sword className="w-4 h-4" />
                Attack
              </Button>
            )}
            
            {availableButtonSlugs.includes('swap') && (
              <Button
                onClick={() => emitButtonClick('swap')}
                className="flex gap-2 items-center"
              >
                <SwapHorizontal className="w-4 h-4" />
                Swap
              </Button>
            )}

            {availableButtonSlugs.includes('back') && (
              <Button
                onClick={() => emitButtonClick('back')}
                className="flex gap-2 items-center"
              >
                <ArrowLeft className="w-4 h-4" />
                Back
              </Button>
            )}
          </div>

          {/* Skills */}
          {availableButtonSlugs.includes('attack') && (
            <div className="grid grid-cols-2 gap-4">
              {playerCreature.collections.skills.map((skill) => (
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
