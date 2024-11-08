import { useCurrentButtons } from "@/lib/useChoices"
import { Sword, ArrowLeft, SwapHorizontal } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { PlayerCard } from "@/components/ui/custom/player/player_card"

interface Skill {
  uid: string
  display_name: string
  description: string
  stats: {
    base_damage: number
  }
}

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

interface Player {
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
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons()

  const playerCreature = props.data.entities.player?.entities.active_creature
  const opponentCreature = props.data.entities.opponent?.entities.active_creature
  const player = props.data.entities.player
  const opponent = props.data.entities.opponent

  const showingAttacks = availableButtonSlugs.includes('back') && !availableButtonSlugs.includes('attack')

  return (
    <div className="w-full h-full aspect-video bg-background">
      <div className="grid grid-rows-[2fr_1fr] h-full">
        {/* Battlefield */}
        <div className="grid grid-cols-2 gap-4 p-4">
          {/* Opponent Status */}
          <div className="flex items-start justify-start">
            {opponent && opponentCreature && (
              <div className="space-y-4">
                <PlayerCard
                  uid={opponent.uid}
                  name={opponent.display_name}
                  imageUrl={`/players/opponent.png`}
                />
                <CreatureCard
                  uid={opponentCreature.uid}
                  name={opponentCreature.display_name}
                  imageUrl={`/creatures/${opponentCreature.meta.prototype_id}.png`}
                  currentHp={opponentCreature.stats.hp}
                  maxHp={opponentCreature.stats.max_hp}
                />
              </div>
            )}
          </div>

          {/* Opponent Creature */}
          <div className="flex items-center justify-center">
            {opponentCreature && (
              <div className="relative">
                <img 
                  src={`/creatures/${opponentCreature.meta.prototype_id}_front.png`}
                  alt={opponentCreature.display_name}
                  className="w-48 h-48 object-contain"
                />
                <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
              </div>
            )}
          </div>

          {/* Player Creature */}
          <div className="flex items-center justify-center">
            {playerCreature && (
              <div className="relative">
                <img 
                  src={`/creatures/${playerCreature.meta.prototype_id}_back.png`}
                  alt={playerCreature.display_name}
                  className="w-48 h-48 object-contain"
                />
                <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
              </div>
            )}
          </div>

          {/* Player Status */}
          <div className="flex items-start justify-end">
            {player && playerCreature && (
              <div className="space-y-4">
                <PlayerCard
                  uid={player.uid}
                  name={player.display_name}
                  imageUrl={`/players/player.png`}
                />
                <CreatureCard
                  uid={playerCreature.uid}
                  name={playerCreature.display_name}
                  imageUrl={`/creatures/${playerCreature.meta.prototype_id}.png`}
                  currentHp={playerCreature.stats.hp}
                  maxHp={playerCreature.stats.max_hp}
                />
              </div>
            )}
          </div>
        </div>

        {/* UI Area */}
        <div className="bg-muted p-4 flex flex-col gap-4">
          {showingAttacks && playerCreature?.collections.skills ? (
            <div className="grid grid-cols-2 gap-4">
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
          ) : (
            <div className="flex gap-4 justify-center">
              {availableButtonSlugs.includes('attack') && (
                <Button onClick={() => emitButtonClick('attack')}>
                  <Sword className="mr-2 h-4 w-4" />
                  Attack
                </Button>
              )}
              {availableButtonSlugs.includes('swap') && (
                <Button onClick={() => emitButtonClick('swap')}>
                  <SwapHorizontal className="mr-2 h-4 w-4" />
                  Swap
                </Button>
              )}
              {availableButtonSlugs.includes('back') && (
                <Button onClick={() => emitButtonClick('back')}>
                  <ArrowLeft className="mr-2 h-4 w-4" />
                  Back
                </Button>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
