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
    prototype_id: string
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
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities?.player?.entities?.active_creature
  const opponentCreature = props.data.entities?.opponent?.entities?.active_creature
  const player = props.data.entities?.player
  const opponent = props.data.entities?.opponent

  if (!player || !opponent) {
    return null
  }

  return (
    <div className="h-screen w-screen aspect-video flex flex-col bg-gradient-to-b from-blue-100 to-blue-200">
      {/* Battlefield Area */}
      <div className="flex-grow grid grid-cols-2 p-4 gap-4">
        {/* Opponent Side */}
        <div className="flex flex-col items-end justify-start gap-4">
          {opponent && (
            <PlayerCard
              uid={opponent.uid}
              name={opponent.display_name}
              imageUrl={`/players/${opponent.meta.prototype_id}.png`}
              className="transform -scale-x-100"
            />
          )}
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              imageUrl={`/creatures/${opponentCreature.meta.prototype_id}.png`}
              currentHp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
              className="transform -scale-x-100"
            />
          )}
        </div>
        
        {/* Player Side */}
        <div className="flex flex-col items-start justify-end gap-4">
          {player && (
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl={`/players/${player.meta.prototype_id}.png`}
            />
          )}
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl={`/creatures/${playerCreature.meta.prototype_id}.png`}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 bg-white/90 p-4 border-t-2 border-gray-200">
        <div className="flex flex-wrap gap-2">
          {availableButtonSlugs.includes('attack') && playerCreature?.collections?.skills?.map(skill => (
            skill.__type === "Skill" && (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                description={skill.description}
                stats={{
                  damage: skill.stats.base_damage
                }}
                onClick={() => emitButtonClick('attack', { skillId: skill.uid })}
              >
                <Sword className="mr-2 h-4 w-4" />
                {skill.display_name}
              </SkillButton>
            )
          ))}
          
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
